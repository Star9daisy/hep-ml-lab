from math import isnan

import pytest

from hml.observables.n_subjettiness_ratio import NSubjettinessRatio
from hml.observables.n_subjettiness_ratio import TauMN


def test_init():
    obs = NSubjettinessRatio(physics_object="FatJet0", m=2, n=1)

    # Parameters ------------------------------------------------------------- #
    assert obs.m == 2
    assert obs.n == 1
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_types == ["single", "collective"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "FatJet0.NSubjettinessRatio"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"m": 2, "n": 1, "physics_object": obs.physics_object.name}
    assert repr(obs) == "FatJet0.NSubjettinessRatio : nan"

    obs = TauMN(physics_object="FatJet0", m=2, n=1)

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "FatJet0.Tau21"


def test_class_methods():
    obs = NSubjettinessRatio(physics_object="FatJet0", m=2, n=1)
    assert obs == NSubjettinessRatio.from_name("FatJet0.NSubjettiness", m=2, n=1)
    assert obs == NSubjettinessRatio.from_config(obs.config)

    with pytest.raises(ValueError):
        NSubjettinessRatio.from_name("NSubjettinessRatio", m=2, n=1)

    obs = TauMN(physics_object="FatJet0", m=2, n=1)
    assert obs == TauMN.from_name("FatJet0.Tau21")
    assert obs == TauMN.from_config(obs.config)

    with pytest.raises(ValueError):
        TauMN.from_name("Tau21")


def test_read(event):
    obs = TauMN("FatJet0", 2, 1).read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = TauMN("FatJet:5", 2, 1).read_ttree(event)
    assert obs.shape == "5 * float64"
