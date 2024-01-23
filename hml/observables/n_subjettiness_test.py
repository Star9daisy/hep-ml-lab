from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .n_subjettiness import NSubjettiness
from .n_subjettiness import TauN


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = NSubjettiness(1, "FatJet0")

    assert obs.n == 1
    assert obs.physics_object.identifier == "FatJet0"
    assert obs.supported_types == ["single", "collective"]
    assert obs.name == "NSubjettiness"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "FatJet0.NSubjettiness"
    assert obs.config == {
        "n": 1,
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "FatJet0.NSubjettiness"

    assert (
        NSubjettiness.from_identifier("FatJet0.NSubjettiness", n=1).config == obs.config
    )

    obs = TauN(1, "FatJet0")
    assert obs.name == "Tau1"
    assert obs.identifier == "FatJet0.Tau1"


def test_read(event):
    obs = TauN(1, "FatJet0").read(event)
    assert isinstance(obs.value, float)
    assert obs.shape == "1 * float64"

    obs = TauN(1, "FatJet:5").read(event)
    assert isinstance(obs.value, list)
    assert obs.shape == "5 * float64"


def test_from_identifier():
    obs = TauN.from_identifier("FatJet0.Tau1")
    assert obs.n == 1

    with pytest.raises(ValueError):
        TauN.from_identifier("Tau1")
