from typing import Any, Protocol


class Model(Protocol):
    def compile(self, optimizer: Any, loss: Any, metrics: Any):
        pass

    def fit(self, x_train: Any, y_train: Any):
        pass

    def summary(self):
        pass

    def save(self, path: str, suffix: str):
        pass
