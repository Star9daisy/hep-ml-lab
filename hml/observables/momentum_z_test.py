from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .momentum_z import MomentumZ
from .momentum_z import Pz


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = MomentumZ("Jet0")

    assert obs.physics_object.identifier == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]
    assert obs.name == "MomentumZ"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0.MomentumZ"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0.MomentumZ"

    assert MomentumZ.from_identifier("Jet0.MomentumZ").config == obs.config

    obs = Pz("Jet0")
    assert obs.name == "Pz"
    assert obs.identifier == "Jet0.Pz"


def test_read(event):
    obs = Pz("Jet0").read(event)
    assert isinstance(obs.value, float)
    assert obs.shape == "1 * float64"

    obs = Pz("Jet:5").read(event)
    assert isinstance(obs.value, list)
    assert obs.shape == "5 * float64"

    obs = Pz("Jet:2.Constituents:5").read(event)
    assert isinstance(obs.value, list)
    assert obs.shape == "2 * 5 * float64"
