import pytest

from hml.observables import Pt, TauMN, TauN, parse_observable


def test_parse():
    assert parse_observable(None) is None
    assert parse_observable("jet0.pt") == Pt(physics_object="jet0", class_name="pt")
    assert parse_observable("fatjet0.tau1") == TauN(1, "fatjet0", class_name="tau1")
    assert parse_observable("fatjet0.tau21") == TauMN(
        2, 1, "fatjet0", class_name="tau21"
    )

    with pytest.raises(ValueError):
        parse_observable("unknown_observable")
