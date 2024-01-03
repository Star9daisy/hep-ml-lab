import re
from typing import Callable

import awkward as ak
import keras
import pandas as pd
from keras import losses, ops

from hml.utils import get_observable


@keras.saving.register_keras_serializable()
class CutLayer(keras.Layer):
    def __init__(
        self,
        cut: str | None = None,
        count=0,
        cut_left: float | None = None,
        cut_right: float | None = None,
        case: float | None = None,
        n_bins=50,
        feature_id=0,
        loss_fn: Callable | str = "binary_crossentropy",
        **kwargs,
    ):
        if cut is not None:
            super().__init__(name=cut, **kwargs)
        else:
            super().__init__(**kwargs)
            self.name = self.name.replace("cut_layer", "Observable")

        self._cut = cut
        self._count = count

        self._cut_left = self.add_weight(
            shape=(),
            initializer="zeros",
            trainable=False,
        )
        if cut_left is not None:
            self._cut_left.assign(cut_left)

        self._cut_right = self.add_weight(
            shape=(),
            initializer="zeros",
            trainable=False,
        )
        if cut_right is not None:
            self._cut_right.assign(cut_right)

        self._case = self.add_weight(
            shape=(),
            initializer="zeros",
            trainable=False,
        )
        if case is not None:
            self._case.assign(case)

        self.n_bins = n_bins
        self.feature_id = feature_id
        self.loss_fn = losses.get(loss_fn)

    def is_passed(self, event):
        if not isinstance(self._cut, str):
            raise TypeError(f"is_passed should be used when specify a cut manually")

        cut_exp = self._cut

        cuts_per_obs = cut_exp.strip().split("and")
        cuts_per_obs = [i.strip().split("or") for i in cuts_per_obs]
        cuts_per_obs = [i for j in cuts_per_obs for i in j]
        cuts_per_obs = [i.strip().split("xor") for i in cuts_per_obs]
        cuts_per_obs = [i for j in cuts_per_obs for i in j]

        obs_pattern = r"\b(?!\d+\b)(?!\d*\.\d+\b)\S+\b"
        obs_names = [re.findall(obs_pattern, i)[0] for i in cuts_per_obs]
        obs_list = [get_observable(i).read(event) for i in obs_names]
        for obs in obs_list:
            if "var" in obs.shape:
                obs.value = ak.flatten(obs.value)

        for i in obs_names:
            cut_exp = cut_exp.replace(i, f"`{i}`")

        df = pd.DataFrame({obs.name: obs.value for obs in obs_list})

        if len(df) == len(df.query(cut_exp)):
            return True
        else:
            self._count += 1
            return False

    def call(self, inputs, targets=None, sample_weight=None):
        x = inputs
        y = targets
        x = ops.take(x, self.feature_id, -1)
        self.sample_weight = sample_weight

        if y is not None and self.loss_fn is not None:
            y = ops.argmax(y, -1) if ops.ndim(y) > 1 else y  # type: ignore

            x_min = ops.min(x)
            x_max = ops.max(x)
            bin_edges = ops.linspace(x_min, x_max, self.n_bins + 1)

            is_bkg = ops.squeeze(ops.where(ops.equal(y, 0)), 0)
            is_sig = ops.squeeze(ops.where(ops.equal(y, 1)), 0)

            x0 = ops.take(x, is_bkg)
            x1 = ops.take(x, is_sig)

            hist0 = ops_histogram_fixed_width(x0, [x_min, x_max], self.n_bins)
            hist1 = ops_histogram_fixed_width(x1, [x_min, x_max], self.n_bins)

            curr_case0 = ops.greater(hist0, hist1)[:-1]  # type: ignore
            next_case0 = ops.greater(hist0, hist1)[1:]  # type: ignore
            is_on_boundary0 = ops.logical_xor(curr_case0, next_case0)
            is_not_empty0 = hist0[:-1] > 0  # type: ignore
            is_candidate0 = ops.logical_and(is_on_boundary0, is_not_empty0)
            candidate_indices0 = ops.add(ops.squeeze(ops.where(is_candidate0), 0), 1)
            candidates0 = ops.take(bin_edges, candidate_indices0)

            curr_case1 = ops.greater(hist1, hist0)[:-1]  # type: ignore
            next_case1 = ops.greater(hist1, hist0)[1:]  # type: ignore
            is_on_boundary1 = ops.logical_xor(curr_case1, next_case1)
            is_not_empty1 = hist1[:-1] > 0  # type: ignore
            is_candidate1 = ops.logical_and(is_on_boundary1, is_not_empty1)
            candidate_indices1 = ops.add(ops.squeeze(ops.where(is_candidate1), 0), 1)
            candidates1 = ops.take(bin_edges, candidate_indices1)

            candidates = ops_unique(ops.concatenate([candidates0, candidates1], 0))
            candidates = ops.cond(
                ops.equal(ops.shape(candidates), (1,)),
                lambda: ops.append(candidates, x_max),
                lambda: candidates,
            )
            i, j = ops.meshgrid(candidates, candidates)  # type: ignore
            i, j = i[i < j], j[i < j]
            candidate_pairs = ops.stack([i, j], 1)
            losses_and_cases = ops.vectorized_map(
                lambda pair: self._get_min_loss_and_case(x, y, pair, self.loss_fn),
                candidate_pairs,
            )
            min_index = ops.argmin(ops.take(losses_and_cases, 0, 1))
            min_loss = losses_and_cases[min_index, 0]  # type: ignore
            min_case = losses_and_cases[min_index, 1]  # type: ignore

            lower = candidate_pairs[min_index, 0]  # type: ignore
            upper = candidate_pairs[min_index, 1]  # type: ignore

            # self.cut.assign(ops.array([lower, upper]))
            # self.case.assign(min_case)
            self._cut_left.assign(lower)
            self._cut_right.assign(upper)
            self._case.assign(min_case)

        y_pred = ops.cond(
            ops.equal(self._case, 0),
            lambda: ops.where(x <= self._cut_left, 1, 0),
            lambda: ops.cond(
                ops.equal(self._case, 1),
                lambda: ops.where(x >= self._cut_left, 1, 0),
                lambda: ops.cond(
                    ops.equal(self._case, 2),
                    lambda: ops.where(
                        ops.logical_and(x >= self._cut_left, x <= self._cut_right), 1, 0
                    ),
                    lambda: ops.where(
                        ops.logical_or(x <= self._cut_left, x >= self._cut_right), 1, 0
                    ),
                ),
            ),
        )
        return y_pred

    def _get_min_loss_and_case(self, x, y, candidate_pair, loss_fn):  # pragma: no cover
        # I: (n_samples,), (n_samples, ?), (2,)
        cut0 = candidate_pair[0]
        cut1 = candidate_pair[1]

        # For each pair, calculate the loss of the four cases
        # Case 0: signal on the left
        on_left = ops.less_equal(x, cut0)  # (n_samples,)
        y_pred0 = ops.where(on_left, 1.0, 0.0)  # (n_samples,)
        loss0 = loss_fn(y, y_pred0, self.sample_weight)

        # Case 1: signal on the right
        on_right = ops.greater_equal(x, cut0)
        y_pred1 = ops.where(on_right, 1.0, 0.0)
        loss1 = loss_fn(y, y_pred1, self.sample_weight)

        # Case 2: signal in the middle
        in_middle = ops.logical_and(x >= cut0, x <= cut1)
        y_pred2 = ops.where(in_middle, 1.0, 0.0)
        loss2 = loss_fn(y, y_pred2, self.sample_weight)

        # Case 3: signal on both sides
        on_both_sides = ops.logical_or(x <= cut0, x >= cut1)
        y_pred3 = ops.where(on_both_sides, 1.0, 0.0)
        loss3 = loss_fn(y, y_pred3, self.sample_weight)

        # The cases 0, 1, 2, 3 are corresponding to the four possible cases:
        # left, right, middle, both sides
        min_case = ops.argmin([loss0, loss1, loss2, loss3])
        min_loss = ops.min([loss0, loss1, loss2, loss3])

        return ops.append(min_loss, min_case)  # (2,)

    def compute_output_shape(self, input_shape):
        return input_shape

    @property
    def cut(self):
        if self._cut is not None:
            return self._cut
        else:
            if self.case == 0:
                return f"{self.name} <= {self.cut_left:.5f}"
            elif self.case == 1:
                return f"{self.name} >= {self.cut_left:.5f}"
            elif self.case == 2:
                return f"{self.cut_left:.5f} <= {self.name} <= {self.cut_right:.5f}"
            else:
                return f"{self.name} <= {self.cut_left:.5f} or {self.name} >= {self.cut_right:.5f}"

    @property
    def count(self):
        return ops.convert_to_numpy(self._count)

    @property
    def cut_left(self):
        return ops.convert_to_numpy(self._cut_left)

    @property
    def cut_right(self):
        return ops.convert_to_numpy(self._cut_right)

    @property
    def case(self):
        return ops.convert_to_numpy(self._case)

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "cut": self._cut,
                # "cut_left": self.cut_left,
                # "cut_right": self.cut_right,
                # "case": self.case,
                "count": self._count,
                "n_bins": self.n_bins,
                "feature_id": self.feature_id,
                "loss_fn": self.loss_fn,
            }
        )
        return config


def ops_histogram_fixed_width(values, value_range, nbins, dtype="int32"):
    value_min, value_max = value_range
    bin_edges = ops.linspace(value_min, value_max, nbins + 1)
    lower = bin_edges[:-1]  # type: ignore
    upper = bin_edges[1:]  # type: ignore

    return ops.fori_loop(
        0,
        nbins,
        lambda i, s: ops.scatter_update(
            s,
            [[i]],
            [
                ops.count_nonzero(
                    ops.where(
                        ops.logical_and(lower[i] <= values, values <= upper[i]), 1, 0
                    )
                )
            ],
        ),
        ops.zeros((nbins,), dtype=dtype),
    )


def ops_unique(tensor):
    sorted_tensor, sorted_indices = ops.sort(tensor), ops.argsort(tensor)
    selection = ops.not_equal(sorted_tensor[1:], sorted_tensor[:-1])  # type: ignore
    selection = ops.add(ops.squeeze(ops.where(selection), 0), 1)
    unique_indices = ops.append([0], selection)

    try:
        unique_elements = ops.take(sorted_tensor, unique_indices)
        unique_indices = ops.take(sorted_indices, unique_indices)
        return unique_elements
    except:
        return ops.array([0])
