import pytest
import ROOT

ROOT.gSystem.Load("libDelphes")


@pytest.fixture
def event():
    filepath = "tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root"
    file = ROOT.TFile(filepath)
    tree = file.Get("Delphes")
    tree.GetEntry(0)

    yield tree
