from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from typing import Any, Protocol

import numpy
from keras import Model
from keras.engine.functional import Functional
from keras.engine.sequential import Sequential
from keras.models import load_model


class Method(Protocol):
    @property
    def name(self) -> str:
        ...

    def n_parameters(self) -> int:
        ...

    def compile(self, optimizer: Any, loss: Any, metrics: Any) -> None:
        ...

    def fit(self, x: Any, y: Any, *args, **kwargs) -> dict:
        ...

    def predict(self, x: Any, *args, **kwargs) -> numpy.ndarray:
        ...

    def evaluate(self, x: Any, y: Any, *args, **kwargs) -> dict:
        ...

    def summary(self) -> str:
        ...

    def save(self, file_path: str, overwrite: bool, save_format: str) -> None:
        ...

    @classmethod
    def load(cls, file_path: str) -> Method:
        ...


class KerasMethod:
    def __init__(self, model: Sequential | Functional | Model) -> None:
        self.model = model

    @property
    def name(self) -> str:
        return self.model.name

    @property
    def n_parameters(self) -> int:
        return self.model.count_params()

    def compile(self, *args, **kwargs) -> None:
        self.model.compile(*args, **kwargs)

    def fit(self, x: Any, y: Any, *args, **kwargs) -> dict:
        history = self.model.fit(x, y, *args, **kwargs)
        return history.history

    def predict(self, x: Any, *args, **kwargs) -> numpy.ndarray:
        return self.model.predict(x, *args, **kwargs)

    def evaluate(self, x: Any, y: Any, *args, **kwargs) -> float | dict | list:
        return self.model.evaluate(x, y, *args, **kwargs)

    def summary(self) -> str:
        stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        self.model.summary()
        sys.stdout = stdout
        return output_buffer.getvalue()

    def save(self, file_path: str | Path, overwrite: bool = True, save_format: str = "h5") -> None:
        file_path = Path(file_path)
        if file_path.suffix != ".h5" and save_format == "h5":
            file_path = file_path.with_suffix(".h5")
        self.model.save(
            filepath=file_path,
            overwrite=overwrite,
            save_format=save_format,
        )

    @classmethod
    def load(cls, file_path: str | Path, **kwargs) -> KerasMethod:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Saved model {file_path} does not exist.")
        else:
            model = load_model(filepath=file_path, **kwargs)
            return cls(model=model)
