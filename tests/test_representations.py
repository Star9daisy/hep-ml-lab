from hml.generators import Madgraph5
from hml.observables import Mass, TransverseMomentum
from hml.representations import Set
from hml.utils import Filter


def test_Set(tmp_path):
    demo_output = tmp_path / "demo"
    g = Madgraph5(processes=["p p > z z, z > j j, z > e+ e-"], output=demo_output)
    run = g.launch(
        shower="pythia8",
        detector="delphes",
        settings={"iseed": 42, "nevents": 100},
    )
    representation1 = Set([TransverseMomentum("Jet0"), Mass("Jet1"), Mass("Jet0+Jet1")])
    representation2 = Set(["Jet0.Pt", "Jet1.M", "Jet0+Jet1.M"])

    for event in run.events:
        if Filter(["Jet.Size >= 2"]).read_event(event).passed():
            representation1.read_event(event)
            representation2.read_event(event)
            break

    assert representation1.values is not None
    assert representation1.to_numpy().shape == (1, 3)
    assert representation1.to_pandas().shape == (1, 3)
    assert representation1.to_numpy().shape == representation2.to_numpy().shape
