from hml.generators import Madgraph5Run
from hml.observables import *
from hml.types import Path
from hml.utils import get_observable

DATA_DIR = Path("tests/data")
run_tt = Madgraph5Run(DATA_DIR / "pp2tt", "run_01")
run_zz = Madgraph5Run(DATA_DIR / "pp2zz", "run_01")
event_tt = next(iter(run_tt.events()))
event_zz = next(iter(run_zz.events()))


def test_four_vector():
    for obs_cls in [Px, Py, Pz, E, Pt, Eta, Phi, M]:
        cls_name = obs_cls.__name__

        for obj in [
            "Jet0",
            "Jet:2",
            "Jet0.Constituents:10",
            "Jet:2.Constituents:10",
            "Jet:2.Constituents",
            "Jet:200.Constituents:200",
            "Jet0,Jet1",
        ]:
            ...

            obs_specific = obs_cls(obj).read(event_tt)
            obs_agnostic = get_observable(f"{obj}.{cls_name}").read(event_tt)
            assert obs_specific == obs_agnostic


def test_n_subjettiness():
    for obj in [
        "FatJet0",
        "FatJet",
        "FatJet:2",
        "FatJet0,FatJet0",
        "FatJet0.Constituents",
    ]:
        obs_specific = NSubjettiness(obj, 1).read(event_zz)
        obs_agnostic = get_observable(f"{obj}.NSubjettiness", 1).read(event_tt)
        assert obs_specific == obs_agnostic


def test_n_subjettiness_ratio():
    for obj in [
        "FatJet0",
        "FatJet",
        "FatJet:2",
        "FatJet0,FatJet0",
        "FatJet0.Constituents",
    ]:
        obs_specific = NSubjettinessRatio(obj, 2, 1).read(event_zz)
        obs_agnostic = get_observable(f"{obj}.NSubjettinessRatio", 2, 1).read(event_tt)
        assert obs_specific == obs_agnostic


def test_b_tag():
    for obj in [
        "FatJet0",
        "FatJet",
        "FatJet:2",
        "FatJet0,FatJet0",
        "FatJet0.Constituents",
    ]:
        obs_specific = BTag(obj).read(event_zz)
        obs_agnostic = get_observable(f"{obj}.BTag").read(event_tt)
        assert obs_specific == obs_agnostic


def test_charge():
    for obj in [
        "FatJet0",
        "FatJet",
        "FatJet:2",
        "FatJet0,FatJet0",
        "FatJet0.Constituents",
    ]:
        obs_specific = Charge(obj).read(event_zz)
        obs_agnostic = get_observable(f"{obj}.Charge").read(event_tt)
        assert obs_specific == obs_agnostic


def test_size():
    for obj in ["Jet0", "Jet", "Jet:2", "Jet,Jet", "Jet0", "Jet.Constituents"]:
        obs_specific = Size(obj).read(event_zz)
        obs_agnostic = get_observable(f"{obj}.Size").read(event_tt)
        assert obs_specific == obs_agnostic
