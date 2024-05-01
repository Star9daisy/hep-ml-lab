from __future__ import annotations

from keras import ops
from keras.config import epsilon
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
        cross_sections=None,
        luminosity=None,
        weights=None,
        thresholds=None,
        class_id=1,
        name="max_significance",
        dtype=None,
    ):
        super().__init__(name=name, dtype=dtype)
        self.luminosity = luminosity if luminosity is not None else 1.0

        cross_sections = cross_sections.copy() if cross_sections is not None else [1, 1]
        self.cross_sections = cross_sections
        self.s_xsec = cross_sections.pop(class_id)
        self.b_xsec = cross_sections

        weights = weights.copy() if weights is not None else [1, 1]
        self.weights = weights
        self.s_weight = weights.pop(class_id)
        self.b_weight = weights

        self.class_id = class_id

        if thresholds is None:
            self.thresholds = [0.5]
        elif thresholds == "auto":
            self.thresholds = thresholds
        else:
            self.thresholds = thresholds

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_t_ndim = ops.ndim(ops.squeeze(y_true))
        y_p_ndim = ops.ndim(ops.squeeze(y_pred))

        y_true = ops.argmax(y_true, -1) if y_t_ndim == 2 else y_true
        y_pred = ops.take(y_pred, self.class_id, -1) if y_p_ndim == 2 else y_pred
        valid_y_pred = ops.where(y_pred > 0, y_pred, epsilon())

        if self.thresholds == "auto":
            self.thresholds = calculate_thresholds(y_pred).numpy().tolist()

        self.metric_tp = TruePositives(thresholds=self.thresholds, dtype=self.dtype)
        self.metric_fp = FalsePositives(thresholds=self.thresholds, dtype=self.dtype)
        self.metric_tn = TrueNegatives(thresholds=self.thresholds, dtype=self.dtype)
        self.metric_fn = FalseNegatives(thresholds=self.thresholds, dtype=self.dtype)

        self.metric_tp.update_state(y_true, valid_y_pred)
        self.metric_fp.update_state(y_true, valid_y_pred)
        self.metric_tn.update_state(y_true, valid_y_pred)
        self.metric_fn.update_state(y_true, valid_y_pred)

    def result(self):
        tp = self.metric_tp.result()
        fn = self.metric_fn.result()
        tn = self.metric_tn.result()
        fp = self.metric_fp.result()
        tpr = tp / (tp + fn)
        fpr = fp / (fp + tn)

        if self.cross_sections == [1, 1]:
            s = tp
            b = fp
        else:
            if self.thresholds != [0.5]:
                selection = fpr != 0
                tpr = tpr[selection]
                fpr = fpr[selection]
                thresholds = ops.convert_to_tensor(self.thresholds)[selection]
            else:
                thresholds = ops.convert_to_tensor(self.thresholds)

            s = self.s_xsec * self.luminosity * self.s_weight * tpr
            b = sum(
                [
                    xsec * self.luminosity * weight * fpr
                    for xsec, weight in zip(self.b_xsec, self.b_weight)
                ]
            )

        significance = ops.divide(s, ops.sqrt(s + b))
        self.significance = significance
        max_index = ops.argmax(significance)

        if self.thresholds != [0.5]:
            self.selected_tpr = tpr[max_index]
            self.selected_fpr = fpr[max_index]
            self.selected_threshold = thresholds[max_index]
            max_significance = significance[max_index]
        else:
            self.selected_tpr = tpr
            self.selected_fpr = fpr
            self.selected_threshold = self.thresholds
            max_significance = significance

        return max_significance


def max_significance(): ...


def calculate_thresholds(y_score):
    # Ensure y_score is a one-dimensional array
    y_score = ops.convert_to_tensor(y_score)
    assert ops.ndim(y_score) == 1

    # Sort scores in descending order
    desc_score_indices = ops.argsort(y_score)[::-1]
    y_score_sorted = ops.take(y_score, desc_score_indices)

    # Find indices where the score value changes
    distinct_value_indices = ops.where(ops.diff(y_score_sorted))[0]

    # Append the last index to capture the threshold for the smallest score
    threshold_idxs = ops.append(distinct_value_indices, ops.size(y_score) - 1)

    # Return the scores at the threshold indices
    thresholds = ops.append(1, ops.take(y_score_sorted, threshold_idxs))
    thresholds = ops.clip(thresholds - epsilon(), 0, 1)
    return thresholds
