from .observable import Observable


class Size(Observable):
    def __init__(self, physics_object: str):
        supported_types = ["collective"]
        super().__init__(physics_object, supported_types)

    def read_ttree(self, event):
        self.physics_object.read_ttree(event)
        self._value = len(self.physics_object.objects)

        return self


Size.add_alias("size")
