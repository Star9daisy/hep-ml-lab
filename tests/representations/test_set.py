import pytest

from hml.observables import parse_observable
from hml.representations import Set


def test_init():
    r = Set(
        [
            "FatJet0.Mass",
            parse_observable("FatJet0.TauMN", m=2, n=1),
            "Jet0,Jet1.DeltaR",
        ]
    )

    # Attributes ------------------------------------------------------------- #
    assert r.observables == [
        parse_observable("FatJet0.Mass"),
        parse_observable("FatJet0.TauMN", m=2, n=1),
        parse_observable("Jet0,Jet1.DeltaR"),
    ]
    assert r.names == ["FatJet0.Mass", "FatJet0.TauMN", "Jet0,Jet1.DeltaR"]
    assert r.values is None
    assert r.config == {
        "observable_configs": {
            0: {
                "class_name": "M",
                "config": {"physics_object": "FatJet0", "class_name": "Mass"},
            },
            1: {
                "class_name": "TauMN",
                "config": {
                    "class_name": "TauMN",
                    "physics_object": "FatJet0",
                    "m": 2,
                    "n": 1,
                },
            },
            2: {
                "class_name": "AngularDistance",
                "config": {"physics_object": "Jet0,Jet1", "class_name": "DeltaR"},
            },
        }
    }


def test_read(events):
    # Common cases ----------------------------------------------------------- #
    r = Set(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"]).read(events)

    assert str(r.values.type) == "100 * 3 * ?float32"

    # Error cases ------------------------------------------------------------ #
    with pytest.raises(ValueError):
        Set(["Jet:.Pt"]).read(events)


def test_class_methods():
    r = Set(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"])

    assert Set.from_config(r.config).config == r.config
