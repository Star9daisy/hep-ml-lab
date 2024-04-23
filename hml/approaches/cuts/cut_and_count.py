from __future__ import annotations

import keras
from keras import ops

from hml.operations import ops_histogram_fixed_width, ops_unique

from .cut_layer import CutLayer


@keras.saving.register_keras_serializable()
class CutAndCount(keras.Model):
    def __init__(
        self,
        n_observables: int,
        n_bins: int = 50,
        topology="parallel",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.n_observables = n_observables
        self.topology = topology
        self.n_bins = n_bins
        self.cut_layers = [CutLayer(feature_id=i) for i in range(n_observables)]

    def train_step(self, data):
        x, y = data
        y_pred = self(x, y)  # (N, 2)
        loss = self.compute_loss(y=y, y_pred=y_pred)

        for metric in self.metrics:
            if metric.name == "loss":
                metric.update_state(loss)
            else:
                metric.update_state(y, y_pred)

        return {m.name: m.result() for m in self.metrics}

    def call(self, x, y=None):
        if self.topology == "parallel":
            y_pred = ops.squeeze(self.parallel_call(x, y))  # (N,)
        elif self.topology == "sequential":
            y_pred = ops.squeeze(self.sequential_call(x, y))  # (N,)
        else:
            raise NotImplementedError()

        return ops.one_hot(ops.cast(y_pred, "int32"), num_classes=2)

    def parallel_call(self, x, y=None):
        y_preds = []

        for cut_layer in self.cut_layers:
            ix = ops.take(x, cut_layer.feature_id, axis=-1)

            if y is not None:
                cut_left, cut_right, case = self.find_best_cut(ix, y)
                cut_layer._cut_left.assign(cut_left)
                cut_layer._cut_right.assign(cut_right)
                cut_layer._case.assign(case)

            y_pred = cut_layer(ix)
            y_preds.append(y_pred)

        return keras.layers.Multiply()(y_preds)

    def sequential_call(self, x, y=None, show_cut_mark=False):
        y_pred = ops.ones(ops.shape(x)[0])
        mask = y_pred
        for cut_layer in self.cut_layers:
            ix = ops.take(x, cut_layer.feature_id, axis=-1)

            if y is not None:
                masked_x = ops.take(ix, ops.squeeze(ops.where(mask >= 0), 0))
                masked_y = ops.take(
                    y, ops.squeeze(ops.where(mask >= 0), 0), 0
                )  # should keep y as original
                cut_left, cut_right, case = self.find_best_cut(masked_x, masked_y)
                cut_layer._cut_left.assign(cut_left)
                cut_layer._cut_right.assign(cut_right)
                cut_layer._case.assign(case)

            mask = cut_layer.apply_cut(ix, -1)
            y_pred = ops.logical_and(y_pred, ops.where(mask < 0, 0.0, 1.0))
            y_pred = ops.cast(y_pred, "float32")

        return y_pred

    def find_best_cut(self, x, y):
        if ops.ndim(y) == 2:
            if ops.ndim(ops.squeeze(y)) == 2:
                iy = ops.argmax(y, -1)
            else:
                iy = ops.squeeze(y)
        else:
            iy = y

        x_min = ops.min(x)
        x_max = ops.max(x)
        bin_edges = ops.linspace(x_min, x_max, self.n_bins + 1)

        is_bkg = ops.squeeze(ops.where(ops.equal(iy, 0)), 0)
        is_sig = ops.squeeze(ops.where(ops.equal(iy, 1)), 0)

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
            ops.equal(ops.shape(candidates)[0], 1),
            lambda: ops.append(candidates, x_max),
            lambda: candidates,
        )
        i, j = ops.meshgrid(candidates, candidates)  # type: ignore
        i, j = i[i < j], j[i < j]
        candidate_pairs = ops.stack([i, j], 1)
        losses_and_cases = ops.vectorized_map(
            lambda pair: self._get_min_loss_and_case(x, y, pair, self.compute_loss),
            candidate_pairs,
        )
        min_index = ops.argmin(ops.take(losses_and_cases, 0, 1))
        # min_loss = losses_and_cases[min_index, 0]  # type: ignore
        min_case = losses_and_cases[min_index, 1]  # type: ignore

        lower = candidate_pairs[min_index, 0]  # type: ignore
        upper = candidate_pairs[min_index, 1]  # type: ignore

        return lower, upper, min_case

    def _get_min_loss_and_case(self, x, y, candidate_pair, loss_fn):  # pragma: no cover
        # I: (n_samples,), (n_samples, ?), (2,)
        cut0 = candidate_pair[0]
        cut1 = candidate_pair[1]

        # For each pair, calculate the loss of the four cases
        # Case 0: signal on the left
        on_left = ops.less_equal(x, cut0)  # (n_samples,)
        y_pred0 = ops.where(on_left, 1.0, 0.0)  # (n_samples,)
        y_pred0 = ops.one_hot(ops.cast(y_pred0, "int32"), num_classes=2)
        loss0 = loss_fn(y=y, y_pred=y_pred0)

        # Case 1: signal on the right
        on_right = ops.greater_equal(x, cut0)
        y_pred1 = ops.where(on_right, 1.0, 0.0)
        y_pred1 = ops.one_hot(ops.cast(y_pred1, "int32"), num_classes=2)
        loss1 = loss_fn(y=y, y_pred=y_pred1)

        # Case 2: signal in the middle
        in_middle = ops.logical_and(x >= cut0, x <= cut1)
        y_pred2 = ops.where(in_middle, 1.0, 0.0)
        y_pred2 = ops.one_hot(ops.cast(y_pred2, "int32"), num_classes=2)
        loss2 = loss_fn(y=y, y_pred=y_pred2)

        # Case 3: signal on both sides
        on_both_sides = ops.logical_or(x <= cut0, x >= cut1)
        y_pred3 = ops.where(on_both_sides, 1.0, 0.0)
        y_pred3 = ops.one_hot(ops.cast(y_pred3, "int32"), num_classes=2)
        loss3 = loss_fn(y=y, y_pred=y_pred3)

        # The cases 0, 1, 2, 3 are corresponding to the four possible cases:
        # left, right, middle, both sides
        min_case = ops.argmin([loss0, loss1, loss2, loss3])
        min_loss = ops.min([loss0, loss1, loss2, loss3])

        return ops.append(min_loss, min_case)  # (2,)

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "n_observables": self.n_observables,
                "n_bins": self.n_bins,
                "topology": self.topology,
            }
        )

        return config
