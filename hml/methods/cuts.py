from __future__ import annotations

import json
from functools import reduce
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class CutBasedAnalysis:
    def __init__(
        self,
        name: str = "cut_based_analysis",
        bins: int = 100,
    ):
        self.name = name
        self.bins = bins

        self.signal_locations = []
        self.cuts = []
        self.best_accurcies = []

    def compile(
        self,
        optimizer: str = "auto",
        loss: None = None,
        metrics: None = None,
    ) -> None:
        pass

    def fit(self, x_train: np.ndarray, y_train: np.ndarray) -> None:
        signal = x_train[y_train == 1]
        background = x_train[y_train == 0]

        for i in range(signal.shape[1]):
            signal_location, cut, best_accuracy = find_best_cut(
                signal[:, i], background[:, i], bins=self.bins
            )
            self.signal_locations.append(signal_location)
            self.cuts.append(cut)
            self.best_accurcies.append(best_accuracy)

    def predict(self, x: np.ndarray) -> np.ndarray:
        cut_results = []
        for i, (cut, location) in enumerate(zip(self.cuts, self.signal_locations)):
            if location == "left":
                result = x[:, i] < cut
            elif location == "right":
                result = x[:, i] > cut
            elif location == "middle":
                result = (cut[0] < x[:, i]) & (x[:, i] < cut[1])
            elif location == "both_sides":
                result = (x[:, i] < cut[0]) | (x[:, i] > cut[1])
            cut_results.append(result)

        return reduce(np.logical_and, cut_results).astype(np.int16)

    def summary(self) -> str:
        output = [f"Model: {self.name}"]
        for i, (cut, location) in enumerate(zip(self.cuts, self.signal_locations), start=1):
            if location == "left":
                output.append(f"Cut{i}: Feature < {cut[0]}")
            elif location == "right":
                output.append(f"Cut{i}: Feature > {cut[0]}")
            elif location == "middle":
                output.append(f"Cut{i}: {cut[0, 0]} < Feature < {cut[1, 0]}")
            elif location == "both_sides":
                output.append(f"Cut{i}: Feature < {cut[0, 0]} or Feature > {cut[1, 0]}")

        return "\n".join(output)

    def save(self, path: str, suffix: str = ".json"):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix != suffix:
            path = path.with_suffix(suffix)

        output = {}
        for i, (cut, location) in enumerate(zip(self.cuts, self.signal_locations), start=1):
            if location == "left":
                output[f"Cut{i}"] = f"Feature < {cut[0]}"
            elif location == "right":
                output[f"Cut{i}"] = f"Feature > {cut[0]}"
            elif location == "middle":
                output[f"Cut{i}"] = f"{cut[0, 0]} < Feature < {cut[1, 0]}"
            elif location == "both_sides":
                output[f"Cut{i}"] = f"Feature < {cut[0, 0]} or Feature > {cut[1, 0]}"

        with open(path, "w") as f:
            json.dump(output, f, indent=4)


def find_best_cut(sig, bkg, bins=100):
    _, bins_edges = np.histogram(np.concatenate([sig, bkg]), bins=bins)
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
    best_index = np.argmax([accuracy_left, accuracy_right, accuracy_middle, accuracy_both])
    location = ["left", "right", "middle", "both_sides"][best_index]
    best_accuracy = [accuracy_left, accuracy_right, accuracy_middle, accuracy_both][best_index]
    best_cut = [cut_left, cut_right, cut_middle, cut_both][best_index]

    return location, best_cut, best_accuracy


def plot_cuts(sig, bkg, bins, cut, signal_location):
    # Plot the signal and background histograms
    plt.hist(sig, bins=bins, alpha=0.5, label="Signal", color="blue")
    plt.hist(bkg, bins=bins, alpha=0.5, label="Background", color="orange")

    cut = np.squeeze(cut)
    if signal_location == "left":
        plt.axvline(cut, color="red", linestyle="--", label=f"Optimal cut: feature < {cut:.2f}")
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]], plt.gca().get_xlim()[0], cut, color="red", alpha=0.5
        )

    elif signal_location == "right":
        plt.axvline(cut, color="red", linestyle="--", label=f"Optimal cut: feature > {cut:.2f}")
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]], cut, plt.gca().get_xlim()[1], color="red", alpha=0.5
        )

    elif signal_location == "middle":
        plt.axvline(
            cut[0], color="red", linestyle="--", label=f"Optimal cut: feature > {cut[0]:.2f}"
        )
        plt.axvline(
            cut[1], color="red", linestyle="--", label=f"Optimal cut: feature < {cut[1]:.2f}"
        )
        plt.fill_betweenx([0, plt.gca().get_ylim()[1]], cut[0], cut[1], color="red", alpha=0.5)

    else:
        plt.axvline(
            cut[0], color="red", linestyle="--", label=f"Optimal cut: feature < {cut[0]:.2f}"
        )
        plt.axvline(
            cut[1], color="red", linestyle="--", label=f"Optimal cut: feature > {cut[1]:.2f}"
        )
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]], plt.gca().get_xlim()[0], cut[0], color="red", alpha=0.5
        )
        plt.fill_betweenx(
            [0, plt.gca().get_ylim()[1]], cut[1], plt.gca().get_xlim()[1], color="red", alpha=0.5
        )

    plt.xlabel("Value")
    plt.ylabel("Counts")
    plt.legend(loc="upper right")
    plt.title("Signal, Background")
    plt.show()
