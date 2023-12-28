from pathlib import Path

import dill as pickle
import keras

from ..types import PathLike


def load_approach(filepath: PathLike, **kwargs):
    filepath = Path(filepath)

    if filepath.suffix == ".pickle":
        with open(filepath, "rb") as f:
            return pickle.load(f)
    else:
        return keras.models.load_model(filepath, **kwargs)
