from __future__ import annotations

import pickle
from importlib import import_module
from pathlib import Path
from typing import Any

from keras.metrics import Metric
from keras.utils import to_categorical
from numpy import ndarray
from sklearn.ensemble import GradientBoostingClassifier

from ..preprocessing import is_categorical


class BoostedDecisionTree:
    def __init__(
        self,
        name: str = "boosted_decision_tree",
        learning_rate: float = 0.1,
        n_estimators: int = 100,
        **kwargs,
    ):
        self._name = name
        self.model = GradientBoostingClassifier(
            learning_rate=learning_rate, n_estimators=n_estimators, **kwargs
        )
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators

    @property
    def name(self) -> str:
        return self._name

    @property
    def n_parameters(self) -> int:
        max_nodes_per_tree = 2 ** (self.model.max_depth + 1) - 1
        max_parameters = max_nodes_per_tree * self.model.n_estimators
        return max_parameters

    def compile(
        self,
        optimizer: None = None,
        loss: str = "log_loss",
        metrics: None | list[Metric] = None,
    ) -> None:
        self.optimizer = optimizer
        self.model.set_params(loss=loss)
        self.loss = getattr(import_module("sklearn.metrics"), loss)
        self.metrics = metrics

    def fit(self, x: ndarray, y: ndarray, verbose: int = 1, **kwargs) -> dict[str, list[float]]:
        if is_categorical(y):
            encoding = "one-hot"
            y = y.argmax(axis=1)
        else:
            encoding = "ordinal"

        self._history = {"loss": []}
        if self.metrics is not None:
            for metric in self.metrics:
                self._history[metric.name] = []

            def _monitor(i, model, local_variables):
                y_true = local_variables["y"]
                y_pred = local_variables["raw_predictions"]
                y_prob = model._loss._raw_prediction_to_proba(y_pred)

                progress = f"Iter {i + 1}/{model.n_estimators}"
                train_loss = (
                    f"loss: {model._loss(y_true, y_pred, local_variables['sample_weight']):.4f}"
                )

                metric_results = []
                if encoding == "one-hot":
                    y_true = to_categorical(y_true)
                for metric in self.metrics:
                    metric.update_state(y_true, y_prob)
                    metric_results.append(f"{metric.name}: {metric.result():.4f}")
                    self._history[metric.name].append(metric.result().numpy())

                if verbose > 0:
                    print(f"{progress} - {train_loss} - {' - '.join(metric_results)}")
                return False

            self.model.fit(x, y, monitor=_monitor, **kwargs)

        else:
            self.model.fit(x, y, **kwargs)

        self._history["loss"] = self.model.train_score_.tolist()
        return self._history

    def predict(self, x: ndarray) -> ndarray:
        return self.model.predict_proba(x)

    def evaluate(self, x: ndarray, y: ndarray, verbose: int = 1) -> dict[str, list[float]]:
        y_true = y
        y_pred = self.predict(x)

        results = {}
        results["loss"] = self.loss(y_true, y_pred)
        if self.metrics is not None:
            for metric in self.metrics:
                metric.update_state(y_true, y_pred)
                results[metric.name] = metric.result().numpy()

        if verbose > 0:
            print(" - ".join([f"{k}: {v:.4f}" for k, v in results.items()]))

        return results

    def summary(self, return_string: bool = False, deep=False, **kwargs) -> str | None:
        output = ["Model: {}".format(self.name)]
        for parameter, value in self.model.get_params(deep=deep, **kwargs).items():
            output.append(f"- {parameter}: {value}")

        if return_string:
            return "\n".join(output)
        else:
            print("\n".join(output))

    def save(self, file_path: str | Path, overwrite: bool = True) -> None:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path.suffix != ".pkl":
            file_path = file_path.with_suffix(".pkl")

        if file_path.exists() and not overwrite:
            raise FileExistsError(f"Checkpoint {file_path} already exists.")

        with open(file_path, "wb") as f:
            pickle.dump(self.model, f)

    @classmethod
    def load(cls, file_path: str | Path, *args, **kwargs) -> BoostedDecisionTree:
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Checkpoint {file_path} does not exist.")

        with open(file_path, "rb") as f:
            model = pickle.load(f, *args, **kwargs)
            return cls(model=model)
