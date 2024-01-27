import pytest


@pytest.fixture
def single_names():
    yield [
        "Jet0",
    ]


@pytest.fixture
def collective_names():
    yield [
        "Jet:",
        "Jet1:",
        "Jet:3",
        "Jet1:3",
    ]


@pytest.fixture
def nested_names():
    yield [
        "Jet0.Constituents0",
        "Jet0.Constituents:",
        "Jet0.Constituents1:",
        "Jet0.Constituents:3",
        "Jet0.Constituents1:3",
        "Jet:.Constituents:",
        "Jet:.Constituents1:",
        "Jet:.Constituents:3",
        "Jet:.Constituents1:3",
        "Jet1:.Constituents:",
        "Jet1:.Constituents1:",
        "Jet1:.Constituents:3",
        "Jet1:.Constituents1:3",
        "Jet:3.Constituents:",
        "Jet:3.Constituents1:",
        "Jet:3.Constituents:3",
        "Jet:3.Constituents1:3",
        "Jet1:3.Constituents:",
        "Jet1:3.Constituents1:",
        "Jet1:3.Constituents:3",
        "Jet1:3.Constituents1:3",
    ]


@pytest.fixture
def multiple_names():
    yield [
        "Jet0,Jet1",
        "Jet0,Jet1,Jet2",
        "Jet0,Jet:",
        "Jet0,Jet0.Constituents:",
        "Jet0.Constituents:,Jet0.Constituents:",
    ]
