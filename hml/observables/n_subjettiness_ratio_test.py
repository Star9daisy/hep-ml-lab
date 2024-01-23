from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .n_subjettiness_ratio import NSubjettinessRatio
from .n_subjettiness_ratio import TauMN


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_n_subjettiness(event):
    obs = NSubjettinessRatio(2, 1, "FatJet0")

    assert obs.m == 2
    assert obs.n == 1
    assert obs.physics_object.identifier == "FatJet0"
    assert obs.supported_types == ["single", "collective"]
    assert obs.name == "NSubjettinessRatio"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "FatJet0.NSubjettinessRatio"
    assert obs.config == {
        "m": 2,
        "n": 1,
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "FatJet0.NSubjettinessRatio"

    assert (
        NSubjettinessRatio.from_identifier(
            "FatJet0.NSubjettinessRatio", m=2, n=1
        ).config
        == obs.config
    )

    obs = TauMN(2, 1, "FatJet0")
    assert obs.name == "Tau21"
    assert obs.identifier == "FatJet0.Tau21"


def test_read(event):
    obs = TauMN(2, 1, "FatJet0").read(event)
    assert isinstance(obs.value, float)
    assert obs.shape == "1 * float64"

    obs = TauMN(2, 1, "FatJet:5").read(event)
    assert isinstance(obs.value, list)
    assert obs.shape == "5 * float64"


def test_from_identifier():
    obs = TauMN.from_identifier("FatJet0.Tau21")
    assert obs.m == 2
    assert obs.n == 1

    with pytest.raises(ValueError):
        TauMN.from_identifier("Tau21")
