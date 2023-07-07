from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from keras.metrics import Metric
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
    ):
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.model.set_params(loss=loss)

    def fit(self, x: Any, y: Any, verbose: int = 1, *args, **kwargs) -> None:
        if self.metrics is not None:

            def _monitor(i, model, local_variables):
                y_true = local_variables["y"]
                y_pred = local_variables["raw_predictions"]
                y_prob = model._loss._raw_prediction_to_proba(y_pred)

                progress = f"Iter {i + 1}/{model.n_estimators}"
                train_loss = (
                    f"Loss: {model._loss(y_true, y_pred, local_variables['sample_weight']):.4f}"
                )

                metric_results = []
                for metric in self.metrics:
                    metric.update_state(y_true, y_prob)
                    metric_results.append(f"{metric.name}: {metric.result():.4f}")

                if verbose > 0:
                    print(f"{progress} - {train_loss} - {' - '.join(metric_results)}")
                return False

            self.model.fit(x, y, monitor=_monitor, *args, **kwargs)
        else:
            self.model.fit(x, y, *args, **kwargs)

    def predict(self, x: Any) -> ndarray:
        return self.model.predict_proba(x)

    def summary(self) -> str:
        output = ["Model: {}".format(self.name)]
        for parameter, value in self.model.get_params(deep=False).items():
            output.append(f"- {parameter}: {value}")
        return "\n".join(output)

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
