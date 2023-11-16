from typing import Any

import pytest

from hml.generators import Madgraph5
from hml.observables import (
    AngularDistance,
    AzimuthalAngle,
    Energy,
    Mass,
    MomentumX,
    MomentumY,
    MomentumZ,
    NSubjettiness,
    NSubjettinessRatio,
    Observable,
    PseudoRapidity,
    Size,
    TransverseMomentum,
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
    if event.Jet.GetEntries() < 2:
        for event in run.events:
            if event.Jet.GetEntries() >= 2:
                break

    for obs_class in [
        MomentumX,
        MomentumY,
        MomentumZ,
        Energy,
        TransverseMomentum,
        PseudoRapidity,
        AzimuthalAngle,
        Mass,
    ]:
        obs1 = obs_class("Jet_0").read(event)
        obs2 = get_observable(f"Jet_0.{obs_class.__name__}").read(event)
        assert obs1.name == obs2.name
        assert obs1.value == obs2.value

    obs1 = Size("Jet").read(event)
    obs2 = get_observable("Jet.Size").read(event)
    obs3 = Size(phyobj_pairs=[("Jet", None)]).read(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value
    assert obs1.name == obs3.name
    assert obs1.value == obs3.value

    obs1 = AngularDistance("Jet_0-Jet_1").read(event)
    obs2 = get_observable("Jet_0-Jet_1.DeltaR").read(event)
    obs3 = AngularDistance(phyobj_pairs=[("Jet", 0), ("Jet", 1)]).read(event)
    # assert obs1.name == obs2.name
    assert obs1.name == "Jet_0-Jet_1.AngularDistance"
    assert obs2.name == "Jet_0-Jet_1.DeltaR"
    assert obs3.name == "Jet_0-Jet_1.AngularDistance"
    assert obs1.value == obs2.value
    # assert obs1.name == obs3.name
    assert obs1.value == obs3.value
    assert repr(obs1) == f"Jet_0-Jet_1.AngularDistance: {obs1.value}"
    assert obs1.to_numpy().shape == ()

    obs1 = NSubjettiness("FatJet_0", n=1).read(event)
    obs2 = get_observable("FatJet_0.NSubjettiness", n=1).read(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value

    obs1 = NSubjettinessRatio("FatJet_0", m=2, n=1).read(event)
    obs2 = get_observable("FatJet_0.NSubjettinessRatio", m=2, n=1).read(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value

    with pytest.raises(ValueError):
        get_observable("wrong_name")

    class Dummy(Observable):
        def get_value(self) -> Any:
            return 1.0

    dummy = get_observable("Dummy").read(event)
    assert dummy.name == "Dummy"
