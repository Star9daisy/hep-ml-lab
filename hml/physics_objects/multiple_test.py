import pytest

from ..events.delphes_events import DelphesEvents
from .collective import Collective
from .multiple import Multiple
from .nested import Nested
from .single_test import Single


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obj = Multiple(
        Single("Jet", 0),
        Collective("Jet", 0, 2),
        Nested(Single("Jet", 0), Collective("Particles", 0, 2)),
    )
    assert obj.all[0] == Single("Jet", 0)
    assert obj.all[1] == Collective("Jet", 0, 2)
    assert obj.all[2] == Nested(Single("Jet", 0), Collective("Particles", 0, 2))
    assert obj.objects == []
    assert obj.id == "Jet0,Jet:2,Jet0.Particles:2"
    assert repr(obj) == "Multiple: Jet0,Jet:2,Jet0.Particles:2"
    assert obj.config == {
        "classname": "Multiple",
        "all_configs": [
            {"classname": "Single", "field": "Jet", "index": 0},
            {"classname": "Collective", "field": "Jet", "start": 0, "stop": 2},
            {
                "classname": "Nested",
                "main_config": {
                    "classname": "Single",
                    "field": "Jet",
                    "index": 0,
                },
                "sub_config": {
                    "classname": "Collective",
                    "field": "Particles",
                    "start": 0,
                    "stop": 2,
                },
            },
        ],
    }


def test_from_id():
    assert Multiple.from_id("Jet0,Jet:2,Jet0.Particles:2") == Multiple(
        Single("Jet", 0),
        Collective("Jet", 0, 2),
        Nested(Single("Jet", 0), Collective("Particles", 0, 2)),
    )
    assert Multiple.from_id("Jet0,Jet:2,Jet0.Particles:2") != Multiple(
        Single("Jet", 0),
        Collective("Jet", 0, 2),
        Nested(Single("Jet", 0), Collective("Particles", 0, 3)),
    )

    with pytest.raises(ValueError):
        Multiple.from_id("Jet0")

    with pytest.raises(ValueError):
        Multiple.from_id("Jet")

    with pytest.raises(ValueError):
        Multiple.from_id("Jet.Constituents")

    with pytest.raises(ValueError):
        Multiple.from_id("Jet,Jet")


def test_from_config():
    obj = Multiple(
        Single("Jet", 0),
        Collective("Jet", 0, 2),
        Nested(Single("Jet", 0), Collective("Particles", 0, 2)),
    )
    assert Multiple.from_config(obj.config) == obj

    with pytest.raises(ValueError):
        Multiple.from_config({"classname": "Unknown", "all_configs": []})

    with pytest.raises(ValueError):
        Multiple.from_config(
            {
                "classname": "Multiple",
                "all_configs": [
                    {
                        "classname": "Unknown",
                        "field": "Jet",
                        "index": 0,
                    }
                ],
            }
        )


def test_read(event):
    obj = Multiple(
        Single("Jet", 0),
        Collective("Jet", 0, 2),
        Nested(Single("Jet", 0), Collective("Particles", 0, 2)),
    )
    assert obj.read_ttree(event).objects == [
        [event.Jet[0]],
        [event.Jet[0], event.Jet[1]],
        [[event.Jet[0].Particles[0], event.Jet[0].Particles[1]]],
    ]
