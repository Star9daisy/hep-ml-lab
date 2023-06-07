from __future__ import annotations

import pickle
from pathlib import Path

from numpy import ndarray
from sklearn.ensemble import GradientBoostingClassifier


class BoostedDecisionTree:
    def __init__(
        self,
        name: str = "boosted_decision_tree",
        learning_rate: float = 0.1,
        n_estimators: int = 100,
        **kwargs,
    ):
        self.name = name
        self.model = GradientBoostingClassifier

        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.other_params = kwargs

    def compile(
        self,
        optimizer: None = None,
        loss: str = "log_loss",
        metrics: None = None,
    ):
        self.model = self.model(
            loss=loss,
            learning_rate=self.learning_rate,
            n_estimators=self.n_estimators,
            **self.other_params,
        )

    def fit(self, x_train: ndarray, y_train: ndarray):
        self.model.fit(x_train, y_train)

    def predict(self, x: ndarray) -> ndarray:
        return self.model.predict(x)

    def predict_proba(self, x: ndarray) -> ndarray:
        return self.model.predict_proba(x)

    def summary(self):
        print("Model: {}".format(self.name))
        for parameter, value in self.model.get_params(deep=False).items():
            print(f"- {parameter}: {value}")

    def save(self, path: str, suffix: str = ".pkl"):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix != suffix:
            path = path.with_suffix(suffix)

        with open(path, "wb") as f:
            pickle.dump(self.model, f)
