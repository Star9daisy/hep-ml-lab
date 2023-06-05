import numpy as np


class Dataset:
    def __init__(self) -> None:
        self._data = []
        self._target = []
        self.target_names = []

    def add(self, data, target):
        self._data.append(data)
        self._target.append(target)

    @property
    def data(self):
        return np.array(self._data)

    @property
    def target(self):
        return np.array(self._target)
