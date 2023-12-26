from typing import Callable

import keras
import tensorflow as tf
from keras import losses, ops


@keras.saving.register_keras_serializable()
class CutAndCount(keras.Model):
    def __init__(self, n_bins: int = 50, name: str = "cut_and_count"):
        super().__init__(name=name)
        self.n_bins = self.add_weight(
            name="n_bins",
            shape=(),
            dtype=tf.int32,
            initializer=keras.initializers.Constant(n_bins),
            trainable=False,
        )

    def build(self, input_shape):
        self.cuts = self.add_weight(
            name="cuts",
            shape=(input_shape[-1], 2),
            dtype=tf.float32,
            initializer=keras.initializers.Zeros(),
            trainable=False,
        )
        self.cases = self.add_weight(
            name="cases",
            shape=(input_shape[-1],),
            dtype=tf.int32,
            initializer=keras.initializers.Zeros(),
            trainable=False,
        )
        self.built = True

    def train_step(self, data):
        x, y = data

        # Call the model once to create the weights
        if not self.built:
            _ = self(x)

        # Loop over all features to get best results for each feature
        # I: (n_samples,), (n_samples, ?)
        # O: (n_features, 3): (cut0, cut1, case)
        results = tf.map_fn(
            lambda x: self._get_result(x, y),
            tf.transpose(x),
            fn_output_signature=tf.float32,
        )

        cases = tf.cast(results[:, 2], tf.int32)  # type: ignore
        self.cases.assign(cases)
        self.cuts.assign(results[:, :2])  # type: ignore
        y_pred = self(x)

        loss = self.compute_loss(y=y, y_pred=y_pred)
        # self.compiled_metrics.update_state(y, y_pred)  # type: ignore

        # return {m.name: m.result() for m in self.metrics}
        for metric in self.metrics:
            if metric.name == "loss":
                metric.update_state(loss)
            else:
                metric.update_state(y, y_pred)

        return {m.name: m.result() for m in self.metrics}

    @tf.function
    def _get_result(self, x, y):  # pragma: no cover
        # Find the min and max of the feature to get the bin edges
        # bin_edges: (n_bins+1,)
        x_min, x_max = tf.reduce_min(x), tf.reduce_max(x)
        bin_edges = tf.linspace(x_min, x_max, self.n_bins + 1)

        # Ensure y is a 1d tensor to perform as a boolean mask
        y_ = tf.cond(
            tf.rank(y) > 1,
            lambda: tf.argmax(y, 1, tf.int32),
            lambda: tf.cast(y, tf.int32),
        )

        # Get the histogram of each class
        x0 = tf.gather(x, tf.where(y_ == 0)[:, 0])
        x1 = tf.gather(x, tf.where(y_ == 1)[:, 0])
        hist0 = tf.histogram_fixed_width(x0, [x_min, x_max], self.n_bins)
        hist1 = tf.histogram_fixed_width(x1, [x_min, x_max], self.n_bins)

        # Find the candidate cuts on the boundary of the two classes
        # For the 0 class
        curr_case0 = hist0 > hist1
        next_case0 = tf.roll(curr_case0, shift=-1, axis=0)
        is_on_boundary0 = tf.math.logical_xor(curr_case0[:-1], next_case0[:-1])
        is_not_empty0 = hist0[:-1] > 0
        is_candidate0 = tf.math.logical_and(is_on_boundary0, is_not_empty0)
        candidate_indices0 = tf.where(is_candidate0)[:, 0] + 1
        candidates0 = tf.gather(bin_edges, candidate_indices0)

        # For the 1 class
        curr_case1 = hist1 > hist0
        next_case1 = tf.roll(curr_case1, shift=-1, axis=0)
        is_on_boundary1 = tf.math.logical_xor(curr_case1[:-1], next_case1[:-1])
        is_not_empty1 = hist1[:-1] > 0
        is_candidate1 = tf.math.logical_and(is_on_boundary1, is_not_empty1)
        candidate_indices1 = tf.where(is_candidate1)[:, 0] + 1
        candidates1 = tf.gather(bin_edges, candidate_indices1)

        # Use unique to remove duplicates
        candidates = tf.unique(tf.concat([candidates0, candidates1], axis=0))[0]

        # Add the max if candidate is only one
        candidates = tf.cond(
            tf.size(candidates) == 1,
            lambda: tf.concat([candidates, [x_max]], axis=0),
            lambda: candidates,
        )

        # Pair the candidates
        i, j = tf.meshgrid(candidates, candidates)
        mask = tf.math.less(i, j)
        i, j = tf.boolean_mask(i, mask), tf.boolean_mask(j, mask)
        candidate_pairs = tf.stack([i, j], axis=1)  # (n_pairs, 2)

        # Loop over all pairs to get best cases
        # I: (n_samples,), (n_samples, ?), (n_pairs, 2)
        # O: (n_pairs, 2): (loss, case)
        losses_and_cases = tf.map_fn(
            lambda pair: self._get_min_loss_and_case(x, y, pair),
            candidate_pairs,
            fn_output_signature=tf.float32,
        )

        # Find the minimum loss for all pairs per feature and take the first
        # candidate as cut
        # (n_pairs,) -> ()
        min_loss = tf.reduce_min(losses_and_cases[:, 0])  # type: ignore
        min_index = tf.where(tf.equal(losses_and_cases[:, 0], min_loss))[0, 0]  # type: ignore
        cut, case = candidate_pairs[min_index], losses_and_cases[min_index, 1]  # type: ignore

        # Finally, pack the cut and case into a tensor and return it
        result = tf.stack([cut[0], cut[1], case], axis=0)

        return result

    @tf.function
    def _get_min_loss_and_case(self, x, y, candidate_pair):  # pragma: no cover
        # I: (n_samples,), (n_samples, ?), (2,)
        cut0 = candidate_pair[0]
        cut1 = candidate_pair[1]

        # For each pair, calculate the loss of the four cases
        # Case 0: signal on the left
        on_left = x <= cut0  # (n_samples,)
        y_pred0 = tf.where(on_left, 1.0, 0.0)  # (n_samples,)
        # Turn the predictions into one-hot encoding
        y_pred0 = tf.concat([1 - y_pred0[:, None], y_pred0[:, None]], axis=1)
        loss0 = self.compute_loss(y=y, y_pred=y_pred0)
        # self.compiled_loss.reset_state()  # type: ignore

        # Case 1: signal on the right
        on_right = x >= cut0
        y_pred1 = tf.where(on_right, 1.0, 0.0)
        y_pred1 = tf.concat([1 - y_pred1[:, None], y_pred1[:, None]], axis=1)
        loss1 = self.compute_loss(y=y, y_pred=y_pred1)
        # self.compiled_loss.reset_state()  # type: ignore

        # Case 2: signal in the middle
        in_middle = tf.math.logical_and(x >= cut0, x <= cut1)
        y_pred2 = tf.where(in_middle, 1.0, 0.0)
        y_pred2 = tf.concat([1 - y_pred2[:, None], y_pred2[:, None]], axis=1)
        loss2 = self.compute_loss(y=y, y_pred=y_pred2)
        # self.compiled_loss.reset_state()  # type: ignore

        # Case 3: signal on both sides
        on_both_sides = tf.math.logical_or(x <= cut0, x >= cut1)
        y_pred3 = tf.where(on_both_sides, 1.0, 0.0)
        y_pred3 = tf.concat([1 - y_pred3[:, None], y_pred3[:, None]], axis=1)
        loss3 = self.compute_loss(y=y, y_pred=y_pred3)
        # self.compiled_loss.reset_state()  # type: ignore

        losses_and_cases = tf.concat(
            [
                [[loss0, 0]],
                [[loss1, 1]],
                [[loss2, 2]],
                [[loss3, 3]],
            ],
            axis=0,
        )

        # Find the minimum loss and return it with the corresponding case
        min_loss = tf.reduce_min(losses_and_cases[:, 0])  # type: ignore
        min_index = tf.where(tf.equal(losses_and_cases[:, 0], min_loss))[0, 0]  # type: ignore
        return losses_and_cases[min_index]  # (2,)

    def call(self, x):  # pragma: no cover
        left = x <= self.cuts[:, 0]  # (n_samples, n_features)
        right = x >= self.cuts[:, 0]
        middle = tf.logical_and(self.cuts[:, 0] <= x, x <= self.cuts[:, 1])
        both_sides = tf.logical_or(x <= self.cuts[:, 0], x >= self.cuts[:, 1])
        conditions = tf.stack(
            [left, right, middle, both_sides], axis=-1
        )  # (n_samples, n_features, 4)

        feature_indices = tf.range(tf.shape(x)[1])
        cases_indices = tf.cast(self.cases, tf.int32)
        index_pairs = tf.stack(
            [feature_indices, cases_indices], axis=-1
        )  # (n_features, 2)

        y_pred_per_feature = tf.map_fn(
            lambda index_pair: self.get_pred_per_feature(conditions, index_pair),
            index_pairs,
            fn_output_signature=tf.bool,
        )  # (n_features, n_samples)
        y_pred_per_feature = tf.transpose(y_pred_per_feature)  # (n_samples, n_features)
        y_pred = tf.reduce_all(y_pred_per_feature, axis=-1)  # (n_samples,)
        y_pred = tf.cast(y_pred, tf.float32)
        y_pred = tf.stack([1 - y_pred, y_pred], axis=-1)  # type: ignore
        return y_pred

    # conditions: (n_samples, n_features, 4)
    # indices: (n_features, 2)
    def get_pred_per_feature(self, conditions, indices):
        return conditions[:, indices[0], indices[1]]

    def summary(self, line_length=None, **kwargs):
        super().summary(line_length=line_length, **kwargs)
        print(f"n_bins: {self.n_bins.numpy()}")
        print("cuts:")
        for i, (cuts, case) in enumerate(zip(self.cuts, self.cases), 1):
            if case == 0:
                print(f"  #{i}: x <= {cuts[0]:.4f}")
            elif case == 1:
                print(f"  #{i}: x >= {cuts[0]:.4f}")
            elif case == 2:
                print(f"  #{i}: {cuts[0]:.4f} <= x <= {cuts[1]:.4f}")
            else:
                print(f"  #{i}: x <= {cuts[0]:.4f} or x >= {cuts[1]:.4f}")


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


