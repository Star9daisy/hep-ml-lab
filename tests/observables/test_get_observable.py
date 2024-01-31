from hml.observables import get_observable


def test_get_observable():
    assert get_observable("Unknown") is None
    assert get_observable("Dummy") is not None
    assert get_observable("dummy") is not None
    assert get_observable("FatJet0.tau_21") is not None
    assert get_observable("FatJet0.tau21") is not None
    assert get_observable("FatJet0.tau1") is not None
    assert get_observable("FatJet0.tau2") is not None
    assert get_observable("Jet0.Pt") is not None
