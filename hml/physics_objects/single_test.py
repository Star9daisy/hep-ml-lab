from hml.physics_objects import SinglePhysicsObject


def test_pattern():
    obj1 = SinglePhysicsObject("Jet", 0)
    obj2 = SinglePhysicsObject.from_name("Jet0")
    obj3 = SinglePhysicsObject.from_config(
        {
            "single_physics_object_type": "Jet",
            "single_physics_object_index": 0,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.index == 0
        assert obj.name == "Jet0"
        assert obj.config == {
            "single_physics_object_type": "Jet",
            "single_physics_object_index": 0,
        }
