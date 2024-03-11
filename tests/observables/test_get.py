from hml.observables import AngularDistance, InvariantMass, Pt, get


def test_get():
    assert get("Pt") is Pt
    assert get("AngularDistance") is AngularDistance
    assert get("InvariantMass") is InvariantMass
    assert get(None) is None
