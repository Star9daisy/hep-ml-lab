# import pytest
# import ROOT

# from hml.generators.madgraph5 import Madgraph5Run


# @pytest.fixture
# def event():
#     ROOT.gSystem.Load("libDelphes")
#     filepath = "tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root"
#     file = ROOT.TFile(filepath)
#     tree = file.Get("Delphes")
#     tree.GetEntry(0)

#     yield tree


# @pytest.fixture
# def run():
#     return Madgraph5Run("tests/data/pp2zz", "run_01")
