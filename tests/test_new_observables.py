from hml.new_generators import Madgraph5
from hml.new_observables import (
    DeltaR,
    E,
    Eta,
    M,
    NSubjettiness,
    NSubjettinessRatio,
    Phi,
    Pt,
    Px,
    Py,
    Pz,
    get_observable,
)


def test_Observable(tmpdir):
    demo_output = tmpdir / "test"

    g = Madgraph5(processes=["p p > z z, z > j j, z > e+ e-"], output=demo_output)
    run = g.launch(
        shower="pythia8",
        detector="delphes",
        settings={"iseed": 42, "nevents": 100},
    )
    event = next(iter(run.events))

    for obs_class in [Px, Py, Pz, E, Pt, Eta, Phi, M]:
        obs1 = obs_class("Jet_0").read(event)
        obs2 = get_observable(f"Jet_0.{obs_class.__name__}").read(event)
        assert obs1.name == obs2.name
        assert obs1.value == obs2.value

    obs1 = DeltaR("Jet_0-Jet_1").read(event)
    obs2 = get_observable("Jet_0-Jet_1.DeltaR").read(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value

    obs1 = NSubjettiness("FatJet_0", n=1).read(event)
    obs2 = get_observable("FatJet_0.NSubjettiness", n=1).read(event)
    assert obs1.name == obs2.name
    assert obs1.value == obs2.value

    obs1 = NSubjettinessRatio("FatJet_0", m=2, n=1).read(event)
    obs2 = get_observable("FatJet_0.NSubjettinessRatio", m=2, n=1).read(event)
