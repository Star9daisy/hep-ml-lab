from math import isnan

from hml.observables.invariant_mass import InvariantMass
from hml.observables.invariant_mass import InvM
from hml.observables.invariant_mass import InvMass


def test_init():
    obs = InvariantMass(physics_object="Jet0,Jet1")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0,Jet1"
    assert obs.supported_types == ["single", "multiple"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0,Jet1.InvariantMass"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}
    assert repr(obs) == "Jet0,Jet1.InvariantMass : nan"

    obs = InvMass(physics_object="Jet0,Jet1")
    assert obs == InvariantMass(physics_object="Jet0,Jet1")

    obs = InvM(physics_object="Jet0,Jet1")
    assert obs == InvariantMass(physics_object="Jet0,Jet1")


def test_class_methods():
    obs = InvM(physics_object="Jet0,Jet1")
    assert obs == InvM.from_name("Jet0,Jet1.InvM")
    assert obs == InvM.from_config(obs.config)


def test_read(event):
    obs = InvM("Jet0,Jet1").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = InvM("Jet0,Jet1,Jet2").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = InvM("Jet0,Jet1,Jet100").read_ttree(event)
    assert obs.shape == "1 * float64"
