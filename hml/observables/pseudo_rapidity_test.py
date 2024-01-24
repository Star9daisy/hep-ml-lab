from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .pseudo_rapidity import Eta
from .pseudo_rapidity import PseudoRapidity


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = PseudoRapidity("Jet0")

    assert obs.physics_object.identifier == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]
    assert obs.name == "PseudoRapidity"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0.PseudoRapidity"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0.PseudoRapidity : nan"

    assert PseudoRapidity.from_identifier("Jet0.PseudoRapidity").config == obs.config

    obs = Eta("Jet0")
    assert obs.name == "Eta"
    assert obs.identifier == "Jet0.Eta"


def test_read(event):
    obs = Eta("Jet0").read(event)
    assert obs.shape == "1 * float64"

    obs = Eta("Jet:5").read(event)
    assert obs.shape == "5 * float64"

    obs = Eta("Jet:2.Constituents:5").read(event)
    assert obs.shape == "2 * 5 * float64"
