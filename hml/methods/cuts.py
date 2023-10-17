from __future__ import annotations

import json
import re
import shutil
from collections import OrderedDict
from functools import reduce
from itertools import product
from pathlib import Path

import keras
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import yaml
from keras.losses import Loss
from keras.metrics import Metric
from keras.utils import to_categorical

from ..new_observables import get_observable


class CutAndCount:
    """Cut and count method.

    This method is used to find the optimal cut for each feature. The optimal cut is defined as the
    cut that maximizes the accuracy of the classifier.

    For each feature, it first bins data into a given number of bins. Then, it tries to find the
    optimal cut by comparing the accuracy of the classifier for each bin edge and for four different
    cases:

    - left: signal < cut
    - right: signal > cut
    - middle: cut[0] < signal < cut[1]
    - both_sides: signal < cut[0] or signal > cut[1]

    Parameters
    ----------
    name : str, optional
        Name of the method. Default is "cut_and_count".
    n_bins : int, optional
        Number of bins to use for the cut and count method. Default is 100.

    Attributes
    ----------
    name : str
        Name of the method.
    n_parameters : int
        Number of parameters of the method.
    signal_locations : list[str]
        Location of the signal for each feature. Can be "left", "right", "middle", or "both_sides".
    cuts : list[list[float]]
        Optimal cut for each feature.
    metadata : dict
        Metadata of the method.
    model : dict
        Model of the method.
    """

    def __init__(
        self,
        name: str = "cut_and_count",
        n_bins: int = 100,
    ):
        self._name = name
        self.n_bins = n_bins

        self.signal_locations = []
        self.cuts = []

        self.metadata = {
            "name": self.name,
            "n_bins": self.n_bins,
        }
        self.model = {
            "signal_locations": self.signal_locations,
            "cuts": self.cuts,
        }

    @property
    def name(self) -> str:
        return self._name

    @property
    def n_parameters(self) -> int:
        return len(self.cuts)

    def compile(
        self,
        optimizer: None = None,
        loss: Loss | None = None,
        metrics: None | list[Metric] = None,
    ) -> None:
        self.optimizer = optimizer

        if loss is None:
            raise ValueError("Loss function must be specified.")

        self.loss = loss
        self.metrics = metrics

    def fit(
        self, x: np.ndarray, y: np.ndarray, signal_id: int = 1, verbose: int = 1
    ) -> dict[str, list[float]]:
        if y.ndim == 2:
            _y = y.argmax(axis=1)
        else:
            _y = y
        signal = x[_y == signal_id]
        background = x[_y != signal_id]

        self._history = {"loss": []}
        if self.metrics is not None:
            for metric in self.metrics:
                self._history[metric.name] = []

        for i in range(signal.shape[1]):
            # TODO: Add loss to find_best_cut
            signal_location, cut, best_accuracy = find_best_cut(
                signal[:, i], background[:, i], n_bins=self.n_bins
            )
            self.signal_locations.append(signal_location)
            self.cuts.append(cut)
            # self.best_accurcies.append(best_accuracy)

            progress = f"Cut {i + 1}/{signal.shape[1]}"
            loss = f"loss: {self.loss(y, self.predict(x)):.4f}"
            self._history["loss"].append(self.loss(y, self.predict(x)).numpy())

            metric_results = []
            if self.metrics is not None:
                for metric in self.metrics:
                    metric.update_state(y, self.predict(x))
                    metric_results.append(f"{metric.name}: {metric.result():.4f}")
                    self._history[metric.name].append(metric.result().numpy())

            if verbose > 0:
                print(" - ".join([progress, loss] + metric_results))

        return self._history

    def predict(self, x: np.ndarray) -> np.ndarray:
        cut_results = []
        for i, (cut, location) in enumerate(zip(self.cuts, self.signal_locations)):
            if location == "left":
                result = x[:, i] < cut
            elif location == "right":
                result = x[:, i] > cut
            elif location == "middle":
                result = (cut[0] < x[:, i]) & (x[:, i] < cut[1])
            else:
                result = (x[:, i] < cut[0]) | (x[:, i] > cut[1])
            cut_results.append(result)

        y_pred_raw = reduce(np.logical_and, cut_results).astype(np.int16)
        return to_categorical(y_pred_raw)

    def evaluate(
        self, x: np.ndarray, y: np.ndarray, verbose: int = 1
    ) -> dict[str, list[float]]:
        y_true = y
        y_pred = self.predict(x)

        results = {}
        results["loss"] = self.loss(y_true, y_pred).numpy()
        if self.metrics is not None:
            for metric in self.metrics:
                metric.update_state(y_true, y_pred)
                results[metric.name] = metric.result().numpy()

        if verbose > 0:
            print(" - ".join([f"{k}: {v:.4f}" for k, v in results.items()]))

        for k, v in results.items():
            results[k] = [v]

        return results

    def summary(self, return_string: bool = False) -> str | None:
        output = [f'Model: "{self.name}"']
        for i, (cut, location) in enumerate(
            zip(self.cuts, self.signal_locations), start=1
        ):
            if location == "left":
                output.append(f"Cut{i}: Feature < {cut[0]}")
            elif location == "right":
                output.append(f"Cut{i}: Feature > {cut[0]}")
            elif location == "middle":
                output.append(f"Cut{i}: {cut[0][0]} < Feature < {cut[1][0]}")
            else:
                output.append(f"Cut{i}: Feature < {cut[0][0]} or Feature > {cut[1][0]}")

        if return_string:
            return "\n".join(output)
        else:
            print("\n".join(output))

    def save(self, dir_path: str | Path) -> None:
        dir_path = Path(dir_path)
        metadata_path = dir_path / "metadata.yml"
        model_path = dir_path / "model.json"

        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True)

        # Save metadata
        with open(metadata_path, "w") as f:
            yaml.dump(self.metadata, f, indent=2)

        # Save model
        with open(model_path, "w") as f:
            json.dump(self.model, f, indent=4)

    @classmethod
    def load(cls, dir_path: str | Path) -> CutAndCount:
        dir_path = Path(dir_path)
        metadata_path = dir_path / "metadata.yml"
        model_path = dir_path / "model.json"

        if not dir_path.exists():
            raise FileNotFoundError(f"Checkpoint {dir_path} does not exist.")
        if not metadata_path.exists() or not model_path.exists():
            raise TypeError(
                f"Checkpoint {dir_path} is not a valid CutAndCount checkpoint or it has been corrupted."
            )

        with open(metadata_path, "r") as f:
            metadata = yaml.safe_load(f)
        with open(model_path, "r") as f:
            model = json.load(f)

        method = cls(metadata["name"], metadata["n_bins"])
        method.signal_locations = model["signal_locations"]
        method.cuts = model["cuts"]
        return method


