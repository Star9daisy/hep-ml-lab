from __future__ import annotations

from typing import Any, Type


def validate_type(
    object_: Any,
    expected_types: Type | tuple[Type, ...],
    name: str | None = None,
):
    """Validate the type of an object.

    Parameters
    ----------
    object_ : Any
        The object to validate.
    expected_types : Type | tuple[Type, ...]
        The expected type or types of the object.
    name : str, optional
        The name of the object. This is used in the error message.

    Raises
    ------
    TypeError
        If the object is not of the expected type.

    Examples
    --------
    >>> validate_type("string", str)
    >>> validate_type("string", (str, int))

    >>> validate_type("string", int)
    Traceback (most recent call last):
        ...
    TypeError: object must be of type int, not str
    """
    name = name if name is not None else "object"

    # If the expected type is a single type, convert it to a tuple
    if not isinstance(expected_types, tuple):
        expected_types = (expected_types,)

    if not isinstance(object_, expected_types):
        if len(expected_types) == 1:
            raise TypeError(
                f"{name} must be of type {expected_types[0].__name__}, not {type(object_).__name__}"
            )
        else:
            type_names = tuple([t.__name__ for t in expected_types])
            raise TypeError(
                f"{name} must be one of {type_names}, not {type(object_).__name__}"
            )
