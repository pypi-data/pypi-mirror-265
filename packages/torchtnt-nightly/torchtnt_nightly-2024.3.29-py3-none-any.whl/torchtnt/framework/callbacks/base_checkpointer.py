# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

import abc
import bisect
import logging
import os
from datetime import timedelta
from typing import Any, cast, Iterable, List, Literal, Optional, Union

import torch.distributed as dist

from torchtnt.framework.callback import Callback
from torchtnt.framework.callbacks._checkpoint_utils import (
    _delete_checkpoint,
    _metadata_exists,
    _sort_by_metric_value,
    _sort_by_recency,
    get_best_checkpoint_path,
    get_checkpoint_dirpaths,
    get_latest_checkpoint_path,
    rank_zero_read_and_broadcast,
)
from torchtnt.framework.callbacks.checkpointer_types import (
    BestCheckpointConfig,
    RestoreOptions,
)
from torchtnt.framework.state import EntryPoint, State
from torchtnt.framework.unit import AppStateMixin, TEvalUnit, TTrainData, TTrainUnit
from torchtnt.framework.utils import get_timing_context
from torchtnt.utils.distributed import PGWrapper
from torchtnt.utils.fsspec import get_filesystem
from torchtnt.utils.rank_zero_log import rank_zero_info, rank_zero_warn

logger: logging.Logger = logging.getLogger(__name__)


