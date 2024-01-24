from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .angular_distance import AngularDistance
from .angular_distance import DeltaR


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = AngularDistance("Jet0,Jet1")

    assert obs.physics_object.identifier == "Jet0,Jet1"
    assert obs.supported_types == ["single", "collective", "nested", "multiple"]
    assert obs.name == "AngularDistance"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0,Jet1.AngularDistance"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0,Jet1.AngularDistance : nan"

    assert (
        AngularDistance.from_identifier("Jet0,Jet1.AngularDistance").config
        == obs.config
    )

    obs = DeltaR("Jet0,Jet1")
    assert obs.name == "DeltaR"
    assert obs.identifier == "Jet0,Jet1.DeltaR"

    with pytest.raises(ValueError):
        AngularDistance("Jet0,Jet1,Jet2")


def test_read(event):
    assert DeltaR("Jet100,Jet1").read(event).shape == "1 * 1 * float64"
    assert DeltaR("Jet0,Jet100").read(event).shape == "1 * 1 * float64"

    # (0, v) -> 0
    assert DeltaR("Jet100:,Jet1").read(event).shape == "0 * unknown"
    assert DeltaR("Jet100.Constituents:,Jet1").read(event).shape == "0 * unknown"
    assert DeltaR("Jet100:.Constituents:,Jet1").read(event).shape == "0 * unknown"
    assert DeltaR("Jet0.Constituents100,Jet1").read(event).shape == "0 * unknown"
    assert DeltaR("Jet0.Constituents100:,Jet1").read(event).shape == "0 * unknown"

    # (v, v) -> (v, v)
    assert DeltaR("Jet0,Jet100:").read(event).shape == "1 * 0 * unknown"
    assert DeltaR("Jet0,Jet100.Constituents:").read(event).shape == "1 * 0 * unknown"
    assert DeltaR("Jet0,Jet100:.Constituents:").read(event).shape == "1 * 0 * unknown"
    assert DeltaR("Jet0,Jet1.Constituents100").read(event).shape == "1 * 0 * unknown"
    assert DeltaR("Jet0,Jet1.Constituents100:").read(event).shape == "1 * 0 * unknown"
    assert DeltaR("Jet0,Jet1").read(event).shape == "1 * 1 * float64"
    assert DeltaR("Jet:5,Jet:5").read(event).shape == "5 * 5 * float64"
    assert (
        DeltaR("Jet:5.Constituents:100,Jet:5.Constituents:100").read(event).shape
        == "500 * 500 * float64"
    )
