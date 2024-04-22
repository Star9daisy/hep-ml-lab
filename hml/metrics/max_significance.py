from __future__ import annotations

from keras import ops
from keras.metrics import FalsePositives, Metric, TruePositives


class MaxSignificance(Metric):
    def __init__(
        self,
        thresholds=None,
        class_id=1,
        name="max_significance",
        dtype=None,
    ):
        super().__init__(name=name, dtype=dtype)
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


def max_significance(): ...
