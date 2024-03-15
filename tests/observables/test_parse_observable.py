import pytest

from hml.observables import Pt, TauMN, TauN, parse


def test_parse():
    assert parse(None) is None
    assert parse("jet0.pt") == Pt(physics_object="jet0", class_name="pt")
    assert parse("fatjet0.tau1") == TauN(1, "fatjet0", class_name="tau1")
    assert parse("fatjet0.tau21") == TauMN(2, 1, "fatjet0", class_name="tau21")

    with pytest.raises(ValueError):
        parse("unknown_observable")
