from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .mass import M
from .mass import Mass


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = Mass("Jet0")

    assert obs.physics_object.identifier == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]
    assert obs.name == "Mass"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0.Mass"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0.Mass"

    assert Mass.from_identifier("Jet0.Mass").config == obs.config

    obs = M("Jet0")
    assert obs.name == "M"
    assert obs.identifier == "Jet0.M"


def test_read(event):
    obs = M("Jet0").read(event)
    assert isinstance(obs.value, float)
    assert obs.shape == "1 * float64"

    obs = M("Jet:5").read(event)
    assert isinstance(obs.value, list)
    assert obs.shape == "5 * float64"

    obs = M("Jet:2.Constituents:5").read(event)
    assert isinstance(obs.value, list)
    assert obs.shape == "2 * 5 * float64"
