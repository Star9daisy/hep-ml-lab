from __future__ import annotations

ALL_OBJECTS_DICT = {}


class PhysicsObject:
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        ALL_OBJECTS_DICT[cls.__name__] = cls

    def __eq__(self, other: str | PhysicsObject) -> bool:
        if isinstance(other, str):
            return self.name == other
        else:
            return self.config == other.config

    def __str__(self) -> str:
        return self.name

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
    def add_alias(cls, *alias: str) -> None:
        for i in alias:
            ALL_OBJECTS_DICT[i] = cls

    @classmethod
    def from_name(cls, name: str) -> PhysicsObject:
        raise NotImplementedError

    @classmethod
    def from_config(cls, config: dict) -> PhysicsObject:
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
