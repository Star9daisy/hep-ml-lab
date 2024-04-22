from __future__ import annotations

from keras import ops
from keras.metrics import Metric, SpecificityAtSensitivity


class RejectionAtEfficiency(Metric):
    def __init__(
        self,
        efficiency,
        num_thresholds=200,
        class_id=None,
        name="rejection_at_efficiency",
        dtype=None,
    ):
        super().__init__(name=name, dtype=dtype)
        self.specificity_at_sensitivity = SpecificityAtSensitivity(
            sensitivity=efficiency,
            num_thresholds=num_thresholds,
            class_id=class_id,
            dtype=dtype,
        )

    def update_state(self, y_true, y_pred, sample_weight=None):
        if ops.shape(y_true) != ops.shape(y_pred):  # -> not allowed in non-eager mode
            n_classes = ops.shape(y_pred)[-1]
            y_true = ops.one_hot(ops.squeeze(y_true), n_classes, dtype="int32")

        self.specificity_at_sensitivity.update_state(y_true, y_pred, sample_weight)

    def result(self):
        fpr = ops.subtract(
            1, self.specificity_at_sensitivity.result()
        )  # -> not allowed in non-eager mode
        rejection = ops.divide(1, fpr)
        return rejection


def rejection_at_efficiency(): ...
