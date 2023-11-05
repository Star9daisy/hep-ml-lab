from typing import Any

import pytest

from hml.generators import Madgraph5
from hml.observables import (
    DeltaR,
    E,
    Eta,
    M,
    NSubjettiness,
    NSubjettinessRatio,
    Observable,
    Phi,
    Pt,
    Px,
    Py,
    Pz,
    Size,
    get_observable,
)


def test_Observable(tmp_path):
    demo_output = tmp_path / "demo"

    g = Madgraph5(processes=["p p > z z, z > j j, z > e+ e-"], output=demo_output)
    run = g.launch(
        shower="pythia8",
        detector="delphes",
        settings={"iseed": 42, "nevents": 100},
    )
    event = next(iter(run.events))

    for obs_class in [Px, Py, Pz, E, Pt, Eta, Phi, M]:
        obs1 = obs_class("Jet_0").read_event(event)
        obs2 = get_observable(f"Jet_0.{obs_class.__name__}").read_event(event)
        assert obs1.name == obs2.name
        assert obs1.value == obs2.value

    obs1 = Size("Jet").read_event(event)
    obs2 = get_observable("Jet.Size").read_event(event)
    obs3 = Size(object_pairs=[("Jet", None)]).read_event(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value
    assert obs1.name == obs3.name
    assert obs1.value == obs3.value

    obs1 = DeltaR("Jet_0-Jet_1").read_event(event)
    obs2 = get_observable("Jet_0-Jet_1.DeltaR").read_event(event)
    obs3 = DeltaR(object_pairs=[("Jet", 0), ("Jet", 1)]).read_event(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value
    assert obs1.name == obs3.name
    assert obs1.value == obs3.value
    assert repr(obs1) == f"Jet_0-Jet_1.DeltaR: {obs1.value}"
    assert obs1.to_numpy().shape == ()

    obs1 = NSubjettiness("FatJet_0", n=1).read_event(event)
    obs2 = get_observable("FatJet_0.NSubjettiness", n=1).read_event(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value

    obs1 = NSubjettinessRatio("FatJet_0", m=2, n=1).read_event(event)
    obs2 = get_observable("FatJet_0.NSubjettinessRatio", m=2, n=1).read_event(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value

    with pytest.raises(ValueError):
        get_observable("wrong_name")

    class Dummy(Observable):
        def get_value(self) -> Any:
            return 1.0

    dummy = get_observable("Dummy").read_event(event)
    assert dummy.name == "Dummy"
