from ROOT import TLorentzVector

from .observable import Observable


class InvariantMass(Observable):
    def __init__(self, physics_object: str):
        supported_objects = ["single", "multiple"]
        super().__init__(physics_object, supported_objects)

    def read_ttree(self, event):
        self.physics_object.read_ttree(event)
        vectors = TLorentzVector()
        for obj in self.physics_object.objects:
            if obj != []:
                vectors += obj[0].P4()
            else:
                vectors += TLorentzVector()

        self._value = vectors.M()

        return self


class InvMass(InvariantMass):
    ...


class InvM(InvariantMass):
    ...


InvariantMass.add_alias("invariant_mass")
InvMass.add_alias("inv_mass")
InvM.add_alias("inv_m")
