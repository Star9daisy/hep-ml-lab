import pytest
import uproot


@pytest.fixture
def events():
    filepath = "tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root"
    events = uproot.open(filepath)["Delphes"]

    yield events
