from __future__ import annotations

from keras import ops
from keras.metrics import (
    FalsePositives,
    Metric,
    SpecificityAtSensitivity,
    TruePositives,
)


class MaxSignificance(Metric):
    def __init__(
        self,
        thresholds=None,
        class_id=1,
        name="max_significance",
        dtype=None,
    ):
        super().__init__(name, dtype)
        self.class_id = class_id
        self.tp = TruePositives(thresholds=thresholds, dtype=dtype)
        self.fp = FalsePositives(thresholds=thresholds, dtype=dtype)

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = ops.convert_to_tensor(y_true)
        y_pred = ops.convert_to_tensor(y_pred)

        y_true = ops.cond(
            ops.logical_and(
                ops.greater(ops.ndim(y_true), 1),
                ops.greater(ops.shape(y_true)[-1], 1),
            ),
            lambda: ops.take(y_true, self.class_id, axis=-1),
            lambda: y_true,
        )

        y_pred = ops.cond(
            ops.logical_and(
                ops.greater(ops.ndim(y_pred), 1),
                ops.greater(ops.shape(y_pred)[-1], 1),
            ),
            lambda: ops.take(y_pred, self.class_id, axis=-1),
            lambda: y_pred,
        )

        self.tp.update_state(y_true, y_pred, sample_weight)
        self.fp.update_state(y_true, y_pred, sample_weight)

    def result(self):
        s = self.tp.result()
        b = self.fp.result()
        significance = ops.divide(s, ops.sqrt(s + b))
        max_significance = ops.max(significance)
        return max_significance


class RejectionAtEfficiency(Metric):
    def __init__(
        self,
        efficiency,
        num_thresholds=200,
        class_id=None,
        name="rejection_at_efficiency",
        dtype=None,
    ):
        super().__init__(name, dtype)
        self.specificity_at_sensitivity = SpecificityAtSensitivity(
            sensitivity=efficiency,
            num_thresholds=num_thresholds,
            class_id=class_id,
            dtype=dtype,
        )

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true = ops.convert_to_tensor(y_true)
        y_pred = ops.convert_to_tensor(y_pred)

        if y_true.shape != y_pred.shape:
            n_classes = y_pred.shape[-1]
            y_true = ops.one_hot(ops.squeeze(y_true), n_classes, dtype="int32")

        self.specificity_at_sensitivity.update_state(y_true, y_pred, sample_weight)

    def result(self):
        fpr = ops.subtract(1, self.specificity_at_sensitivity.result())
        rejection = ops.divide(1, fpr)
        return rejection
