from hml.physics_objects import Collective, Nested, Single, get


def test_get():
    assert get("single") is Single
    assert get("Single") is Single
    assert get("collective") is Collective
    assert get("Collective") is Collective
    assert get("nested") is Nested
    assert get("Nested") is Nested
