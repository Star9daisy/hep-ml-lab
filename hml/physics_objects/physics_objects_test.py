import pytest

from . import get
from .collective import Collective
from .multiple import Multiple
from .nested import Nested
from .single import Single


def test_get():
    obj = get("Jet0")
    assert isinstance(obj, Single)

    for name in ["Jet:", "Jet1:", "Jet:3", "Jet1:3"]:
        obj = get(name)
        assert isinstance(obj, Collective)

    for name in ["Jet1.Constituents2", "Jet1.Constituents:"]:
        obj = get(name)
        assert isinstance(obj, Nested)

    for name in ["Jet1,Jet2", "Jet:.Constituents:,Jet0"]:
        obj = get(name)
        assert isinstance(obj, Multiple)

    with pytest.raises(ValueError):
        get("Jet1.Constituents2.Constituents2")

    with pytest.raises(ValueError):
        get("Jet.Constituents")
