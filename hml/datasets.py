from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy
import numpy as np
import yaml


@dataclass
class Dataset:
    """Dataset class for storing data and metadata.

    Parameters
    ----------
    data: numpy.ndarray
        Data array.
    target: array
        Target array.
    feature_names: list[str]
        List of feature names.
    target_names: list[str]
        List of target names.
    description: str
        Description of dataset.
    dir_path: str
        Path to dataset directory.

    """

    data: numpy.ndarray
    target: numpy.ndarray
    feature_names: list[str]
    target_names: list[str]
    description: str
    dir_path: str | Path

    def __post_init__(self):
        self.dir_path = Path(self.dir_path)

    def save(self, exist_ok: bool = False):
        """Save dataset to disk."""
        dir_path = Path(self.dir_path)
        dir_path.mkdir(parents=True, exist_ok=exist_ok)

        # Pack metadata
        metadata = {
            "feature_names": self.feature_names,
            "target_names": self.target_names,
            "description": self.description,
            "dir_path": str(self.dir_path),
        }

        # Save metadata as yaml and dataset as npz
        with open(dir_path / "metadata.yml", "w") as f:
            yaml.dump(metadata, f)
        np.savez(dir_path / f"dataset.npz", data=self.data, target=self.target)

    @classmethod
    def load(cls, dir_path: str | Path) -> Dataset:
        """Load dataset from disk."""
        dir_path = Path(dir_path)
        with open(dir_path / "metadata.yml", "r") as f:
            metadata = yaml.safe_load(f)
        dataset = np.load(dir_path / "dataset.npz")

        return cls(
            data=dataset["data"],
            target=dataset["target"],
            feature_names=metadata["feature_names"],
            target_names=metadata["target_names"],
            description=metadata["description"],
            dir_path=metadata["dir_path"],
        )