def find_best_cut(sig: np.ndarray, bkg: np.ndarray, n_bins=100):
    _, bins_edges = np.histogram(np.concatenate([sig, bkg]), bins=n_bins)
    cuts = bins_edges[..., None]
    sig = sig[None, ...]
    bkg = bkg[None, ...]

    # Signal is left
    tp = (sig <= cuts).sum(1)
    fp = (bkg <= cuts).sum(1)
    tn = (bkg > cuts).sum(1)
    fn = (sig > cuts).sum(1)
    accuracy = (tp + tn) / (tp + fp + tn + fn)
    accuracy_left = accuracy.max()
    cut_left = cuts[accuracy.argmax()]

    # Signal is right
    tp = (sig >= cuts).sum(1)
    fp = (bkg >= cuts).sum(1)
    tn = (bkg < cuts).sum(1)
    fn = (sig < cuts).sum(1)
    accuracy = (tp + tn) / (tp + fp + tn + fn)
    accuracy_right = accuracy.max()
    cut_right = cuts[accuracy.argmax()]

    # For two cut case, define lower and upper limits first
    limits = []
    for i, v in enumerate(cuts[1:-1]):
        limits += list(product([v], cuts[i + 1 :]))

    limits = np.array(limits)
    lower, upper = limits[:, 0], limits[:, 1]

    # Signal is at the middle
    tp = np.logical_and(sig >= lower, sig <= upper).sum(1)
    fp = np.logical_and(bkg >= lower, bkg <= upper).sum(1)
    tn = np.logical_or(bkg < lower, bkg > upper).sum(1)
    fn = np.logical_or(sig < lower, sig > upper).sum(1)

    accuracy = (tp + tn) / (tp + fp + tn + fn)
    accuracy_middle = accuracy.max()
    cut_middle = limits[accuracy.argmax()]

    # Signal is at both sides
    tp = np.logical_or(sig <= lower, sig >= upper).sum(1)
    fp = np.logical_or(bkg <= lower, bkg >= upper).sum(1)
    tn = np.logical_and(bkg > lower, bkg < upper).sum(1)
    fn = np.logical_and(sig > lower, sig < upper).sum(1)

    accuracy = (tp + tn) / (tp + fp + tn + fn)
    accuracy_both = accuracy.max()
    cut_both = limits[accuracy.argmax()]

    # Return the best cut
    best_index = np.argmax(
        [accuracy_left, accuracy_right, accuracy_middle, accuracy_both]
    )
    location = ["left", "right", "middle", "both_sides"][best_index]
    best_accuracy = [accuracy_left, accuracy_right, accuracy_middle, accuracy_both][
        best_index
    ]
    best_cut = [cut_left, cut_right, cut_middle, cut_both][best_index]
    best_cut = best_cut.tolist()

    return location, best_cut, best_accuracy


