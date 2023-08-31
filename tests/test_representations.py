import shutil
from pathlib import Path

from hml.generators import Madgraph5, MG5Run
from hml.observables import M, Pt
from hml.representations import Set


def test_observables():
    event_name = "pp2zj_"
    generator = Madgraph5(
        executable="mg5_aMC",
        processes=["p p > z j, z > j j"],
        output=f"./tests/data/{event_name}",
        shower="Pythia8",
        detector="Delphes",
        settings={"nevents": 10, "iseed": 42},
    )

    generator.launch()
    run = MG5Run(f"tests/data/{event_name}/run_1")
    representation = Set(
        [
            Pt("Jet1"),
            Pt("Jet2"),
            Pt("Jet1+Jet2"),
            M("Jet1"),
            M("Jet2"),
            M("Jet1+Jet2"),
        ]
    )

    for event in run.events:
        if event.Jet.GetEntries() < 2:
            continue

        representation.from_event(event)
        break

    assert representation.values is not None
    assert representation.values.shape == (6,)

    # Clean up
    run.events.Reset()
    generator.clean()
