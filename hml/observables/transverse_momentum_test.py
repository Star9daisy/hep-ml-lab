from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .transverse_momentum import Pt
from .transverse_momentum import TransverseMomentum


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = TransverseMomentum("Jet0")

    assert obs.physics_object.identifier == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]
    assert obs.name == "TransverseMomentum"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0.TransverseMomentum"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0.TransverseMomentum"

    assert (
        TransverseMomentum.from_identifier("Jet0.TransverseMomentum").config
        == obs.config
    )

    obs = Pt("Jet0")
    assert obs.name == "Pt"
    assert obs.identifier == "Jet0.Pt"


def test_read(event):
    obs = Pt("Jet0").read(event)
    assert obs.shape == "1 * float64"

    obs = Pt("Jet:5").read(event)
    assert obs.shape == "5 * float64"

    obs = Pt("Jet:2.Constituents:5").read(event)
    assert obs.shape == "2 * 5 * float64"
