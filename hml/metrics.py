from __future__ import annotations

import tensorflow as tf
from keras.metrics import Metric


class MaxSignificance(Metric):
    """Calculate the maximum significance of a model's predictions."""

    def __init__(
        self,
        thresholds: float | list | tuple = 0.5,
        class_id: int = 1,
        name: str = "max_significance",
        dtype=None,
    ):
        super().__init__(name=name, dtype=dtype)

        if isinstance(thresholds, (list, tuple)):
            self.thresholds = thresholds
        else:
            self.thresholds = [thresholds]

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
