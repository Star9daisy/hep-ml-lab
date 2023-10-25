from __future__ import annotations

import json
import re
import shutil
from collections import OrderedDict
from functools import reduce
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import yaml
from keras.losses import Loss
from keras.metrics import Metric
from keras.utils import to_categorical
from tensorflow import keras

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
    def __init__(self, n_features: int, n_bins=100, name="cut_and_count"):
        super().__init__(name=name)
        self.n_bins = self.add_weight(
            name="n_bins",
            shape=(),
            dtype=tf.int32,
            trainable=False,
            initializer=tf.keras.initializers.Constant(n_bins),
        )
        self.cuts = self.add_weight(
            name="cuts",
            shape=(n_features, 2),
            dtype=tf.float32,
            trainable=False,
        )
        self.cases = self.add_weight(
            name="cases",
            shape=(n_features),
            dtype=tf.int32,
            trainable=False,
        )

    def train_step(self, data):
        samples, targets = data
        results = tf.map_fn(
            lambda x: self.get_result(x, targets), tf.transpose(samples)
        )
        min_losses = results[:, 0]
        loss = tf.reduce_mean(min_losses)
        cases = tf.cast(results[:, 1], tf.int32)
        cuts = results[:, 2:]

        self.cases.assign(cases)
        self.cuts.assign(cuts)
        self.compiled_metrics.update_state(targets, self(samples))

        for metric in self.metrics:
            if metric.name == "loss":
                metric.update_state(loss)
            else:
                metric.update_state(targets, self(samples))

        return {m.name: m.result() for m in self.metrics}

    def get_result(self, x, y):
        x_min = tf.reduce_min(x)
        x_max = tf.reduce_max(x)
        bin_edges = tf.linspace(x_min, x_max, self.n_bins + 1)

        samples_0 = x[y == 0]
        samples_1 = x[y == 1]
        hist_0 = tf.histogram_fixed_width(samples_0, [x_min, x_max], self.n_bins)
        hist_1 = tf.histogram_fixed_width(samples_1, [x_min, x_max], self.n_bins)

        # ---------------------------------------------------------------------------- #
        curr_selection_0 = hist_0 > hist_1
        next_selection_0 = tf.roll(curr_selection_0, shift=-1, axis=0)

        is_border_bin_0 = tf.math.logical_xor(
            curr_selection_0[:-1], next_selection_0[:-1]
        )
        is_not_empty_bin_0 = hist_0[:-1] > 0

        selection_0 = tf.logical_and(is_border_bin_0, is_not_empty_bin_0)
        border_edge_indices_0 = tf.where(selection_0) + 1
        edges_0 = tf.gather(bin_edges, border_edge_indices_0)
        edges_0 = tf.squeeze(edges_0)

        # ---------------------------------------------------------------------------- #
        curr_selection_1 = hist_1 > hist_0
        next_selection_1 = tf.roll(curr_selection_1, shift=-1, axis=0)

        is_border_bin_1 = tf.math.logical_xor(
            curr_selection_1[:-1], next_selection_1[:-1]
        )
        is_not_empty_bin_1 = hist_1[:-1] > 0

        selection_1 = tf.logical_and(is_border_bin_1, is_not_empty_bin_1)
        border_edge_indices_1 = tf.where(selection_1) + 1
        edges_1 = tf.gather(bin_edges, border_edge_indices_1)
        edges_1 = tf.squeeze(edges_1)

        # ---------------------------------------------------------------------------- #
        edges_0 = tf.reshape(edges_0, [-1])
        edges_1 = tf.reshape(edges_1, [-1])
        edges = tf.unique(tf.concat([edges_0, edges_1], 0))[0]
        i, j = tf.meshgrid(edges, edges)
        mask = tf.math.less(i, j)
        i, j = tf.boolean_mask(i, mask), tf.boolean_mask(j, mask)
        edge_pairs = tf.stack([i, j], axis=1)

        # To calculate losses for all edge pairs, we need to expand the samples to let
        # pair information at the 2nd axis
        x_expanded = tf.expand_dims(x, 1)  # (n_samples, 1)

        # ---------------------------------------------------------------------------- #
        on_left = x_expanded <= edge_pairs[:, 0]  # (n_samples, n_edges)
        y_pred_left = tf.where(on_left, 1.0, 0.0)  # (n_samples, n_edges)
        y_pred_left = tf.transpose(y_pred_left)  # (n_edges, n_samples)
        losses_left = self.compute_loss(
            y=tf.expand_dims(y, 0), y_pred=y_pred_left
        )  # (n_edges,)

        # ---------------------------------------------------------------------------- #
        on_right = x_expanded >= edge_pairs[:, 0]
        y_pred_right = tf.where(on_right, 1.0, 0.0)
        y_pred_right = tf.transpose(y_pred_right)
        losses_right = self.compute_loss(y=tf.expand_dims(y, 0), y_pred=y_pred_right)

        # ---------------------------------------------------------------------------- #
        in_middle = tf.logical_and(
            edge_pairs[:, 0] <= x_expanded, x_expanded <= edge_pairs[:, 1]
        )
        y_pred_middle = tf.where(in_middle, 1.0, 0.0)
        y_pred_middle = tf.transpose(y_pred_middle, (1, 0))
        losses_middle = self.compute_loss(y=tf.expand_dims(y, 0), y_pred=y_pred_middle)

        # ---------------------------------------------------------------------------- #
        on_both_sides = tf.logical_or(
            x_expanded <= edge_pairs[:, 0], x_expanded >= edge_pairs[:, 1]
        )
        y_pred_both = tf.where(on_both_sides, 1.0, 0.0)
        y_pred_both = tf.transpose(y_pred_both, (1, 0))
        losses_both = self.compute_loss(y=tf.expand_dims(y, 0), y_pred=y_pred_both)

        # ---------------------------------------------------------------------------- #
        losses = tf.stack([losses_left, losses_right, losses_middle, losses_both], 1)
        min_loss = tf.reduce_min(losses)
        min_index = tf.where(losses == min_loss)[0]
        cut = edge_pairs[min_index[0]]
        case = tf.cast(min_index[1], tf.float32)

        result = tf.stack([min_loss, case, cut[0], cut[1]])
        return result

    def call(self, x):
        left = x <= self.cuts[:, 0]
        right = x >= self.cuts[:, 0]
        middle = tf.logical_and(self.cuts[:, 0] <= x, x <= self.cuts[:, 1])
        both_sides = tf.logical_or(x <= self.cuts[:, 0], x >= self.cuts[:, 1])
        conditions = tf.stack([left, right, middle, both_sides], axis=-1)

        feature_indices = tf.range(4)
        cases_indices = tf.cast(self.cases, tf.int32)
        indices = tf.stack([feature_indices, cases_indices], axis=-1)

        y_pred_per_feature = tf.stack(
            [
                conditions[:, indices[0, 0], indices[0, 1]],
                conditions[:, indices[1, 0], indices[1, 1]],
                conditions[:, indices[2, 0], indices[2, 1]],
                conditions[:, indices[3, 0], indices[3, 1]],
            ],
            axis=-1,
        )
        y_pred = tf.reduce_all(y_pred_per_feature, axis=-1)
        y_pred = tf.cast(y_pred, tf.float32)
        return y_pred
