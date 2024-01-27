import pytest

from hml.physics_objects import Collective
from hml.physics_objects import Multiple
from hml.physics_objects import Nested
from hml.physics_objects import Single
from hml.physics_objects import get_physics_object


def test_get_physics_object(
    single_names,
    collective_names,
    nested_names,
    multiple_names,
):
    # Single ----------------------------------------------------------------- #
    for case in single_names:
        assert isinstance(get_physics_object(case), Single)

    # Collective ------------------------------------------------------------- #
    for case in collective_names:
        assert isinstance(get_physics_object(case), Collective)

    # Nested ----------------------------------------------------------------- #
    for case in nested_names:
        assert isinstance(get_physics_object(case), Nested)

    # Multiple --------------------------------------------------------------- #
    for case in multiple_names:
        assert isinstance(get_physics_object(case), Multiple)

    # Invalid cases ---------------------------------------------------------- #
    with pytest.raises(ValueError):
        get_physics_object("Jet")
