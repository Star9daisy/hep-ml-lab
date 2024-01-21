import pytest

from . import CollectivePhysicsObject
from . import MultiplePhysicsObject
from . import NestedPhysicsObject
from . import SinglePhysicsObject
from . import get


def test_get():
    obj = get(None)
    assert obj is None

    obj = get("Jet0")
    assert isinstance(obj, SinglePhysicsObject)

    for name in ["Jet", "Jet1:", "Jet:3", "Jet1:3"]:
        obj = get(name)
        assert isinstance(obj, CollectivePhysicsObject)

    for name in ["Jet1.Constituents2", "Jet1.Constituents"]:
        obj = get(name)
        assert isinstance(obj, NestedPhysicsObject)

    for name in ["Jet1,Jet2", "Jet.Constituents,Jet0"]:
        obj = get(name)
        assert isinstance(obj, MultiplePhysicsObject)

    with pytest.raises(ValueError):
        get("Jet1.Constituents2.Constituents2")