class CutLayer(keras.layers.Layer):
    def __init__(
        self,
        cut=None,
        case=None,
        n_bins=50,
        feature_id=0,
        loss_fn: Callable | str = "binary_crossentropy",
    ):
        super().__init__()

        self.n_bins = n_bins
        self.feature_id = feature_id

        self.loss_fn = losses.get(loss_fn)

        self.cut = self.add_weight(
            shape=(2,),
            initializer="zeros",
            trainable=False,
        )
        if cut is not None:
            self.cut.assign(cut)

        self.case = self.add_weight(
            shape=(),
            initializer="zeros",
            trainable=False,
        )
        if case is not None:
            self.case.assign(case)

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

            self.cut.assign(ops.array([lower, upper]))
            self.case.assign(min_case)

        y_pred = ops.cond(
            ops.equal(self.case, 0),
            lambda: ops.where(x <= self.cut[0], 1, 0),
            lambda: ops.cond(
                ops.equal(self.case, 1),
                lambda: ops.where(x >= self.cut[0], 1, 0),
                lambda: ops.cond(
                    ops.equal(self.case, 2),
                    lambda: ops.where(
                        ops.logical_and(x >= self.cut[0], x <= self.cut[1]), 1, 0
                    ),
                    lambda: ops.where(
                        ops.logical_or(x <= self.cut[0], x >= self.cut[1]), 1, 0
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
