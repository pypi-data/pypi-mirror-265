# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

from dataclasses import dataclass
from typing import Literal, Optional


# TODO: eventually support overriding all knobs
@dataclass
class KnobOptions:
    """
    Controls the knobs in TorchSnapshot.

    Args:
        max_per_rank_io_concurrency: Maximum number of concurrent IO operations per rank. Defaults to 16.
    """

    max_per_rank_io_concurrency: Optional[int] = None


@dataclass
class RestoreOptions:
    """
    Options when restoring a snapshot.

    Args:
        restore_train_progress: Whether to restore the training progress state.
        restore_eval_progress: Whether to restore the evaluation progress state.
        restore_optimizers: Whether to restore the optimizer states.
        restore_lr_schedulers: Whether to restore the lr scheduler states.
    """

    restore_train_progress: bool = True
    restore_eval_progress: bool = True
    restore_optimizers: bool = True
    restore_lr_schedulers: bool = True


@dataclass
class BestCheckpointConfig:
    """
    Config for saving the best checkpoints.

    Args:
        monitored_metric: Metric to monitor for saving best checkpoints. Must be an numerical or tensor attribute on the unit.
        mode: One of `min` or `max`. The save file is overwritten based the max or min of the monitored metric.
    """

    monitored_metric: str
    mode: Literal["min", "max"] = "min"
