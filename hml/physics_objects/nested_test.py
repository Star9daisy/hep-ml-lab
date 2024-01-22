import pytest

from ..events.delphes_events import DelphesEvents
from .collective import Collective
from .nested import Nested
from .single import Single


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obj = Nested(Single("Jet", 0), Single("Particles", 0))
    assert obj.main == Single("Jet", 0)
    assert obj.sub == Single("Particles", 0)
    assert obj.objects == []
    assert obj.identifier == "Jet0.Particles0"
    assert repr(obj) == "Jet0.Particles0"
    assert obj.config == {
        "classname": "Nested",
        "main_object_config": {
            "classname": "Single",
            "name": "Jet",
            "index": 0,
        },
        "sub_object_config": {
            "classname": "Single",
            "name": "Particles",
            "index": 0,
        },
    }

    obj = Nested(Collective("Jet", 0, 2), Collective("Particles", 0, 3))
    assert obj.main == Collective("Jet", 0, 2)
    assert obj.sub == Collective("Particles", 0, 3)
    assert obj.objects == []
    assert obj.identifier == "Jet:2.Particles:3"
    assert repr(obj) == "Jet:2.Particles:3"
    assert obj.config == {
        "classname": "Nested",
        "main_object_config": {
            "classname": "Collective",
            "name": "Jet",
            "start": 0,
            "stop": 2,
        },
        "sub_object_config": {
            "classname": "Collective",
            "name": "Particles",
            "start": 0,
            "stop": 3,
        },
    }


def test_from_identifier():
    assert Nested.from_identifier("Jet0.Particles0") == Nested(
        Single("Jet", 0), Single("Particles", 0)
    )
    assert Nested.from_identifier("Jet0.Particles1") != Nested(
        Single("Jet", 0), Single("Particles", 0)
    )

    with pytest.raises(ValueError):
        Nested.from_identifier("Jet0")

    with pytest.raises(ValueError):
        Nested.from_identifier("Jet")

    with pytest.raises(ValueError):
        Nested.from_identifier("Jet0,Jet1")


def test_from_config():
    obj = Nested(Single("Jet", 0), Single("Particles", 0))
    assert obj == Nested.from_config(obj.config)

    obj = Nested(Collective("Jet", 0, 2), Collective("Particles", 0, 3))
    assert obj == Nested.from_config(obj.config)

    with pytest.raises(ValueError):
        Nested.from_config({"classname": "Unknown"})


def test_read(event):
    obj = Nested.from_identifier("Jet0.Particles0").read(event)
    assert len(obj.objects) == 1
    assert len(obj.objects[0]) == 1
    assert obj.objects[0][0] is not None

    obj = Nested.from_identifier("Jet0.Particles100").read(event)
    assert len(obj.objects) == 1
    assert len(obj.objects[0]) == 1
    assert obj.objects[0][0] is None

    obj = Nested.from_identifier("Jet:2.Particles100").read(event)
    assert len(obj.objects) == 2
    for i in range(2):
        assert len(obj.objects[i]) == 1
        assert obj.objects[i][0] is None

    obj = Nested.from_identifier("Jet100.Particles0").read(event)
    assert len(obj.objects) == 1
    assert len(obj.objects[0]) == 1
    assert obj.objects[0][0] is None

    obj = Nested.from_identifier("Jet100.Particles100:110").read(event)
    assert len(obj.objects) == 1
    assert len(obj.objects[0]) == 10
    assert any(obj.objects[0]) is False

    obj = Nested.from_identifier("Jet3:6.Particles100").read(event)
    assert len(obj.objects) == 3
    for i in range(3):
        assert len(obj.objects[i]) == 1
        assert obj.objects[i][0] is None

    obj = Nested.from_identifier("Jet:3.Particles:10").read(event)
    assert len(obj.objects) == 3
    for i in range(3):
        assert len(obj.objects[i]) == 10
        assert all(obj.objects[i]) is True
