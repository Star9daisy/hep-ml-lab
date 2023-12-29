from hml.utils import get_madgraph5_run, parse_physics_object


def test_get_madgraph5_run_for_single():
    expected = {
        "name": "run_01",
        "collider": "pp:6500.0x6500.0",
        "tag": "tag_1",
        "seed": 42,
        "cross": 503.6,
        "error": 2.8,
        "n_events": 100,
        "events": {
            "lhe": "tests/data/pp2tt/Events/run_01/unweighted_events.lhe.gz",
            "hepmc": "tests/data/pp2tt/Events/run_01/tag_1_pythia8_events.hepmc.gz",
            "root": "tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root",
        },
    }
    assert get_madgraph5_run("tests/data/pp2tt", "run_01") == expected


def test_get_madgraph5_run_for_multiple():
    expected = {
        "name": "run_02",
        "collider": "pp:6500.0x6500.0",
        "tag": "tag_1",
        "seed": 42,
        "cross": 503.7,
        "error": 2.0,
        "n_events": 200,
        "events": {"lhe": "tests/data/pp2tt/Events/run_02/unweighted_events.lhe.gz"},
    }
    assert get_madgraph5_run("tests/data/pp2tt", "run_02") == expected


def test_parse_physics_object_single():
    # Single case
    branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    indices = [0, 1, 2]
    phyobjs = [f"{b}{i}" for b in branches for i in indices]

    expected_starts = [i for i in indices]
    expected_ends = [i + 1 for i in indices]
    expected_phyobjs = [
        {"main": (b, s, e)}
        for b in branches
        for s, e in zip(expected_starts, expected_ends)
    ]
    expected_phyobjs = [[i] for i in expected_phyobjs]

    for obj, exp in zip(phyobjs, expected_phyobjs):
        assert parse_physics_object(obj) == exp


def test_parse_physics_object_collective_only_main():
    branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    starts = ["", 1, "", 2]
    ends = ["", "", 5, 3]
    phyobjs = [f"{b}{s}:{e}" for b in branches for s, e in zip(starts, ends)]

    expected_starts = [0, 1, 0, 2]
    expected_ends = [None, None, 5, 3]
    expected_phyobjs = [
        {"main": (b, s, e)}
        for b in branches
        for s, e in zip(expected_starts, expected_ends)
    ]
    expected_phyobjs = [[i] for i in expected_phyobjs]

    for obj, exp in zip(phyobjs, expected_phyobjs):
        assert parse_physics_object(obj) == exp


def test_parse_physics_object_collective_main_sub():
    main_branches = ["FatJet", "Jet"]
    sub_branches = ["Constituents", "Particles"]
    starts = ["", 1, "", 2]
    ends = ["", "", 5, 3]
    phyobjs = [
        f"{m}{ms}:{me}.{s}{ss}:{se}"
        for m in main_branches
        for s in sub_branches
        for ms, me in zip(starts, ends)
        for ss, se in zip(starts, ends)
    ]

    expected_starts = [0, 1, 0, 2]
    expected_ends = [None, None, 5, 3]
    expected_phyobjs = [
        {"main": (m, mes, mee), "sub": (s, ses, see)}
        for m in main_branches
        for s in sub_branches
        for mes, mee in zip(expected_starts, expected_ends)
        for ses, see in zip(expected_starts, expected_ends)
    ]
    expected_phyobjs = [[i] for i in expected_phyobjs]

    for obj, exp in zip(phyobjs, expected_phyobjs):
        assert parse_physics_object(obj) == exp


def test_parse_physics_object_multiple_single_single():
    # First
    sg1_branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    sg1_indices = [0, 1, 2]
    sg1_phyobjs = [f"{b}{i}" for b in sg1_branches for i in sg1_indices]

    # Second
    sg2_branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    sg2_indices = [0, 1, 2]
    sg2_phyobjs = [f"{b}{i}" for b in sg2_branches for i in sg2_indices]

    phyobjs = [f"{obj1},{obj2}" for obj1 in sg1_phyobjs for obj2 in sg2_phyobjs]

    expected_starts = [0, 1, 2]
    expected_ends = [1, 2, 3]
    expected_phyobjs = [
        [{"main": (obj1, s1, e1)}, {"main": (obj2, s2, e2)}]
        for obj1 in sg1_branches
        for s1, e1 in zip(expected_starts, expected_ends)
        for obj2 in sg2_branches
        for s2, e2 in zip(expected_starts, expected_ends)
    ]

    for obj, exp in zip(phyobjs, expected_phyobjs):
        assert parse_physics_object(obj) == exp


