import pytest

from . import get
from .collective import Collective
from .multiple import Multiple
from .nested import Nested
from .single import Single


def test_get():
    assert get("single") == Single
    assert get("collective") == Collective
    assert get("nested") == Nested
    assert get("multiple") == Multiple

    with pytest.raises(ValueError):
        assert get("unknown")