class BaseCheckpointer(Callback, metaclass=abc.ABCMeta):
    """
    Abstract base class for file-based state_dict checkpointing. This class can be used as the base of a checkpointing callback, and handles
    checkpointing frequency logic, checkpoint naming, checkpoint purging / upkeep, and process group synchronization. There are only two methods
    that need to be implemented by subclasses:

    1) ``_checkpoint_impl`` which implements the checkpoint saving logic, given the relevant checkpoint items and path.
    2) ``restore`` which implements restoring the checkpoint given the relevant checkpoint path.

    The subclass may override the ``metadata_fname`` attribute to specify the filename of the metadata file that will be written within the checkpoint directory.
    This will be used by this base class to ensure the integrity of the checkpoint.

    Args:
        dirpath: Parent directory to save checkpoints to.
        save_every_n_train_steps: Frequency of steps with which to save checkpoints during the train epoch. If None, no intra-epoch checkpoints are generated.
        save_every_n_epochs: Frequency of epochs with which to save checkpoints during training. If None, no end-of-epoch checkpoints are generated.
        save_every_n_eval_epochs: Frequency of evaluation epochs with which to save checkpoints during training. Use this if wanting to save checkpoints after every eval epoch during fit.
        keep_last_n_checkpoints: Number of most recent checkpoints to keep. If None, all checkpoints are kept. If an excess of existing checkpoints are present, the oldest ones will be deleted to clean the difference. If best checkpoint config is enabled, this param will manage the top n checkpoints instead.
        best_checkpoint_config: Configuration for saving the best checkpoint based on a monitored metric. The metric is read off the attribute of the unit prior to checkpoint.
        process_group: The process group on which the ranks will communicate on. If the process group is not gloo-based, a new gloo-based process group will be created.

    Note:
        If torch.distributed is available and default process group is initialized, the constructor will call a collective operation for rank 0 to broadcast the dirpath to all other ranks

    Note:
        This class assumes checkpoint items are saved in the directory provided in ``_checkpoint_impl`` and will be in the form of ``<dirpath>/<epoch>-<step>/``. Checkpoint contents
        should be stored within this directory, as deleting and retrieving latest checkpoint relies on reading the <epoch>-<step> directory name within <dirpath>

    Note:
        If best_checkpoint_config is enabled, the attribute must be on the unit upon checkpoint time, and must be castable to "float". This value must be maintained by the unit, and updated
        appropriately. For example, if logging validation accuracy, the unit must be responsible for maintaining the value and resetting it when the epoch ends. If the metric value is None, the
        checkpoint will be saved, without the metric value in the checkpoint name
    """

    metadata_fname: Optional[str] = None

    def __init__(
        self,
        dirpath: str,
        *,
        save_every_n_train_steps: Optional[int] = None,
        save_every_n_epochs: Optional[int] = None,
        save_every_n_eval_epochs: Optional[int] = None,
        keep_last_n_checkpoints: Optional[int] = None,
        best_checkpoint_config: Optional[BestCheckpointConfig] = None,
        process_group: Optional[dist.ProcessGroup] = None,
    ) -> None:
        if save_every_n_train_steps is not None and save_every_n_train_steps <= 0:
            raise ValueError(
                f"Invalid value passed for save_every_n_train_steps. Expected to receive either None or positive number, but received {save_every_n_train_steps}"
            )
        if save_every_n_epochs is not None and save_every_n_epochs <= 0:
            raise ValueError(
                f"Invalid value passed for save_every_n_epochs. Expected to receive either None or positive number, but received {save_every_n_epochs}"
            )
        if keep_last_n_checkpoints is not None and keep_last_n_checkpoints <= 0:
            raise ValueError(
                f"Invalid value passed for keep_last_n_checkpoints. Expected to receive either None or positive number, but received {keep_last_n_checkpoints}"
            )

        self._best_checkpoint_config = best_checkpoint_config
        if best_checkpoint_config and best_checkpoint_config.mode not in {"min", "max"}:
            raise ValueError(
                f"Invalid value passed for best_checkpoint_config.mode. Expected to receive 'min' or 'max', but received {best_checkpoint_config.mode}"
            )

        self._save_every_n_train_steps = save_every_n_train_steps
        self._save_every_n_epochs = save_every_n_epochs
        self._save_every_n_eval_epochs = save_every_n_eval_epochs
        self._keep_last_n_checkpoints = keep_last_n_checkpoints

        self._ckpt_dirpaths: List[str] = []
        if self._keep_last_n_checkpoints:
            metric_name = (
                None
                if not best_checkpoint_config
                else best_checkpoint_config.monitored_metric
            )
            ckpt_dirpaths = get_checkpoint_dirpaths(
                dirpath=dirpath,
                metadata_fname=self.metadata_fname,
                metric_name=metric_name,
                process_group=process_group,
            )

            # sort by metric value if doing best checkpoint, else by recency
            if best_checkpoint_config:
                self._ckpt_dirpaths = _sort_by_metric_value(
                    ckpt_dirpaths, mode=best_checkpoint_config.mode
                )
            else:
                self._ckpt_dirpaths = _sort_by_recency(ckpt_dirpaths)

        self._process_group: Optional[dist.ProcessGroup] = None
        self._setup_gloo_pg(process_group)
        self._pg_wrapper = PGWrapper(process_group)

        # sync dirpaths from rank 0
        self._sync_dirpath_to_all_ranks(dirpath)

    def _setup_gloo_pg(self, process_group: Optional[dist.ProcessGroup]) -> None:
        """
        Setups gloo process group to be used for any collectives called during
        checkpointing. If global process group is already gloo, no action is required.
        Gloo is used over nccl for better compatibility.
        """
        if not dist.is_initialized():
            # there can be no process group
            return

        if process_group is None:
            # use global process group
            process_group = dist.group.WORLD

        # we create a new gloo process group if different backend is being used
        if dist.get_backend(process_group) != dist.Backend.GLOO:
            rank_zero_info("Creating new gloo process group for checkpointing.")
            self._process_group = dist.new_group(
                timeout=timedelta(seconds=3600), backend=dist.Backend.GLOO
            )
        else:
            self._process_group = process_group

    def _sync_dirpath_to_all_ranks(self, dirpath: str) -> None:
        if not (dist.is_available() and dist.is_initialized()):
            self._dirpath: str = dirpath
            return

        dirpath_container = [dirpath] if self._pg_wrapper.get_rank() == 0 else [""]
        # broadcast directory from global rank 0
        dist.broadcast_object_list(dirpath_container, src=0, group=self._process_group)
        updated_dirpath = dirpath_container[0]
        if updated_dirpath != dirpath:
            logger.warning(f"Updating dirpath to match rank 0: {updated_dirpath}")

        self._dirpath: str = updated_dirpath

    @property
    def dirpath(self) -> str:
        """Returns parent directory to save to."""
        return self._dirpath

    def _generate_checkpoint_and_upkeep(
        self, state: State, unit: Union[TTrainUnit, TEvalUnit], hook: str
    ) -> bool:
        """
        Implementation for saving checkpoint while taking care of checkpoint
        name generation and cleanup of oldest checkpoints.

        Args:
            state: Current state of the trainer.
            unit: Current training unit.
            hook: Hook at which checkpoint is being saved.

        Returns:
            True if checkpoint was successfully saved. False otherwise.
        """
        unit = cast(TTrainUnit, unit)

        # 1) generate checkpoint name
        num_steps_completed = unit.train_progress.num_steps_completed
        if state.entry_point == EntryPoint.FIT:
            num_steps_completed += cast(
                TEvalUnit, unit
            ).eval_progress.num_steps_completed
        epoch = unit.train_progress.num_epochs_completed
        checkpoint_path = _get_save_path(self._dirpath, epoch, num_steps_completed)

        # 1.5) Ensure the need to checkpoint again at the end of training
        if hook == "on_train_end" and self._does_checkpoint_exist(
            checkpoint_path, process_group=self._process_group
        ):
            rank_zero_warn("Final checkpoint already exists, skipping.", logger=logger)
            return False

        # 2) handle best checkpoint config on all hooks except `on_train_end`
        # TODO: isolate this logic into its own function
        metric_value_f: Optional[float] = None
        best_checkpoint_config = self._best_checkpoint_config
        if best_checkpoint_config:
            if not hasattr(unit, best_checkpoint_config.monitored_metric):
                raise RuntimeError(
                    f"Unit does not have attribute {best_checkpoint_config.monitored_metric}, unable to retrieve metric to checkpoint."
                )

            metric_value = getattr(unit, best_checkpoint_config.monitored_metric)
            if metric_value is not None:
                try:
                    metric_value_f = float(metric_value)
                except Exception as e:
                    raise RuntimeError(
                        f"Unable to convert monitored metric {best_checkpoint_config.monitored_metric} to a float. Please ensure the value can be converted to float and is not a multi-element tensor value."
                    ) from e

                # update checkpoint path to include the metric value info
                checkpoint_path += (
                    f"_{best_checkpoint_config.monitored_metric}={metric_value_f}"
                )

        should_checkpoint = self._should_save_checkpoint(metric_value_f)
        if not should_checkpoint:
            return False

        # 3) try to save checkpoint
        success = self._checkpoint_impl(
            state,
            unit,
            checkpoint_path=checkpoint_path,
            hook=hook,
        )

        if success:
            # remove the checkpoint if applicable
            # and update the tracked list of checkpoint paths

            if self._should_remove_checkpoint():
                self._remove_checkpoint(state)

            if best_checkpoint_config:
                if metric_value_f:
                    # insert the checkpoint path at the right index to preserve ordering
                    keys = [
                        float(os.path.basename(x).split("=")[-1])
                        for x in self._ckpt_dirpaths
                    ]
                    if best_checkpoint_config.mode == "min":
                        keys.reverse()
                    # Use bisect.bisect() to find the insertion point
                    idx = bisect.bisect(keys, metric_value_f)
                    if best_checkpoint_config.mode == "min":
                        idx = len(self._ckpt_dirpaths) - idx
                    self._ckpt_dirpaths.insert(idx, checkpoint_path)
            else:
                self._ckpt_dirpaths.append(checkpoint_path)

        return success

    def on_train_start(self, state: State, unit: TTrainUnit) -> None:
        # clean up the difference if surplus of checkpoints exist
        keep_last_n_checkpoints = self._keep_last_n_checkpoints
        if (
            keep_last_n_checkpoints
            and len(self._ckpt_dirpaths) > keep_last_n_checkpoints
        ):
            logger.warning(
                " ".join(
                    [
                        f"{len(self._ckpt_dirpaths)} checkpoints found in {self._dirpath}.",
                        f"Deleting {len(self._ckpt_dirpaths) - keep_last_n_checkpoints} oldest",
                        "checkpoints to enforce ``keep_last_n_checkpoints`` argument.",
                    ]
                )
            )
            for _ in range(len(self._ckpt_dirpaths) - keep_last_n_checkpoints):
                self._remove_checkpoint(state)

    def on_train_step_end(self, state: State, unit: TTrainUnit) -> None:
        num_steps_completed = unit.train_progress.num_steps_completed
        save_every_n_train_steps = self._save_every_n_train_steps
        if (
            save_every_n_train_steps is None
            or num_steps_completed % save_every_n_train_steps != 0
        ):
            return

        self._generate_checkpoint_and_upkeep(state, unit, hook="on_train_step_end")

    def on_train_epoch_end(self, state: State, unit: TTrainUnit) -> None:
        epoch = unit.train_progress.num_epochs_completed
        save_every_n_epochs = self._save_every_n_epochs
        if save_every_n_epochs is None or epoch % save_every_n_epochs != 0:
            return

        self._generate_checkpoint_and_upkeep(state, unit, hook="on_train_epoch_end")

    def on_eval_epoch_end(self, state: State, unit: TEvalUnit) -> None:
        epoch = unit.eval_progress.num_epochs_completed
        save_every_n_eval_epochs = self._save_every_n_eval_epochs
        if save_every_n_eval_epochs is None or epoch % save_every_n_eval_epochs != 0:
            return

        self._generate_checkpoint_and_upkeep(state, unit, hook="on_eval_epoch_end")

    def on_train_end(self, state: State, unit: TTrainUnit) -> None:
        self._generate_checkpoint_and_upkeep(state, unit, hook="on_train_end")

    @abc.abstractmethod
    def _checkpoint_impl(
        self,
        state: State,
        unit: AppStateMixin,
        *,
        checkpoint_path: str,
        hook: str,
    ) -> bool:
        """
        Implementation of saving checkpoint.

        Args:
            state: current application state
            unit: current unit
            checkpoint_path: path to save checkpoint
            hook: name of callback hook that triggered this function call

        Returns:
            Whether a new checkpoint was created.
        """
        ...

    def _should_save_checkpoint(self, metric_value: Optional[float] = None) -> bool:
        """
        Whether a new checkpoint should be saved.
        """

        keep_last_n_checkpoints = self._keep_last_n_checkpoints
        if not keep_last_n_checkpoints:
            # always save candidate checkpoint if no limit of checkpoints is specified
            return True

        if len(self._ckpt_dirpaths) < keep_last_n_checkpoints:
            # limit of checkpoints has not been reached
            return True

        best_checkpoint_config = self._best_checkpoint_config
        if not best_checkpoint_config:
            # we always save the latest checkpoint
            return True

        # otherwise, we need to determine if we should overwrite the worst checkpoint
        assert metric_value
        ckpt_value = float(self._ckpt_dirpaths[0].split("=")[-1])

        # do not checkpoint if candidate is worse than the existing one
        if best_checkpoint_config.mode == "min" and metric_value > ckpt_value:
            return False
        elif best_checkpoint_config.mode == "max" and metric_value < ckpt_value:
            return False
        # the candidate checkpoint is better than the existing one, so we must overwrite it
        return True

    def _should_remove_checkpoint(self) -> bool:
        """
        Whether the oldest / worst checkpoint should be removed.

        This is called after the candidate checkpoint is saved, so it is already evaluated that the
        candidate checkpoint was worth saving.
        """

        keep_last_n_checkpoints = self._keep_last_n_checkpoints
        return (
            keep_last_n_checkpoints is not None
            and len(self._ckpt_dirpaths) >= keep_last_n_checkpoints
        )

    def _remove_checkpoint(self, state: State) -> None:
        # remove oldest checkpoint directory
        oldest_ckpt_path = self._ckpt_dirpaths.pop(0)
        with get_timing_context(state, f"{self.__class__.__name__}.delete_checkpoint"):
            if self._pg_wrapper.get_rank() == 0:
                # only delete on rank 0
                _delete_checkpoint(oldest_ckpt_path)
            self._pg_wrapper.barrier()

    @staticmethod
    @abc.abstractmethod
    def restore(
        path: str,
        unit: AppStateMixin,
        *,
        train_dataloader: Optional[Iterable[TTrainData]] = None,
        process_group: Optional[dist.ProcessGroup] = None,
        restore_options: Optional[RestoreOptions] = None,
    ) -> None:
        """Method to restore checkpoint state from a path.

        There are additional flags offered should the user want to skip loading the train and eval progress.
        By default, the train and eval progress are restored, if applicable.

        Args:
            path: Path of the checkpoint to restore.
            unit: An instance of :class:`~torchtnt.framework.unit.TrainUnit`, :class:`~torchtnt.framework.unit.EvalUnit`, or :class:`~torchtnt.framework.unit.PredictUnit` containing states to restore.
            train_dataloader: An optional train dataloader to restore.
            process_group: The process group on which the ranks will communicate on. default: ``None`` (the entire world)
            restore_options: Controls what to filter when restoring the state.
        """
        ...

    @classmethod
    def restore_from_latest(
        cls,
        dirpath: str,
        unit: AppStateMixin,
        *,
        train_dataloader: Optional[Iterable[TTrainData]] = None,
        process_group: Optional[dist.ProcessGroup] = None,
        restore_options: Optional[RestoreOptions] = None,
        **kwargs: Any,
    ) -> bool:
        """
        Given a parent directory where checkpoints are saved, restore the checkpoint state from the latest checkpoint in the directory.

        There are additional flags offered should the user want to skip loading the train and eval progress.
        By default, the train and eval progress are restored, if applicable.

        Args:
            dirpath: Parent directory from which to get the latest checkpoint.
            unit: An instance of :class:`~torchtnt.framework.unit.TrainUnit`, :class:`~torchtnt.framework.unit.EvalUnit`, or :class:`~torchtnt.framework.unit.PredictUnit` containing states to restore.
            train_dataloader: An optional train dataloader to restore.
            process_group: The process group on which the ranks will communicate on. default: ``None`` (the entire world)
            restore_options: Controls what to  filter when restoring the state.

        Returns:
            True if the latest checkpoint directory was found and successfully restored, otherwise False.
        """
        path = get_latest_checkpoint_path(
            dirpath, metadata_fname=cls.metadata_fname, process_group=process_group
        )
        if path is None:
            return False
        logger.info(f"Restoring from path: {path}")
        cls.restore(
            path,
            unit,
            train_dataloader=train_dataloader,
            process_group=process_group,
            restore_options=restore_options,
            **kwargs,
        )
        return True

    @classmethod
    def restore_from_best(
        cls,
        dirpath: str,
        unit: AppStateMixin,
        metric_name: str,
        mode: Literal["min", "max"],
        *,
        train_dataloader: Optional[Iterable[TTrainData]] = None,
        process_group: Optional[dist.ProcessGroup] = None,
        restore_options: Optional[RestoreOptions] = None,
        **kwargs: Any,
    ) -> bool:
        """
        Given a parent directory where checkpoints are saved, restore the checkpoint state from the best checkpoint in the directory.

        There are additional flags offered should the user want to skip loading the train and eval progress.
        By default, the train and eval progress are restored, if applicable.

        Args:
            dirpath: Parent directory from which to get the latest checkpoint.
            unit: An instance of :class:`~torchtnt.framework.unit.TrainUnit`, :class:`~torchtnt.framework.unit.EvalUnit`, or :class:`~torchtnt.framework.unit.PredictUnit` containing states to restore.
            metric_name: Name of the metric to use to find the best checkpoint.
            mode: Either 'min' or 'max'. If 'min', finds and loads the lowest value metric checkpoint. If 'max', finds and loads the largest.
            train_dataloader: An optional train dataloader to restore.
            process_group: The process group on which the ranks will communicate on. default: ``None`` (the entire world)
            restore_options: Controls what to  filter when restoring the state.

        Returns:
            True if the best checkpoint directory was found and successfully restored, otherwise False.
        """
        best_checkpoint_path = get_best_checkpoint_path(
            dirpath,
            metric_name=metric_name,
            mode=mode,
            metadata_fname=cls.metadata_fname,
            process_group=process_group,
        )

        if best_checkpoint_path is None:
            rank_zero_warn(
                f"No checkpoints with metric name {metric_name} were found in {dirpath}. Not loading any checkpoint.",
                logger=logger,
            )
            return False

        rank_zero_info(f"Loading checkpoint from {best_checkpoint_path}")

        cls.restore(
            best_checkpoint_path,
            unit,
            train_dataloader=train_dataloader,
            process_group=process_group,
            restore_options=restore_options,
            **kwargs,
        )

        return True

    @rank_zero_read_and_broadcast
    def _does_checkpoint_exist(
        self, checkpoint_path: str, process_group: Optional[dist.ProcessGroup] = None
    ) -> bool:
        """
        Checking whether a checkpoint already exists by verifying whether the optional metadata file is present in the directory.
        If the checkpointer doesn't have a metadata file, this function will always return False.
        """
        metadata_fname = self.metadata_fname
        if not metadata_fname:
            return False

        fs = get_filesystem(checkpoint_path)
        return _metadata_exists(fs, checkpoint_path, metadata_fname)


def _get_save_path(dirpath: str, epoch: int, step: int) -> str:
    # TODO: discuss whether this path should be customized
    return os.path.join(dirpath, f"epoch_{epoch}_step_{step}")
