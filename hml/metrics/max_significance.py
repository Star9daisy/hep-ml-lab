from __future__ import annotations

from keras import ops
from keras.metrics import (
    FalseNegatives,
    FalsePositives,
    Metric,
    TrueNegatives,
    TruePositives,
)


class MaxSignificance(Metric):
    def __init__(
        self,
        cross_sections=[1, 1],
        luminosity=1,
        weights=[1, 1],
        thresholds=None,
        class_id=1,
        name="max_significance",
        dtype=None,
    ):
        super().__init__(name=name, dtype=dtype)
        self.luminosity = luminosity

        self.cross_sections = cross_sections
        self.s_xsec = cross_sections.pop(class_id)
        self.b_xsec = cross_sections

        self.weights = weights
        self.s_weight = weights.pop(class_id)
        self.b_weight = weights

        self.class_id = class_id
        self.metric_tp = TruePositives(thresholds=thresholds, dtype=dtype)
        self.metric_fp = FalsePositives(thresholds=thresholds, dtype=dtype)
        self.metric_tn = TrueNegatives(thresholds=thresholds, dtype=dtype)
        self.metric_fn = FalseNegatives(thresholds=thresholds, dtype=dtype)

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_t_ndim = ops.ndim(ops.squeeze(y_true))
        y_p_ndim = ops.ndim(ops.squeeze(y_pred))

        y_true = ops.argmax(y_true, -1) if y_t_ndim == 2 else y_true
        y_pred = ops.take(y_pred, self.class_id, -1) if y_p_ndim == 2 else y_pred

        self.metric_tp.update_state(y_true, y_pred)
        self.metric_fp.update_state(y_true, y_pred)
        self.metric_tn.update_state(y_true, y_pred)
        self.metric_fn.update_state(y_true, y_pred)

    def result(self):
        if self.cross_sections == [1, 1]:
            s = self.metric_tp.result()
            b = self.metric_fp.result()

        else:
            tpr = self.metric_tp.result() / (
                self.metric_tp.result() + self.metric_fn.result()
            )
            fpr = self.metric_fp.result() / (
                self.metric_fp.result() + self.metric_tn.result()
            )

            s = self.s_xsec * self.luminosity * self.s_weight * tpr
            b = sum(
                [
                    xsec * self.luminosity * weight * fpr
                    for xsec, weight in zip(self.b_xsec, self.b_weight)
                ]
            )

        significance = ops.divide(s, ops.sqrt(s + b))
        max_significance = ops.max(significance)
        return max_significance


def max_significance(): ...
