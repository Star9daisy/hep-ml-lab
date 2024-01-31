from math import isnan

import pytest

from hml.observables.n_subjettiness import NSubjettiness
from hml.observables.n_subjettiness import TauN


def test_init():
    obs = NSubjettiness(physics_object="FatJet0", n=1)

    # Parameters ------------------------------------------------------------- #
    assert obs.n == 1
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_types == ["single", "collective"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "FatJet0.NSubjettiness"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"n": 1, "physics_object": obs.physics_object.name}
    assert repr(obs) == "FatJet0.NSubjettiness : nan"

    obs = TauN(physics_object="FatJet0", n=1)

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "FatJet0.Tau1"


def test_class_methods():
    obs = NSubjettiness(physics_object="FatJet0", n=1)
    assert obs == NSubjettiness.from_name("FatJet0.NSubjettiness", n=1)
    assert obs == NSubjettiness.from_config(obs.config)

    with pytest.raises(ValueError):
        NSubjettiness.from_name("NSubjettiness", n=1)

    obs = TauN(physics_object="FatJet0", n=1)
    assert obs == TauN.from_name("FatJet0.Tau1")
    assert obs == TauN.from_config(obs.config)

    with pytest.raises(ValueError):
        TauN.from_name("Tau1")


def test_read(event):
    obs = TauN("FatJet0", 1).read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = TauN("FatJet:5", 1).read_ttree(event)
    assert obs.shape == "5 * float64"
