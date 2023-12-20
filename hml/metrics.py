from __future__ import annotations

from keras import ops
from keras.metrics import (
    FalsePositives,
    Metric,
    Precision,
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
        y_t_ndim = ops.ndim(ops.squeeze(y_true))
        y_p_ndim = ops.ndim(ops.squeeze(y_pred))

        y_true = ops.argmax(y_true, -1) if y_t_ndim == 2 else y_true
        y_pred = ops.take(y_pred, self.class_id, -1) if y_p_ndim == 2 else y_pred

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
        if ops.shape(y_true) != ops.shape(y_pred):
            n_classes = ops.shape(y_pred)[-1]
            y_true = ops.one_hot(ops.squeeze(y_true), n_classes, dtype="int32")

        self.specificity_at_sensitivity.update_state(y_true, y_pred, sample_weight)

    def result(self):
        fpr = ops.subtract(1, self.specificity_at_sensitivity.result())
        rejection = ops.divide(1, fpr)
        return rejection