def plot_cuts(sig, bkg, bins, cut, signal_location):
    # Plot the signal and background histograms
    plt.hist(sig, bins=bins, alpha=0.5, label="Signal", color="blue")
    plt.hist(bkg, bins=bins, alpha=0.5, label="Background", color="orange")

    cut = np.squeeze(cut)
    if signal_location == "left":
        plt.axvline(
            cut, color="red", linestyle="--", label=f"Optimal cut: feature < {cut:.2f}"
        )
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]],
            plt.gca().get_xlim()[0],
            cut,
            color="red",
            alpha=0.5,
        )

    elif signal_location == "right":
        plt.axvline(
            cut, color="red", linestyle="--", label=f"Optimal cut: feature > {cut:.2f}"
        )
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]],
            cut,
            plt.gca().get_xlim()[1],
            color="red",
            alpha=0.5,
        )

    elif signal_location == "middle":
        plt.axvline(
            cut[0],
            color="red",
            linestyle="--",
            label=f"Optimal cut: feature > {cut[0]:.2f}",
        )
        plt.axvline(
            cut[1],
            color="red",
            linestyle="--",
            label=f"Optimal cut: feature < {cut[1]:.2f}",
        )
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]], cut[0], cut[1], color="red", alpha=0.5
        )

    else:
        plt.axvline(
            cut[0],
            color="red",
            linestyle="--",
            label=f"Optimal cut: feature < {cut[0]:.2f}",
        )
        plt.axvline(
            cut[1],
            color="red",
            linestyle="--",
            label=f"Optimal cut: feature > {cut[1]:.2f}",
        )
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]],
            plt.gca().get_xlim()[0],
            cut[0],
            color="red",
            alpha=0.5,
        )
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]],
            cut[1],
            plt.gca().get_xlim()[1],
            color="red",
            alpha=0.5,
        )

    plt.xlabel("Value")
    plt.ylabel("Counts")
    plt.legend(loc="upper right")
    plt.title("Signal, Background")
    plt.show()


class Filter:
    def __init__(self, cuts: list[str]) -> None:
        self.cuts = cuts
        self.stat = OrderedDict({cut: 0 for cut in cuts})

    def read(self, event):
        self.event = event
        return self

    def passed(self):
        def _replace_with_value(match):
            observable_name = match.group(0)  # complete match
            value = get_observable(observable_name).read(self.event).value

            if value is not None:
                return str(value)
            else:
                return "np.nan"

        for cut in self.cuts:
            modified_string = re.sub(
                r"\b(?!\d+\b)([\w\d_]+)\.([\w\d_]+)\b", _replace_with_value, cut
            )
            if eval(modified_string) is False:
                self.stat[cut] += 1
                return False

        return True


