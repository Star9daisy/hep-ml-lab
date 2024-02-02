import pytest

from hml.observables import get_observable
from hml.representations import Set


def test_init():
    r = Set(
        "FatJet0.Mass",
        get_observable("FatJet0.TauMN", m=2, n=1),
        "Jet0,Jet1.DeltaR",
    )

    # Attributes ------------------------------------------------------------- #
    assert r.observables == [
        get_observable("FatJet0.Mass"),
        get_observable("FatJet0.TauMN", m=2, n=1),
        get_observable("Jet0,Jet1.DeltaR"),
    ]
    assert r.names == ["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"]
    assert r.values is None
    assert r.config == {
        "observable_configs": {
            "Mass": {"physics_object": "FatJet0"},
            "TauMN": {"physics_object": "FatJet0", "m": 2, "n": 1},
            "DeltaR": {"physics_object": "Jet0,Jet1"},
        }
    }


def test_read_ttree(event):
    # Common cases ----------------------------------------------------------- #
    r = Set("FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR").read_ttree(event)

    assert r.values.shape == (3,)

    # Error cases ------------------------------------------------------------ #
    with pytest.raises(ValueError):
        Set("Jet:.Pt").read_ttree(event)


def test_class_methods():
    r = Set("FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR")

    assert Set.from_config(r.config).config == r.config
