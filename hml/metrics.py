from __future__ import annotations

import tensorflow as tf
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

    def update_state(self, y_true, y_pred, sample_weight=None):  # pragma: no cover
        y_true = tf.convert_to_tensor(y_true)
        y_pred = tf.convert_to_tensor(y_pred)

        if tf.rank(y_true) == 2 and tf.shape(y_true)[-1] > 1:
            y_true = tf.gather(y_true, self.class_id, axis=-1)

        if tf.rank(y_pred) == 2 and tf.shape(y_pred)[-1] > 1:
            y_pred = tf.gather(y_pred, self.class_id, axis=-1)

        self.tp.update_state(y_true, y_pred, sample_weight)
        self.fp.update_state(y_true, y_pred, sample_weight)

    def result(self):  # pragma: no cover
        s = self.tp.result()
        b = self.fp.result()
        significance = s / tf.sqrt(s + b)
        max_significance = tf.reduce_max(significance)
        return max_significance

    def reset_state(self):  # pragma: no cover
        self.tp.reset_state()
        self.fp.reset_state()


class RejectionAtEfficiency(Metric):
    def __init__(
        self,
        efficiency,
        num_thresholds=200,
        class_id=None,
        name=None,
        dtype=None,
    ):
        super().__init__(name, dtype)
        self.specificity_at_sensitivity = SpecificityAtSensitivity(
            sensitivity=efficiency,
            num_thresholds=num_thresholds,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )

    def update_state(self, y_true, y_pred, sample_weight=None):  # pragma: no cover
        y_true = tf.convert_to_tensor(y_true)
        y_pred = tf.convert_to_tensor(y_pred)

        if y_true.shape != y_pred.shape:
            n_classes = y_pred.shape[-1]
            y_true = tf.one_hot(tf.squeeze(y_true), n_classes, dtype=tf.int32)

        self.specificity_at_sensitivity.update_state(y_true, y_pred, sample_weight)

    def result(self):  # pragma: no cover
        fpr = 1 - self.specificity_at_sensitivity.result()
        rejection = 1 / fpr
        return rejection

    def reset_state(self):  # pragma: no cover
        self.specificity_at_sensitivity.reset_state()
