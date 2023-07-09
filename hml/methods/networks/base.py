from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from typing import Any

from keras import Model
from keras.engine.functional import Functional
from keras.engine.sequential import Sequential
from keras.models import load_model


class KerasMethod:
    def __init__(self, model: Sequential | Functional | Model):
        self.model = model

    @property
    def name(self) -> str:
        return self.model.name

    @property
    def n_parameters(self) -> int:
        return self.model.count_params()

    def compile(self, optimizer="rmsprop", loss=None, metrics=None, *args, **kwargs) -> None:
        self.model.compile(optimizer, loss, metrics, *args, **kwargs)

    def fit(self, x: Any, y: Any, *args, **kwargs) -> dict[str, list[float]]:
        history = self.model.fit(x, y, *args, **kwargs)
        return history.history

    def predict(self, x: Any, *args, **kwargs) -> Any:
        return self.model.predict(x, *args, **kwargs)

    def evaluate(self, x: Any, y: Any, **kwargs) -> dict[str, list[float]]:
        results = self.model.evaluate(x, y, return_dict=True, **kwargs)
        for metric, value in results.items():
            results[metric] = [value]
        return results

    def summary(self, return_string: bool = False, *args, **kwargs) -> str | None:
        if return_string:
            stdout = sys.stdout
            output_buffer = StringIO()
            sys.stdout = output_buffer
            self.model.summary(*args, **kwargs)
            sys.stdout = stdout
            return output_buffer.getvalue()
        else:
            self.model.summary(*args, **kwargs)

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
