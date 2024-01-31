from math import isnan

from hml.observables.azimuthal_angle import AzimuthalAngle
from hml.observables.azimuthal_angle import Phi


def test_init():
    obs = AzimuthalAngle(physics_object="Jet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0.AzimuthalAngle"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}


def test_class_methods():
    obs = AzimuthalAngle(physics_object="Jet0")

    assert repr(obs) == "Jet0.AzimuthalAngle : nan"
    assert obs == AzimuthalAngle.from_name("Jet0.AzimuthalAngle")


def test_read(event):
    obs = Phi("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Phi("Jet:5").read_ttree(event)
    assert obs.shape == "5 * float64"

    obs = Phi("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "2 * 5 * float64"
