import awkward as ak
import pytest

from hml.observables import TauMN, TauN


def test_init():
    obs = TauN(n=1, physics_object="jet0")

    assert obs.physics_object.name == "jet0"
    assert obs.class_name == "TauN"

    assert obs.name == "jet0.TauN"
    assert len(obs.value) == 0
    assert obs.config == {"n": 1, "physics_object": "jet0", "class_name": "TauN"}

    # Other init
    assert TauMN(2, 1, physics_object="jet0").name == "jet0.TauMN"

    with pytest.raises(ValueError):
        TauN(n=1, physics_object="jet0.constituents")


def test_class_methods():
    obs = TauN(n=1, physics_object="jet0")

    assert TauN.from_name("jet0.tau1").name == "jet0.tau1"
    assert TauN.from_config(obs.config).name == "jet0.TauN"

    obs = TauMN(2, 1, physics_object="jet0")

    assert TauMN.from_name("jet0.tau21").name == "jet0.tau21"
    assert TauMN.from_config(obs.config).name == "jet0.TauMN"


def test_read(events):
    cut = events["FatJet_size"].array() > 0

    obs = TauN(n=1, physics_object="fatjet0").read(events)
    assert ak.all(obs.value[cut][:, 0] == events["FatJet.Tau[5]"].array()[cut][:, 0, 0])
    assert str(obs.value.type) == f"{len(obs.value)} * 1 * ?float32"

    obs = TauN(n=1, physics_object="fatjet").read(events)
    assert str(obs.value.type) == f"{len(obs.value)} * var * float32"

    obs = TauN(n=1, physics_object="fatjet:10").read(events)
    assert str(obs.value.type) == f"{len(obs.value)} * 10 * ?float32"

    with pytest.raises(ValueError):
        TauN(n=1, physics_object="unknown").read(events)

    obs = TauMN(m=2, n=1, physics_object="fatjet0").read(events)
    assert ak.all(
        TauN(2, physics_object="fatjet0").read(events).value
        / TauN(1, physics_object="fatjet0").read(events).value
        == obs.value
    )
