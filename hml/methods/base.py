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
        ...  # pragma: no cover

    def n_parameters(self) -> int:
        ...  # pragma: no cover

    def compile(self, optimizer: Any, loss: Any, metrics: Any) -> None:
        ...  # pragma: no cover

    def fit(self, x: Any, y: Any, *args, **kwargs) -> dict:
        ...  # pragma: no cover

    def predict(self, x: Any, *args, **kwargs) -> numpy.ndarray:
        ...  # pragma: no cover

    def evaluate(self, x: Any, y: Any, *args, **kwargs) -> dict:
        ...  # pragma: no cover

    def summary(self) -> str:
        ...  # pragma: no cover

    def save(self, file_path: str, overwrite: bool) -> None:
        ...  # pragma: no cover

    @classmethod
    def load(cls, file_path: str) -> Method:
        ...  # pragma: no cover


class KerasMethod:
    def __init__(self, model: Sequential | Functional | Model) -> None:
        self.model = model

    @property
    def name(self) -> str:
        return self.model.name

    @property
    def n_parameters(self) -> int:
        return self.model.count_params()

    def compile(self, optimizer="rmsprop", loss=None, metrics=None, *args, **kwargs) -> None:
        self.model.compile(optimizer, loss, metrics, *args, **kwargs)

    def fit(self, x: Any, y: Any, *args, **kwargs) -> dict:
        history = self.model.fit(x, y, *args, **kwargs)
        return history.history

    def predict(self, x: Any, *args, **kwargs) -> numpy.ndarray:
        return self.model.predict(x, *args, **kwargs)

    def evaluate(self, x: Any, y: Any, *args, **kwargs) -> float | dict | list:
        return self.model.evaluate(x, y, *args, **kwargs)

    def summary(self, return_string: bool = False, **kwargs) -> str | None:
        if return_string:
            stdout = sys.stdout
            output_buffer = StringIO()
            sys.stdout = output_buffer
            self.model.summary(**kwargs)
            sys.stdout = stdout
            return output_buffer.getvalue()
        else:
            self.model.summary(**kwargs)

    def save(self, file_path: str | Path, overwrite: bool = True) -> None:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path.suffix != ".h5":
            file_path = file_path.with_suffix(".h5")

        if file_path.exists() and not overwrite:
            raise FileExistsError(f"Checkpoint {file_path} already exists.")

        self.model.save(
            filepath=file_path,
            overwrite=overwrite,
            save_format="h5",
        )

    @classmethod
    def load(cls, file_path: str | Path, *args, **kwargs) -> KerasMethod:
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Checkpoint {file_path} does not exist.")

        model = load_model(filepath=file_path, *args, **kwargs)
        return cls(model=model)
