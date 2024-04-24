from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Literal, NamedTuple

import dill as pickle
import keras
from numpy import ndarray
from numpy.random import RandomState
from sklearn.base import BaseEstimator
from sklearn.ensemble import GradientBoostingClassifier

KERAS_METRICS = {
    "binary_accuracy": keras.metrics.BinaryAccuracy,
    "categorical_accuracy": keras.metrics.CategoricalAccuracy,
    "sparse_categorical_accuracy": keras.metrics.SparseCategoricalAccuracy,
    "top_k_categorical_accuracy": keras.metrics.TopKCategoricalAccuracy,
    "sparse_top_k_categorical_accuracy": keras.metrics.SparseTopKCategoricalAccuracy,
    "binary_crossentropy": keras.metrics.BinaryCrossentropy,
    "category_crossentropy": keras.metrics.CategoricalCrossentropy,
    "sparse_category_crossentropy": keras.metrics.SparseCategoricalCrossentropy,
    "kullback_leibler_divergence": keras.metrics.KLDivergence,
    "poisson": keras.metrics.Poisson,
    "auc": keras.metrics.AUC,
    "precision": keras.metrics.Precision,
    "recall": keras.metrics.Recall,
    "true_positives": keras.metrics.TruePositives,
    "true_negatives": keras.metrics.TrueNegatives,
    "false_positives": keras.metrics.FalsePositives,
    "false_negatives": keras.metrics.FalseNegatives,
    "precision_at_recall": keras.metrics.PrecisionAtRecall,
    "sensitivity_at_specificity": keras.metrics.SensitivityAtSpecificity,
    "specificity_at_sensitivity": keras.metrics.SpecificityAtSensitivity,
}


class History(NamedTuple):
    history: dict[str, Any]


