import pytest


@pytest.fixture
def single_names():
    yield [
        "jet0",
        "muon1",
    ]


@pytest.fixture
def collective_names():
    yield [
        "jet",
        "jet:",
        "jet1:",
        "jet:3",
        "jet1:3",
    ]


@pytest.fixture
def nested_names():
    yield [
        "jet0.Constituents0",
        "jet0.Constituents:",
        "jet0.Constituents1:",
        "jet0.Constituents:3",
        "jet0.Constituents1:3",
        "jet:.Constituents:",
        "jet:.Constituents1:",
        "jet:.Constituents:3",
        "jet:.Constituents1:3",
        "jet1:.Constituents:",
        "jet1:.Constituents1:",
        "jet1:.Constituents:3",
        "jet1:.Constituents1:3",
        "jet:3.Constituents:",
        "jet:3.Constituents1:",
        "jet:3.Constituents:3",
        "jet:3.Constituents1:3",
        "jet1:3.Constituents:",
        "jet1:3.Constituents1:",
        "jet1:3.Constituents:3",
        "jet1:3.Constituents1:3",
    ]


@pytest.fixture
def multiple_names():
    yield [
        "jet0,jet1",
        "jet0,jet1,jet2",
        "jet0,jet:",
        "jet0,jet0.constituents:",
        "jet0.constituents:,jet0.constituents:",
    ]
