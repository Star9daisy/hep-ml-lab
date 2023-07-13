from numpy.testing import assert_almost_equal


def test_max_significance():
    from hml.metrics import MaxSignificance

    m = MaxSignificance()
    m.update_state([0, 0, 1], [[0.8, 0.2], [0.3, 0.7], [0.4, 0.6]])
    assert_almost_equal(m.result().numpy(), 1.0)


def test_rejection_at_efficiency():
    from hml.metrics import RejectionAtEfficiency

    m = RejectionAtEfficiency()
    m.update_state(
        [[1, 0], [1, 0], [1, 0], [0, 1], [0, 1]],
        [[1, 0], [0.7, 0.3], [0.2, 0.8], [0.7, 0.3], [0.2, 0.8]],
    )
    assert_almost_equal(m.result().numpy(), 2.9999993)
