import unittest

import numpy as np
from keras import ops
from keras.config import epsilon
from sklearn.metrics import roc_curve

from hml.metrics import MaxSignificance
from hml.metrics.max_significance import calculate_thresholds


class TestMaxSignificance(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.y_true = np.append(np.random.choice([0, 1], (10,)), 0)
        self.y_prob = np.append(np.random.uniform(0, 1, (10,)), 0.0)

    def test_default(self):
        m = MaxSignificance()
        m.update_state(self.y_true, self.y_prob)

        assert m.result() == 1.8898223638534546
        assert m.selected_threshold == 0.5
        assert m.selected_tpr == 0.625
        assert m.selected_fpr == 0.6666666865348816
        assert len(m.significance) == 1

    def test_auto(self):
        m = MaxSignificance(thresholds="auto")
        m.update_state(self.y_true, self.y_prob)

        assert m.result() == 2.5298221111297607
        assert m.selected_threshold == 0.0
        assert m.selected_tpr == 1.0
        assert m.selected_fpr == 1.0
        assert len(m.significance) == 12

    def test_custom(self):
        m = MaxSignificance(thresholds=[0.1, 0.5, 0.9])
        m.update_state(self.y_true, self.y_prob)

        assert m.result() == 2.3333332538604736
        assert m.selected_threshold == 0.10000000149011612
        assert m.selected_tpr == 0.875
        assert m.selected_fpr == 0.6666666865348816
        assert len(m.significance) == 3

    def test_cross_sections(self):
        m = MaxSignificance(cross_sections=[100, 1])
        m.update_state(self.y_true, self.y_prob)

        assert m.result() == 0.07619024813175201
        assert m.selected_threshold == 0.5
        assert m.selected_tpr == 0.625
        assert m.selected_fpr == 0.6666666865348816
        assert len(m.significance) == 1


def test_calcualte_thresholds():
    np.random.seed(0)
    y_true = np.append(np.random.choice([0, 1], (10,)), 0)
    y_prob = np.append(np.random.uniform(0, 1, (10,)), 0.0)
    fpr, tpr, thresholds = roc_curve(y_true, y_prob, drop_intermediate=False)

    keras_thresholds = calculate_thresholds(y_prob)
    assert ops.all(thresholds[1:-1] == keras_thresholds[1:-1] + epsilon())
