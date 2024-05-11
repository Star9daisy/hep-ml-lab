import unittest

import numpy as np

from hml.metrics import RejectionAtEfficiency


class TestRejectionAtEfficiency(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.y_true = np.append(np.random.choice([0, 1], (10,)), 0)
        y_pred = np.append(np.random.uniform(0, 1, (10,)), 0.0)
        self.y_pred = np.stack([1 - y_pred, y_pred], axis=1)

    def test_class_id(self):
        # Default class_id
        m = RejectionAtEfficiency(efficiency=0.5)
        m.update_state(self.y_true, self.y_pred)

        assert m.result() == 2.2

        # class_id=1
        m = RejectionAtEfficiency(efficiency=0.5, class_id=1)
        m.update_state(self.y_true, self.y_pred)

        assert m.result() == 1.5000001

        # class_id=0
        m = RejectionAtEfficiency(efficiency=0.5, class_id=0)
        m.update_state(self.y_true, self.y_pred)

        assert m.result() == 1.6