@keras.saving.register_keras_serializable(package="CutAndCount")
class NewCutAndCount(keras.Model):
    def __init__(self, n_bins=5, name="cut_and_count"):
        super().__init__(name=name)
        self.n_bins = self.add_weight(
            name="n_bins",
            shape=(),
            dtype=tf.int32,
            trainable=False,
            initializer=tf.keras.initializers.Constant(n_bins),
        )
        self.cut = self.add_weight(
            name="cut",
            shape=(2,),
            dtype=tf.float32,
            trainable=False,
        )
        self.case = self.add_weight(
            name="case",
            shape=(),
            dtype=tf.int32,
            trainable=False,
        )

    def train_step(self, data):
        x_train, y_train = data

        x_min = tf.reduce_min(x_train)
        x_max = tf.reduce_max(x_train)

        edges = tf.linspace(x_min, x_max, self.n_bins)  # (n_bins,)
        edges = tf.expand_dims(edges, axis=1)  # (n_bins, 1)

        i, j = tf.meshgrid(edges, edges)

        # Filter out diagonal elements and pairs (i, j) where i >= j
        mask = tf.math.less(i, j)

        double_edges = tf.stack(
            [tf.boolean_mask(i, mask), tf.boolean_mask(j, mask)], axis=1
        )

        # losses = tf.vectorized_map(
        #     lambda e: self._compute_max_index(e, x_train, y_train), double_edges
        # )  # (n_edge_pairs, 4)
        losses = self._compute_max_index(double_edges, x_train, y_train)
        min_loss = tf.reduce_min(losses)
        min_indices = tf.where(losses == min_loss)
        min_indices = tf.cast(min_indices, tf.int32)
        self.case.assign(min_indices[0][1])  # type: ignore
        self.cut.assign(tf.gather(double_edges, min_indices[0][0]))  # type: ignore
        self.compiled_metrics.update_state(y_train, self(x_train))  # type: ignore

        for metric in self.metrics:
            if metric.name == "loss":
                metric.update_state(min_loss)
            else:
                metric.update_state(y_train, self(x_train))

        results = {m.name: m.result() for m in self.metrics}
        return results

    def call(self, x):
        y_pred = self._get_y_pred(x, self.case)
        return y_pred

    @tf.function
    def _get_y_pred(self, x, direction):
        branch_fns = {
            0: lambda: self._case_left(x),
            1: lambda: self._case_right(x),
            2: lambda: self._case_middle(x),
            3: lambda: self._case_both(x),
        }
        return tf.switch_case(tf.identity(direction), branch_fns)

    @tf.function
    def _case_left(self, x):
        y_pred = x <= self.cut[0]
        y_pred = tf.cast(y_pred, tf.float32)
        return y_pred

    @tf.function
    def _case_right(self, x):
        y_pred = x >= self.cut[0]
        y_pred = tf.cast(y_pred, tf.float32)
        return y_pred

    @tf.function
    def _case_middle(self, x):
        y_pred = tf.logical_and(x >= self.cut[0], x <= self.cut[1])
        y_pred = tf.cast(y_pred, tf.float32)
        return y_pred

    @tf.function
    def _case_both(self, x):
        y_pred = tf.logical_or(x <= self.cut[0], x >= self.cut[1])
        y_pred = tf.cast(y_pred, tf.float32)
        return y_pred

    @tf.function
    def _compute_max_index(self, edges, x_train, y_train):
        # left
        y_pred_left = tf.cast(
            x_train <= edges[:, 0], tf.float32
        )  # (n_samples, n_pairs)
        loss_left = self.compute_loss(y=y_train, y_pred=y_pred_left)  # (n_pairs,)
        self.compiled_loss.reset_state()  # type: ignore
        # right
        y_pred_right = tf.cast(x_train >= edges[:, 0], tf.float32)
        loss_right = self.compute_loss(y=y_train, y_pred=y_pred_right)
        self.compiled_loss.reset_state()  # type: ignore
        # middle
        y_pred_middle = tf.logical_and(x_train >= edges[:, 0], x_train <= edges[:, 1])
        y_pred_middle = tf.cast(y_pred_middle, tf.float32)
        loss_middle = self.compute_loss(y=y_train, y_pred=y_pred_middle)
        self.compiled_loss.reset_state()  # type: ignore
        # both sides
        y_pred_both = tf.logical_or(x_train <= edges[:, 0], x_train >= edges[:, 1])
        y_pred_both = tf.cast(y_pred_both, tf.float32)
        loss_both = self.compute_loss(y=y_train, y_pred=y_pred_both)
        self.compiled_loss.reset_state()  # type: ignore

        losses = tf.stack([loss_left, loss_right, loss_middle, loss_both], axis=1)

        return losses
