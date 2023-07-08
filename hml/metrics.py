from __future__ import annotations

import tensorflow as tf
from keras.metrics import Metric, SpecificityAtSensitivity


class MaxSignificance(Metric):
    """Calculate the maximum significance of a model's predictions."""

    def __init__(
        self,
        n_thresholds: int = 201,
        class_id: int = 1,
        name: str = "max_significance",
        dtype=None,
    ):
        super().__init__(name=name, dtype=dtype)

        # Compute thresholds in [0, 1] range
        if n_thresholds == 1:
            self.thresholds = [0.5]
        else:
            thresholds = [i / (n_thresholds - 1) for i in range(n_thresholds - 1)]
            self.thresholds = [0.0] + thresholds + [1.0]

        self.class_id = class_id
        self.true_positives = [
            self.add_weight(name=f"tp_{i}", initializer="zeros")
            for i, _ in enumerate(self.thresholds)
        ]
        self.false_positives = [
            self.add_weight(name=f"fp_{i}", initializer="zeros")
            for i, _ in enumerate(self.thresholds)
        ]

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_true_signal = y_true[:, self.class_id]
        y_pred_signal = y_pred[:, self.class_id]
        for i, threshold in enumerate(self.thresholds):
            y_pred_thresholded = tf.cast(tf.greater_equal(y_pred_signal, threshold), tf.float32)
            if sample_weight is not None:
                self.true_positives[i].assign_add(
                    tf.reduce_sum(y_true_signal * y_pred_thresholded) * sample_weight
                )
                self.false_positives[i].assign_add(
                    tf.reduce_sum((1 - y_true_signal) * y_pred_thresholded) * sample_weight
                )
            else:
                self.true_positives[i].assign_add(tf.reduce_sum(y_true_signal * y_pred_thresholded))
                self.false_positives[i].assign_add(
                    tf.reduce_sum((1 - y_true_signal) * y_pred_thresholded)
                )

    def result(self):
        significances = [
            tp / tf.sqrt(fp + tf.keras.backend.epsilon())
            for tp, fp in zip(self.true_positives, self.false_positives)
        ]
        self.max_significance_threshold_index = tf.argmax(significances)
        self.max_significance_threshold = tf.convert_to_tensor(self.thresholds)[
            self.max_significance_threshold_index
        ]
        return tf.reduce_max(significances)

    def reset_state(self):
        # The state of the metric will be reset at the start of each epoch.
        for i in range(len(self.thresholds)):
            self.true_positives[i].assign(0.0)
            self.false_positives[i].assign(0.0)


class RejectionAtEfficiency(Metric):
    def __init__(
        self,
        efficiency: float,
        num_thresholds: int = 200,
        class_id: int = 1,
        name: str = "rejection_at_efficiency",
        dtype=None,
    ):
        super().__init__(
            name=name,
            dtype=dtype,
        )
        self.specificity_at_sensitivity = SpecificityAtSensitivity(
            sensitivity=efficiency,
            num_thresholds=num_thresholds,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.specificity_at_sensitivity.update_state(y_true, y_pred, sample_weight)

    def result(self):
        specificity = 1 - self.specificity_at_sensitivity.result()
        rejection = 1 / (specificity + tf.keras.backend.epsilon())
        return rejection

    def reset_state(self):
        self.specificity_at_sensitivity.reset_states()
