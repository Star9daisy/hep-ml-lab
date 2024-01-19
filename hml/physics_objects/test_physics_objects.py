import pytest

import hml.physics_objects as module


def test_get():
    obj = module.get("Jet0")
    assert isinstance(obj, module.SinglePhysicsObject)

    for name in ["Jet", "Jet1:", "Jet:3", "Jet1:3"]:
        obj = module.get(name)
        assert isinstance(obj, module.CollectivePhysicsObject)

    for name in ["Jet1.Constituents2", "Jet1.Constituents"]:
        obj = module.get(name)
        assert isinstance(obj, module.NestedPhysicsObject)

    for name in ["Jet1,Jet2", "Jet.Constituents,Jet0"]:
        obj = module.get(name)
        assert isinstance(obj, module.MultiplePhysicsObject)

    with pytest.raises(ValueError):
        module.get("Jet1.Constituents2.Constituents2")
