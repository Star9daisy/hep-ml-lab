from __future__ import annotations

from typing import Protocol

import numpy as np

from .types import Path, PathLike


class Dataset(Protocol):
    @property
    def samples(self) -> np.ndarray:
        ...

    @property
    def targets(self) -> np.ndarray:
        ...

    @property
    def description(self) -> str:
        ...

    def save(self, filepath: PathLike, overwrite: bool) -> None:
        ...

    @classmethod
    def load(cls, filepath: PathLike) -> Dataset:
        ...


def load_dataset(filepath: PathLike) -> Dataset:
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File {filepath} does not exist")

    data = np.load(filepath)
    _type = data["_type"].item()
    if _type == "tabular":
        return TabularDataset.load(filepath)
    else:
        raise ValueError(f"Invalid dataset type {_type}")


class TabularDataset:
    def __init__(
        self,
        samples: np.ndarray,
        targets: np.ndarray,
        feature_names: list[str],
        target_names: list[str],
        description: str,
    ) -> None:
        self._samples = samples
        self._targets = targets
        self._feature_names = feature_names
        self._target_names = target_names
        self._description = description

    @property
    def samples(self) -> np.ndarray:
        return self._samples

    @property
    def targets(self) -> np.ndarray:
        return self._targets

    @property
    def feature_names(self) -> list[str]:
        return self._feature_names

    @property
    def target_names(self) -> list[str]:
        return self._target_names

    @property
    def description(self) -> str:
        return self._description

    def save(self, filepath: PathLike, overwrite: bool = True) -> None:
        filepath = Path(filepath)
        if filepath.exists():
            if overwrite:
                filepath.unlink()
            else:
                raise FileExistsError(f"File {filepath} already exists")

        np.savez(
            filepath,
            samples=self.samples,
            targets=self.targets,
            feature_names=self.feature_names,
            target_names=self.target_names,
            description=self.description,
            _type="tabular",
        )

    @classmethod
    def load(cls, filepath: PathLike) -> TabularDataset:
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File {filepath} does not exist")

        data = np.load(filepath)
        return cls(
            samples=data["samples"],
            targets=data["targets"],
            feature_names=data["feature_names"],
            target_names=data["target_names"],
            description=data["description"].item(),
        )