def test_parse_physics_object_multiple_single_collective_only_main():
    # First
    sg_branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    sg_starts = [0, 1, 2]
    sg_objs = [f"{s}{i}" for s in sg_branches for i in sg_starts]

    sg_expected_starts = [s for s in sg_starts]
    sg_expected_ends = [s + 1 for s in sg_starts]
    sg_expected_objs = [
        {"main": (b, s, e)}
        for b in sg_branches
        for s, e in zip(sg_expected_starts, sg_expected_ends)
    ]
    sg_expected_objs = [[i] for i in sg_expected_objs]

    # Second
    cc_branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    cc_starts = ["", 1, "", 2]
    cc_ends = ["", "", 5, 3]
    cc_objs = [f"{c}{s}:{e}" for c in cc_branches for s, e in zip(cc_starts, cc_ends)]

    cc_expectged_starts = [0, 1, 0, 2]
    cc_expected_ends = [None, None, 5, 3]
    cc_expected_objs = [
        {"main": (b, s, e)}
        for b in cc_branches
        for s, e in zip(cc_expectged_starts, cc_expected_ends)
    ]
    cc_expected_objs = [[i] for i in cc_expected_objs]

    mp_objs = [f"{sg},{cc}" for sg in sg_objs for cc in cc_objs]
    mp_expected_objs = [
        [sg[0], cc[0]] for sg in sg_expected_objs for cc in cc_expected_objs
    ]

    for physics_object, expected in zip(mp_objs, mp_expected_objs):
        assert parse_physics_object(physics_object) == expected


def test_parse_physics_object_multiple_main_sub():
    # First
    sg_branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    sg_starts = [0, 1, 2]
    sg_objs = [f"{s}{i}" for s in sg_branches for i in sg_starts]

    sg_expected_starts = [s for s in sg_starts]
    sg_expected_ends = [s + 1 for s in sg_starts]
    sg_expected_objs = [
        {"main": (b, s, e)}
        for b in sg_branches
        for s, e in zip(sg_expected_starts, sg_expected_ends)
    ]
    sg_expected_objs = [[i] for i in sg_expected_objs]

    # Second
    cc_main_branches = ["FatJet", "Jet"]
    cc_sub_branches = ["Constituents", "Particles"]
    cc_starts = ["", 1, "", 2]
    cc_ends = ["", "", 5, 3]
    cc_objs = [
        f"{m}{ms}:{me}.{s}{ss}:{se}"
        for m in cc_main_branches
        for s in cc_sub_branches
        for ms, me in zip(cc_starts, cc_ends)
        for ss, se in zip(cc_starts, cc_ends)
    ]

    cc_expectged_starts = [0, 1, 0, 2]
    cc_expected_ends = [None, None, 5, 3]
    cc_expected_objs = [
        {"main": (m, mes, mee), "sub": (s, ses, see)}
        for m in cc_main_branches
        for s in cc_sub_branches
        for mes, mee in zip(cc_expectged_starts, cc_expected_ends)
        for ses, see in zip(cc_expectged_starts, cc_expected_ends)
    ]
    cc_expected_objs = [[i] for i in cc_expected_objs]

    mp_objs = [f"{sg},{cc}" for sg in sg_objs for cc in cc_objs]
    mp_expected_objs = [
        [sg[0], cc[0]] for sg in sg_expected_objs for cc in cc_expected_objs
    ]

    for physics_object, expected in zip(mp_objs, mp_expected_objs):
        assert parse_physics_object(physics_object) == expected


def test_parse_physics_object_multiple_collective_collective_only_main():
    # First
    cc1_main_branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    cc1_starts = ["", 1, "", 2]
    cc1_ends = ["", "", 5, 3]
    cc1_objs = [
        f"{m}{ms}:{me}"
        for m in cc1_main_branches
        for ms, me in zip(cc1_starts, cc1_ends)
    ]

    # Second
    cc2_branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    cc2_starts = ["", 1, "", 2]
    cc2_ends = ["", "", 5, 3]
    cc2_objs = [
        f"{m}{ms}:{me}" for m in cc2_branches for ms, me in zip(cc2_starts, cc2_ends)
    ]

    # Physics objects
    mp_objs = [f"{i},{j}" for i in cc1_objs for j in cc2_objs]

    # Expected
    cc1_expectged_starts = [0, 1, 0, 2]
    cc1_expected_ends = [None, None, 5, 3]
    cc2_expectged_starts = [0, 1, 0, 2]
    cc2_expected_ends = [None, None, 5, 3]
    mp_expected_objs = [
        [{"main": (i, ies, iee)}, {"main": (j, jes, jee)}]
        for i in cc1_main_branches
        for ies, iee in zip(cc1_expectged_starts, cc1_expected_ends)
        for j in cc2_branches
        for jes, jee in zip(cc2_expectged_starts, cc2_expected_ends)
    ]

    for obj, exp in zip(mp_objs, mp_expected_objs):
        assert parse_physics_object(obj) == exp


