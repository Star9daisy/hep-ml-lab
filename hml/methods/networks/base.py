from __future__ import annotations

import shutil
import sys
from io import StringIO
from pathlib import Path
from typing import Any

import yaml
from keras import Model, Sequential
from keras.models import load_model


class KerasMethod:
    def __init__(self, metadata: dict[str, Any], model: Sequential | Model):
        self.metadata = metadata
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
        if not isinstance(results, dict):
            raise TypeError(f"Expected dict, got {type(results)}")  # pragma: no cover

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

    def save(self, dir_path: str | Path) -> None:
        dir_path = Path(dir_path)
        metadata_path = dir_path / "metadata.yml"
        model_path = dir_path / "model.h5"

        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True)

        # Save metadata
        with open(metadata_path, "w") as f:
            yaml.dump(self.metadata, f, indent=2)

        # Save model
        self.model.save(
            filepath=model_path,
            save_format="h5",
        )

    @classmethod
    def load(cls, dir_path: str | Path) -> KerasMethod:
        dir_path = Path(dir_path)
        metadata_path = dir_path / "metadata.yml"
        model_path = dir_path / "model.h5"

        if not dir_path.exists():
            raise FileNotFoundError(f"Checkpoint {dir_path} does not exist.")
        if not metadata_path.exists() or not model_path.exists():
            raise TypeError(
                f"Checkpoint {dir_path} is not a valid KerasMethod checkpoint or it has been corrupted."
            )

        with open(metadata_path, "r") as f:
            metadata = yaml.safe_load(f)

        model = load_model(filepath=model_path, compile=False)
        method = cls(**metadata)
        method.model = model
        return method
