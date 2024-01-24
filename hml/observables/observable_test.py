from math import isnan

import awkward as ak
import numpy as np
import pytest

from ..events.delphes_events import DelphesEvents
from . import get
from .observable import Observable


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_only_value():
    # Pretend to have overwritten the read method.
    obs = Observable()
    obs._value = 100

    # attributes
    assert obs.physics_object is None
    assert obs.supported_types is None

    assert obs.name == "Observable"
    assert obs.value == 100
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Observable"
    assert obs.config == {
        "physics_object": None,
        "name": "Observable",
        "value": 100,
        "dtype": "float64",
    }
    assert repr(obs) == "Observable"

    # class methods
    assert Observable.from_identifier("Observable", value=100).config == obs.config
    assert (
        Observable.from_config(
            {
                "physics_object": None,
                "name": "Observable",
                "value": 100,
                "dtype": "float64",
            }
        ).config
        == obs.config
    )

    # Conversion to other format
    assert obs.to_awkward() == ak.Array([100])
    assert obs.to_numpy() == np.array([100])


def test_with_name():
    obs = Observable(name="MyObservable")
    assert obs.name == "MyObservable"
    assert isnan(obs.value)
    assert obs.identifier == "MyObservable"


def test_with_physics_object():
    obs = Observable("Jet:")
    assert obs.physics_object.identifier == "Jet:"
    assert obs.identifier == "Jet:.Observable"

    obs = Observable.from_identifier("Jet:.Observable")
    assert obs.physics_object.identifier == "Jet:"
    assert obs.identifier == "Jet:.Observable"


def test_with_supported_types():
    Observable("Jet:", supported_types=["collective"])

    with pytest.raises(ValueError):
        Observable("Jet0", supported_types=[])
    with pytest.raises(ValueError):
        Observable("Jet0", supported_types=["collective"])
    with pytest.raises(ValueError):
        Observable("Jet0", supported_types=["multiple"])
    with pytest.raises(ValueError):
        Observable("Jet0", supported_types=["single", "multiple"])


def test_get():
    assert get("Unknown") is None
    assert get("Dummy") is not None
    assert get("dummy") is not None
    assert get("FatJet0.tau_21") is not None
    assert get("FatJet0.tau21") is not None
    assert get("FatJet0.tau1") is not None
    assert get("FatJet0.tau2") is not None
    assert get("Jet0.Pt") is not None
