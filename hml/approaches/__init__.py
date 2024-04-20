import pickle
from pathlib import Path

from keras.saving import load_model

from .cuts import Cut, CutAndCount, CutLayer
from .networks import SimpleCNN, SimpleGNN, SimpleMLP
from .trees import GradientBoostedDecisionTree


def load_approach(filepath):
    filepath = Path(filepath)

    if filepath.suffix == ".keras":
        return load_model(filepath)

    elif filepath.suffix == ".pickle":
        with open(filepath, "rb") as f:
            return pickle.load(f)

    else:
        raise ValueError("Unknown file format")
