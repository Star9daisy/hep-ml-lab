from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .n_subjettiness import NSubjettiness
from .n_subjettiness import TauN


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_n_subjettiness(event):
    obs = NSubjettiness(n=1, physics_object="FatJet0")
    assert obs.n == 1
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "NSubjettiness"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.NSubjettiness"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "NSubjettiness"
    assert obs.config == {
        "n": 1,
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert NSubjettiness.from_name("FatJet0.NSubjettiness", 1).fullname == obs.fullname
    assert NSubjettiness.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = NSubjettiness(n=1, physics_object="FatJet:5")
    assert obs.n == 1
    assert obs.physics_object.name == "FatJet:5"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "NSubjettiness"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet:5.NSubjettiness"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "NSubjettiness"
    assert obs.physics_object.name == "FatJet:5"
    assert obs.config == {
        "n": 1,
        "physics_object": "FatJet:5",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert NSubjettiness.from_name("FatJet:5.NSubjettiness", 1).fullname == obs.fullname
    assert NSubjettiness.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert len(obs.value) == 5


def test_tau_n(event):
    obs = TauN(n=1, physics_object="FatJet0")
    assert obs.n == 1
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "Tau1"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Tau1"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "TauN"
    assert obs.config == {
        "n": 1,
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert TauN.from_name("FatJet0.Tau1").fullname == obs.fullname
    assert TauN.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = TauN(n=1, physics_object="FatJet:5")
    assert obs.n == 1
    assert obs.physics_object.name == "FatJet:5"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "Tau1"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet:5.Tau1"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "TauN"
    assert obs.physics_object.name == "FatJet:5"
    assert obs.config == {
        "n": 1,
        "physics_object": "FatJet:5",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert TauN.from_name("FatJet:5.Tau1").fullname == obs.fullname
    assert TauN.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert len(obs.value) == 5


def test_bad_cases(event):
    assert isnan(TauN(n=1, physics_object="Jet100").read(event).value)
    assert len(TauN(n=1, physics_object="Jet100:").read(event).value) == 0

    with pytest.raises(TypeError):
        TauN.from_name("Tau1")
