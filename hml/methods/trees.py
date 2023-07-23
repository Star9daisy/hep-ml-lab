from __future__ import annotations

import pickle
import shutil
from importlib import import_module
from pathlib import Path

import yaml
from keras.metrics import Metric
from keras.utils import to_categorical
from numpy import ndarray
from sklearn.ensemble import GradientBoostingClassifier

from ..preprocessing import is_categorical


class BoostedDecisionTree:
    """A wrapper around sklearn's GradientBoostingClassifier.

    Parameters
    ----------
    name : str, optional
        Name of the model. Default is "boosted_decision_tree".
    learning_rate : float, optional
        Learning rate shrinks the contribution of each tree.
    n_estimators : int, optional
        The number of boosting stages to perform. Default is 100.
    **kwargs
        Other parameters to pass to the GradientBoostingClassifier.
    """

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
        self.other_parameters = kwargs

        self.metadata = {
            "name": self.name,
            "learning_rate": self.learning_rate,
            "n_estimators": self.n_estimators,
        }
        self.metadata.update(self.other_parameters)

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
                loss = f"loss: {model._loss(y_true, y_pred, local_variables['sample_weight']):.4f}"

                metric_results = []
                if encoding == "one-hot":
                    y_true = to_categorical(y_true)
                for metric in self.metrics:
                    metric.update_state(y_true, y_prob)
                    metric_results.append(f"{metric.name}: {metric.result():.4f}")
                    self._history[metric.name].append(metric.result().numpy())

                if verbose > 0:
                    print(f"{progress} - {loss} - {' - '.join(metric_results)}")
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

        for k, v in results.items():
            results[k] = [v]

        return results

    def summary(self, return_string: bool = False, deep=False, **kwargs) -> str | None:
        output = ['Model: "{}"'.format(self.name)]
        for parameter, value in self.model.get_params(deep=deep, **kwargs).items():
            output.append(f"- {parameter}: {value}")

        if return_string:
            return "\n".join(output)
        else:
            print("\n".join(output))

    def save(self, dir_path: str | Path) -> None:
        dir_path = Path(dir_path)
        metadata_path = dir_path / "metadata.yml"
        model_path = dir_path / "model.pkl"

        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True)

        # Save metadata
        with open(metadata_path, "w") as f:
            yaml.dump(self.metadata, f, indent=2)

        # Save model
        with open(model_path, "wb") as f:
            pickle.dump(self.model, f)

    @classmethod
    def load(cls, dir_path: str | Path) -> BoostedDecisionTree:
        dir_path = Path(dir_path)
        metadata_path = dir_path / "metadata.yml"
        model_path = dir_path / "model.pkl"

        if not dir_path.exists():
            raise FileNotFoundError(f"Checkpoint {dir_path} does not exist.")
        if not metadata_path.exists() or not model_path.exists():
            raise TypeError(
                f"Checkpoint {dir_path} is not a valid BoostedDecisionTree checkpoint or it has been corrupted."
            )

        with open(metadata_path, "r") as f:
            metadata = yaml.safe_load(f)
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        method = cls(**metadata)
        method.model = model
        return method
