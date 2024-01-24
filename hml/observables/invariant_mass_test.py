from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .invariant_mass import InvariantMass
from .invariant_mass import InvM
from .invariant_mass import InvMass


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = InvariantMass("Jet0,Jet1")

    assert obs.physics_object.identifier == "Jet0,Jet1"
    assert obs.supported_types == ["single", "multiple"]
    assert obs.name == "InvariantMass"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0,Jet1.InvariantMass"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0,Jet1.InvariantMass : nan"

    assert InvariantMass.from_identifier("Jet0,Jet1.InvariantMass").config == obs.config

    obs = InvMass("Jet0,Jet1")
    assert obs.name == "InvMass"
    assert obs.identifier == "Jet0,Jet1.InvMass"

    obs = InvM("Jet0,Jet1")
    assert obs.name == "InvM"
    assert obs.identifier == "Jet0,Jet1.InvM"


def test_read(event):
    obs = InvM("Jet0,Jet1").read(event)
    assert isinstance(obs.value, float)
    assert obs.shape == "1 * float64"

    obs = InvM("Jet0,Jet100").read(event)
    assert isinstance(obs.value, float)
    assert obs.shape == "1 * float64"
