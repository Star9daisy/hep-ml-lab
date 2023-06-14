from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml
from numpy import ndarray


@dataclass
class Dataset:
    data: ndarray
    target: ndarray
    feature_names: list[str]
    target_names: list[str]
    description: str
    dataset_dir: str

    def save(self, exist_ok: bool = False):
        dataset_dir = Path(self.dataset_dir)
        dataset_dir.mkdir(parents=True, exist_ok=exist_ok)

        # Pack metadata
        metadata = {
            "feature_names": self.feature_names,
            "target_names": self.target_names,
            "description": self.description,
            "dirpath": self.dataset_dir,
        }

        # Save metadata as yaml and dataset as npz
        with open(dataset_dir / "metadata.yml", "w") as f:
            yaml.dump(metadata, f)
        np.savez(dataset_dir / f"dataset.npz", data=self.data, target=self.target)

    @classmethod
    def load(cls, dataset_dir: str) -> Dataset:
        dataset_dir = Path(dataset_dir)
        with open(dataset_dir / "metadata.yml", "r") as f:
            metadata = yaml.safe_load(f)
        dataset = np.load(dataset_dir / "dataset.npz")

        return cls(
            data=dataset["data"],
            target=dataset["target"],
            feature_names=metadata["feature_names"],
            target_names=metadata["target_names"],
            description=metadata["description"],
            dataset_dir=metadata["dataset_dir"],
        )
