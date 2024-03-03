class PhysicsObject:
    def __eq__(self, other: "PhysicsObject") -> bool:
        return self.config == other.config

    def __repr__(self) -> str:
        classname = self.__class__.__name__

        configs = []
        for key, value in self.config.items():
            if isinstance(value, str):
                configs.append(f"{key}='{value}'")
            else:
                configs.append(f"{key}={value}")
        configs = ", ".join(configs)

        return f"{classname}({configs})"

    @classmethod
    def from_name(cls, name: str) -> "PhysicsObject":
        raise NotImplementedError

    @classmethod
    def from_config(cls, config: dict) -> "PhysicsObject":
        return cls(**config)

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def branch(self) -> str:
        raise NotImplementedError

    @property
    def slices(self) -> list[slice]:
        raise NotImplementedError

    @property
    def config(self) -> dict:
        raise NotImplementedError
