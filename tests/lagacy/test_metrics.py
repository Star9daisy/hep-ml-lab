from keras import ops

from hml.metrics import MaxSignificance, RejectionAtEfficiency


def test_max_significance():
    # Standard case
    y_true = [0, 1, 1, 1]
    y_pred = [1, 0, 1, 1]
    assert MaxSignificance()(y_true, y_pred) == ops.divide(2.0, ops.sqrt(2.0 + 1.0))

    # Binary case
    y_true = [[0], [1], [1], [1]]
    y_pred = [[0.98], [0], [0.8], [0.6]]
    assert MaxSignificance()(y_true, y_pred) == ops.divide(2.0, ops.sqrt(2.0 + 1.0))

    # Categorical case
    y_true = [[1, 0], [0, 1], [0, 1], [0, 1]]
    y_pred = [[0.02, 0.98], [1.0, 0.0], [0.2, 0.8], [0.4, 0.6]]
    assert MaxSignificance()(y_true, y_pred) == ops.divide(2.0, ops.sqrt(2.0 + 1.0))

    # Sparse categorical case
    y_true = [[0], [1], [1], [1]]
    y_pred = [[0.02, 0.98], [1.0, 0.0], [0.2, 0.8], [0.4, 0.6]]
    assert MaxSignificance()(y_true, y_pred) == ops.divide(2.0, ops.sqrt(2.0 + 1.0))


def test_max_significance_edge_cases():
    # All true positives ----------------------------------------------------- #
    y_true, y_pred = [1, 1, 1, 1], [1, 1, 1, 1]
    assert MaxSignificance()(y_true, y_pred) == 2

    # All false positives ---------------------------------------------------- #
    y_true, y_pred = [0, 0, 0, 0], [1, 1, 1, 1]
    assert MaxSignificance()(y_true, y_pred) == 0

    # No positives ----------------------------------------------------------- #
    y_true, y_pred = [0, 0, 0, 0], [0, 0, 0, 0]
    assert ops.isnan(MaxSignificance()(y_true, y_pred))


def test_rejection_at_efficiency():
    # Binary case ------------------------------------------------------------ #
    y_true = [0, 0, 0, 1, 1]
    y_pred = [1.0, 0.0, 0.0, 1.0, 1.0]
    assert RejectionAtEfficiency(0.5)(y_true, y_pred) == 3.0000002

    # Categorical case ------------------------------------------------------- #
    y_true = [[1, 0], [1, 0], [1, 0], [0, 1], [0, 1]]
    y_pred = [[0.02, 0.98], [1.0, 0.0], [1.0, 0.0], [0.2, 0.8], [0.4, 0.6]]
    assert RejectionAtEfficiency(0.5, class_id=1)(y_true, y_pred) == 3.0000002

    # Sparse categorical case ------------------------------------------------ #
    y_true = [0, 0, 0, 1, 1]
    y_pred = [[0.02, 0.98], [1.0, 0.0], [1.0, 0.0], [0.2, 0.8], [0.4, 0.6]]
    assert RejectionAtEfficiency(0.5, class_id=1)(y_true, y_pred) == 3.0000002


def test_rejection_at_efficiency_edge_cases():
    # Negatives are all true ------------------------------------------------- #
    y_true, y_pred = [0, 0, 1, 1], [0, 0, 1, 1]
    assert ops.isinf(RejectionAtEfficiency(0.5)(y_true, y_pred))