class GradientBoostedDecisionTree(GradientBoostingClassifier):
    def __init__(
        self,
        name: str = "gradient_boosted_decision_tree",
        *,
        loss: Literal["log_loss", "deviance", "exponential"] = "log_loss",
        learning_rate: float = 0.1,
        n_estimators: int = 100,
        subsample: float = 1,
        criterion: Literal["friedman_mse", "squared_error"] = "friedman_mse",
        min_samples_split: float | int = 2,
        min_samples_leaf: float | int = 1,
        min_weight_fraction_leaf: float = 0,
        max_depth: int | None = 3,
        min_impurity_decrease: float = 0,
        init: str | BaseEstimator | None = None,
        random_state: int | RandomState | None = None,
        max_features: float | int | Literal["auto", "sqrt", "log2"] | None = None,
        verbose: int = 0,
        max_leaf_nodes: int | None = None,
        warm_start: bool = False,
        validation_fraction: float = 0.1,
        n_iter_no_change: int | None = None,
        tol: float = 0.0001,
        ccp_alpha: float = 0,
    ) -> None:
        super().__init__(
            loss=loss,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            subsample=subsample,
            criterion=criterion,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            max_depth=max_depth,
            min_impurity_decrease=min_impurity_decrease,
            init=init,
            random_state=random_state,
            max_features=max_features,
            verbose=verbose,
            max_leaf_nodes=max_leaf_nodes,
            warm_start=warm_start,
            validation_fraction=validation_fraction,
            n_iter_no_change=n_iter_no_change,
            tol=tol,
            ccp_alpha=ccp_alpha,
        )
        self.name = name
        self.metrics = []

    def compile(self, optimizer=None, loss="log_loss", metrics=None):
        self.optimizer = optimizer
        self.set_params(loss=loss)
        self.metrics = metrics or []

    def fit(
        self,
        x: ndarray,
        y: ndarray,
        validation_split: float = 0.0,
        validation_data: tuple[ndarray, ndarray] | None = None,
        sample_weight: ndarray | None = None,
        verbose: int = 1,
    ):
        is_categorical = y.ndim == 2
        pb = keras.utils.Progbar(self.n_estimators, verbose=verbose)  # type: ignore
        history = History(history=defaultdict(list))

        if validation_data is not None:
            self.x_val, self.y_val = validation_data
        elif validation_split != 0.0:
            self.x_val = x[-int(validation_split * len(x)) :]
            x = x[: -int(validation_split * len(x))]
            self.y_val = y[-int(validation_split * len(y)) :]
            y = y[: -int(validation_split * len(y))]

        self.metric_pairs = []
        for metric in self.metrics:
            if issubclass(type(metric), keras.metrics.Metric):
                self.metric_pairs.append((metric.name, metric))
            elif metric in KERAS_METRICS:
                self.metric_pairs.append((metric, KERAS_METRICS[metric]()))
            elif metric in ["accuracy", "acc"]:
                if is_categorical:
                    self.metric_pairs.append(
                        (metric, keras.metrics.CategoricalAccuracy())
                    )
                else:
                    self.metric_pairs.append(
                        (metric, keras.metrics.SparseCategoricalAccuracy())
                    )
            else:
                raise ValueError(f"Unknown metric: {metric}")

        def _monitor(i, model, local_variables):
            y_true = local_variables["y"]
            raw_pred = local_variables["raw_predictions"]

            if hasattr(model._loss, "predict_proba"):
                # This works in 1.4.2
                y_prob = model._loss.predict_proba(raw_pred)
            else:
                # This works in 1.3.0
                y_prob = model._loss._raw_prediction_to_proba(raw_pred)
            sample_weight = local_variables["sample_weight"]

            loss = model._loss(y_true, raw_pred, sample_weight)

            y_true = (
                y_true if not is_categorical else keras.utils.to_categorical(y_true)
            )

            # Train metrics
            train_values = [("loss", loss)]
            history.history["loss"].append(loss)
            for name, i in self.metric_pairs:
                i.reset_state()
                i.update_state(y_true, y_prob, sample_weight=sample_weight)
                train_values.append((name, i.result().numpy()))
                history.history[name].append(i.result().numpy())

            # Validation metrics
            val_values = []
            if validation_split != 0.0 or validation_data is not None:
                # Reshape y_val and change dtype to match the previous one
                y_true = (
                    self.y_val if self.y_val.ndim == 1 else self.y_val.argmax(axis=1)
                ).astype(y_true.dtype)  # (n_samples,)
                raw_pred = next(model._staged_raw_predict(self.x_val))  # (n_samples, 1)
                if hasattr(model._loss, "predict_proba"):
                    # This works in 1.4.2
                    y_prob = model._loss.predict_proba(raw_pred)
                else:
                    # This works in 1.3.0
                    y_prob = model._loss._raw_prediction_to_proba(raw_pred)
                # y_prob = model._loss._raw_prediction_to_proba(
                #     raw_pred
                # )  # (n_samples, n_classes)

                # ! sample_weight: (n_samples x (1 - validation_fraction),)
                # here the validation_fraction is a parameter of the parent class
                # print(y_true.shape, raw_pred.shape, y_prob.shape, sample_weight.shape)
                val_loss = model._loss(y_true, raw_pred)  # , sample_weight)
                val_values.append(("val_loss", val_loss))
                history.history["val_loss"].append(val_loss)

                for name, i in self.metric_pairs:
                    i.reset_state()
                    i.update_state(self.y_val, y_prob)
                    val_values.append(("val_" + name, i.result().numpy()))
                    history.history["val_" + name].append(i.result().numpy())

            pb.add(1, values=[("loss", loss)] + train_values + val_values)

            return False

        y = y if not is_categorical else y.argmax(axis=1)
        _ = super().fit(x, y, sample_weight, _monitor)
        return history

    def predict(self, x: ndarray, **kwargs) -> ndarray:
        return super().predict_proba(x)

    def summary(self, deep=False, **kwargs):
        output = [f'Model: "{self.name}"']
        for name, value in self.get_params(deep=deep, **kwargs).items():
            output.append(f"- {name}: {value}")

        print("\n".join(output))

    def save(
        self,
        filepath,
        overwrite=True,
        save_format: Literal["pickle"] = "pickle",
    ):
        filepath = Path(filepath)
        if filepath.suffix != "":
            save_format = filepath.suffix[1:]  # type: ignore

        filepath = filepath.with_suffix(f".{save_format}")
        if not overwrite and filepath.exists():
            raise FileExistsError(f"File already exists: {filepath}")

        with filepath.open("wb") as f:
            if save_format == "pickle":
                pickle.dump(self, f)
            else:
                raise ValueError(f"save_format {save_format} not supported")
