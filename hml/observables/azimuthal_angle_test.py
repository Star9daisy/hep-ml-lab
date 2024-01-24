from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .azimuthal_angle import AzimuthalAngle
from .azimuthal_angle import Phi


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = AzimuthalAngle("Jet0")

    assert obs.physics_object.identifier == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]
    assert obs.name == "AzimuthalAngle"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0.AzimuthalAngle"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0.AzimuthalAngle"

    assert AzimuthalAngle.from_identifier("Jet0.AzimuthalAngle").config == obs.config

    obs = Phi("Jet0")
    assert obs.name == "Phi"
    assert obs.identifier == "Jet0.Phi"


def test_read(event):
    obs = Phi("Jet0").read(event)
    assert obs.shape == "1 * float64"

    obs = Phi("Jet:5").read(event)
    assert obs.shape == "5 * float64"

    obs = Phi("Jet:2.Constituents:5").read(event)
    assert obs.shape == "2 * 5 * float64"
