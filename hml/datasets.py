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
    dirpath: str

    def save(self, exist_ok: bool = False):
        dirpath = Path(self.dirpath)
        dirpath.mkdir(parents=True, exist_ok=exist_ok)

        metadata = {
            "feature_names": self.feature_names,
            "target_names": self.target_names,
            "description": self.description,
            "dirpath": self.dirpath,
        }
        with open(dirpath / "metadata.yml", "w") as f:
            yaml.dump(metadata, f)
        np.savez(dirpath / "metadata.yml", data=self.data, target=self.target)

    @classmethod
    def from_path(cls, dirpath: str) -> Dataset:
        dirpath = Path(dirpath)
        with open(dirpath / "metadata.yml", "r") as f:
            metadata = yaml.safe_load(f)
        dataset = np.load(dirpath / "dataset.npz")

        return cls(
            data=dataset["data"],
            target=dataset["target"],
            feature_names=metadata["feature_names"],
            target_names=metadata["target_names"],
            description=metadata["description"],
            dirpath=metadata["dirpath"],
        )
