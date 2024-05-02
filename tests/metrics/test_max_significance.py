import keras
import numpy as np
from keras import ops
from keras.metrics import FalseNegatives, FalsePositives, TrueNegatives, TruePositives
from keras.ops import convert_to_numpy
from sklearn.metrics import roc_curve

from hml.metrics.max_significance import calculate_thresholds


def test_thresholds():
    np.random.seed(0)
    y_true = np.append(np.random.choice([0, 1], (10,)), 0)
    y_prob = np.append(np.random.uniform(0, 1, (10,)), 0.0)

    fpr, tpr, thresholds = roc_curve(y_true, y_prob, drop_intermediate=False)

    keras_thresholds = calculate_thresholds(y_prob)

    valid_y_prob = ops.where(y_prob > 0, y_prob, keras.config.epsilon())

    m_tp = TruePositives(keras_thresholds.numpy().tolist())
    m_fn = FalseNegatives(keras_thresholds.numpy().tolist())
    m_tn = TrueNegatives(keras_thresholds.numpy().tolist())
    m_fp = FalsePositives(keras_thresholds.numpy().tolist())

    tp = convert_to_numpy(m_tp(y_true, valid_y_prob))
    fn = convert_to_numpy(m_fn(y_true, valid_y_prob))
    tn = convert_to_numpy(m_tn(y_true, valid_y_prob))
    fp = convert_to_numpy(m_fp(y_true, valid_y_prob))

    hml_tpr = tp / (tp + fn)
    hml_fpr = fp / (fp + tn)

    np.testing.assert_allclose(tpr, hml_tpr)
    np.testing.assert_allclose(fpr, hml_fpr)
    np.testing.assert_allclose(thresholds[1:], keras_thresholds[1:], rtol=1e-5)
