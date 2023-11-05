from __future__ import annotations

from typing import Protocol

import numpy as np

from .types import Path, PathLike


class Dataset(Protocol):
    """A protocol for datasets used in HML.

    This protocol follows the same style as the `sklearn.utils.Bunch` class and
    is simpified to quickly save and load datasets.
    """

    @property
    def samples(self) -> np.ndarray:
        """The samples (data points) of the dataset."""
        ...

    @property
    def targets(self) -> np.ndarray:
        """The targets (integer labels) of the dataset."""
        ...

    @property
    def description(self) -> str:
        """The description of the dataset."""
        ...

    def save(self, filepath: PathLike, overwrite: bool) -> None:
        """Save the dataset to a .npz file.

        It is required to save `_type` to distinguish between different datasets
        and load them correctly via `load_dataset` method.
        """
        ...

    @classmethod
    def load(cls, filepath: PathLike) -> Dataset:
        """Load the dataset from a .npz file."""
        ...


def load_dataset(filepath: PathLike) -> Dataset:
    """Load a dataset from a .npz file."""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File {filepath} does not exist")

    data = np.load(filepath)

    if (_type := data.get("_type").item()) is None:
        raise ValueError(
            f"No `_type` key in {filepath}. Cannot load dataset anonymously, "
            f"try to determine the type of dataset and load it directly from "
            f"the corresponding class."
        )

    if _type not in DATASET_CLASSES:
        raise ValueError(
            f"Unknown dataset type {_type}. Available types: "
            f"{', '.join(DATASET_CLASSES.keys())}"
        )

    return DATASET_CLASSES[_type].load(filepath)


class TabularDataset:
    """A tabular dataset.

    This is a class for tabular datasets. Samples are from 1D representation to
    build this 2D representation.

    Parameters
    ----------
    samples : np.ndarray
        The samples (data points) of the dataset.
    targets : np.ndarray
        The targets (integer labels) of the dataset.
    feature_names : list[str]
        The names of the features.
    target_names : list[str]
        The names of the targets.
    description : str
        The description of the dataset.
    """

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


DATASET_CLASSES = {
    "tabular": TabularDataset,
}
