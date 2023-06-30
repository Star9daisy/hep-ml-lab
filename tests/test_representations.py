from hml.generators import MG5Run
from hml.observables import M, Pt
from hml.representations import Set


def test_observables():
    run = MG5Run("tests/data/pp2zz/Events/run_01/")
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
        if event.FatJet.GetEntries() < 1:
            continue

        representation.from_event(event)
        break

    assert representation.values is not None
    assert representation.values.shape == (6,)
