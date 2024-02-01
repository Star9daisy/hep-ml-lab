import pytest

from hml.observables import get_observable
from hml.representations import Set


def test_init():
    # Only strings
    r = Set("FatJet0.Pt", "FatJet0.Eta", "FatJet0.Phi", "FatJet0.Mass")

    # Strings and observables
    r = Set("FatJet0.Pt", "FatJet0.Eta", "FatJet0.Phi", get_observable("FatJet0.Mass"))

    # Parameters ------------------------------------------------------------- #
    assert r.observables == [
        get_observable("FatJet0.Pt"),
        get_observable("FatJet0.Eta"),
        get_observable("FatJet0.Phi"),
        get_observable("FatJet0.Mass"),
    ]

    # Attributes ------------------------------------------------------------- #
    assert r.names == ["FatJet0.Pt", "FatJet0.Eta", "FatJet0.Phi", "FatJet0.Mass"]
    assert r.values is None


def test_read(event):
    r = Set("FatJet0.Pt", "FatJet0.Eta", "FatJet0.Phi", "FatJet0.Mass")
    r.read_ttree(event)

    assert r.values.shape == (4,)

    with pytest.raises(ValueError):
        r = Set("Jet:.Pt")
        r.read_ttree(event)