def test_parse_physics_object_multiple_collective_collective_main_sub_main():
    # First
    cc1_main_branches = ["FatJet", "Jet"]
    cc1_sub_branches = ["Constituents", "Particles"]
    cc1_starts = ["", 1, "", 2]
    cc1_ends = ["", "", 5, 3]
    cc1_objs = [
        f"{m}{ms}:{me}.{s}{ss}:{se}"
        for m in cc1_main_branches
        for s in cc1_sub_branches
        for ms, me in zip(cc1_starts, cc1_ends)
        for ss, se in zip(cc1_starts, cc1_ends)
    ]

    # Second
    cc2_branches = ["Electron", "Jet", "MissingET", "Muon", "Photon"]
    cc2_starts = ["", 1, "", 2]
    cc2_ends = ["", "", 5, 3]
    cc2_objs = [
        f"{m}{ms}:{me}" for m in cc2_branches for ms, me in zip(cc2_starts, cc2_ends)
    ]

    # Physics objects
    mp_objs = [f"{i},{j}" for i in cc1_objs for j in cc2_objs]

    # Expected
    cc1_expectged_starts = [0, 1, 0, 2]
    cc1_expected_ends = [None, None, 5, 3]
    cc2_expectged_starts = [0, 1, 0, 2]
    cc2_expected_ends = [None, None, 5, 3]
    mp_expected_objs = [
        [{"main": (im, imes, imee), "sub": (_is, ises, isee)}, {"main": (j, jes, jee)}]
        for im in cc1_main_branches
        for _is in cc1_sub_branches
        for imes, imee in zip(cc1_expectged_starts, cc1_expected_ends)
        for ises, isee in zip(cc1_expectged_starts, cc1_expected_ends)
        for j in cc2_branches
        for jes, jee in zip(cc2_expectged_starts, cc2_expected_ends)
    ]

    for obj, exp in zip(mp_objs, mp_expected_objs):
        assert parse_physics_object(obj) == exp


def test_parse_physics_object_multiple_collective_collective_main_sub_main_sub():
    # First
    cc1_main_branches = ["FatJet", "Jet"]
    cc1_sub_branches = ["Constituents", "Particles"]
    cc1_starts = ["", 1, "", 2]
    cc1_ends = ["", "", 5, 3]
    cc1_objs = [
        f"{m}{ms}:{me}.{s}{ss}:{se}"
        for m in cc1_main_branches
        for s in cc1_sub_branches
        for ms, me in zip(cc1_starts, cc1_ends)
        for ss, se in zip(cc1_starts, cc1_ends)
    ]

    # Second
    cc2_main_branches = ["FatJet", "Jet"]
    cc2_sub_branches = ["Constituents", "Particles"]
    cc2_starts = ["", 1, "", 2]
    cc2_ends = ["", "", 5, 3]
    cc2_objs = [
        f"{m}{ms}:{me}.{s}{ss}:{se}"
        for m in cc2_main_branches
        for s in cc2_sub_branches
        for ms, me in zip(cc2_starts, cc2_ends)
        for ss, se in zip(cc2_starts, cc2_ends)
    ]

    # Physics objects
    mp_objs = [f"{i},{j}" for i in cc1_objs for j in cc2_objs]

    # Expected
    cc1_expectged_starts = [0, 1, 0, 2]
    cc1_expected_ends = [None, None, 5, 3]
    cc2_expectged_starts = [0, 1, 0, 2]
    cc2_expected_ends = [None, None, 5, 3]
    mp_expected_objs = [
        [
            {"main": (im, imes, imee), "sub": (_is, ises, isee)},
            {"main": (jm, jmes, jmee), "sub": (js, jses, jsee)},
        ]
        for im in cc1_main_branches
        for _is in cc1_sub_branches
        for imes, imee in zip(cc1_expectged_starts, cc1_expected_ends)
        for ises, isee in zip(cc1_expectged_starts, cc1_expected_ends)
        for jm in cc2_main_branches
        for js in cc2_sub_branches
        for jmes, jmee in zip(cc2_expectged_starts, cc2_expected_ends)
        for jses, jsee in zip(cc2_expectged_starts, cc2_expected_ends)
    ]

    for obj, exp in zip(mp_objs, mp_expected_objs):
        assert parse_physics_object(obj) == exp
