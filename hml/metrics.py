from __future__ import annotations

import keras
import numpy as np
import tensorflow as tf
from keras.metrics import Metric, SpecificityAtSensitivity


@tf.keras.utils.register_keras_serializable()
class MaxSignificance(Metric):
    """Calculate the maximum significance of a model's predictions.

    The significance is obtained by correctly identified signal events and incorrectly identified
    background events (tagged as signal). The formula taken here is:

    $$
    \\mathrm{significance} = \\sqrt{2 \\left( (S + B) \\ln \\left( 1 + \\frac{S}{B} \\right) - S \\right)}
    $$

    where $S$ is the number of correctly identified signal events (true positive) and $B$ is the
    number of incorrectly identified background events (false positive). Methods usually give
    probabilities for each class, so a threshold is needed to decide whether an event is signal or
    background. As a result, one threshold corresponds to one significance value. This is why this
    metric is called `MaxSignificance`: it calculates the maximum significance value among all the
    thresholds.

    Parameters
    ----------
    n_thresholds : int, optional
        Number of thresholds to use to compute the significance. The thresholds are uniformly
        distributed in the [0, 1] range. The default is 101.
    class_id : int, optional
        Class ID of the signal class. The default is 1.
    name : str, optional
        Name of the metric. The default is "max_significance".
    dtype : tf.dtypes.DType, optional
        Data type of the metric. The default is tf.float32.

    Attributes
    ----------
    thresholds : list[float]
        List of thresholds used to compute the significance.
    threshold : tf.Tensor
        Threshold that gives the maximum significance.
    threshold_index : tf.Tensor
        Index of the threshold that gives the maximum significance.
    max_significance : tf.Tensor
        Maximum significance value.

    Examples
    --------
    Standalone usage:
    >>> m = MaxSignificance()
    >>> m.update_state([0, 0, 1], [[0.8, 0.2], [0.3, 0.7], [0.4, 0.6]])
    >>> m.result().numpy()
    0.87897015
    >>> m = MaxSignificance()
    >>> m.update_state(
    ...    [[1, 0], [1, 0], [0, 1]],
    ...    [[0.8, 0.2], [0.3, 0.7], [0.4, 0.6]],
    ... )
    >>> m.result().numpy()
    0.87897015

    Usage with `compile` API:
    ```python
    model.compile(
        metrics=[MaxSignificance()],
    )
    ```
    """

    def __init__(
        self,
        n_thresholds: int = 101,
        class_id: int = 1,
        name: str = "max_significance",
        dtype: tf.dtypes.DType = tf.float32,
    ):
        super().__init__(name=name, dtype=dtype)

        # Compute thresholds in [0, 1] range
        # If the number of thresholds is 1, then the threshold is 0.5 and this metric is equivalent
        # to the significance metric.
        if n_thresholds == 1:
            self.thresholds = [0.5]
        else:
            thresholds = [i / (n_thresholds - 1) for i in range(n_thresholds - 1)]
            thresholds = [0.0] + thresholds + [1.0]
            self.thresholds = thresholds

        self.class_id = class_id
        self.true_positives = [
            self.add_weight(name=f"tp_{i}", initializer="zeros")
            for i, _ in enumerate(self.thresholds)
        ]
        self.false_positives = [
            self.add_weight(name=f"fp_{i}", initializer="zeros")
            for i, _ in enumerate(self.thresholds)
        ]

    def update_state(
        self,
        y_true: list | np.ndarray | tf.Tensor,
        y_pred: list | np.ndarray | tf.Tensor,
        sample_weight: list | np.ndarray | tf.Tensor | None = None,
    ):
        """Update the state of the metric in a batch-wise fashion.

        Parameters
        ----------
        y_true : list | np.ndarray | tf.Tensor
            True labels.
        y_pred : list | np.ndarray | tf.Tensor
            Predicted values (probabilities).
        sample_weight : list | np.ndarray | tf.Tensor | None, optional
            Sample weights. The default is None.
        """
        # Convert inputs to tensors
        # y_true should be a tensor of integers
        # y_pred and sample_weight follows self.dtype
        y_true = tf.convert_to_tensor(y_true, tf.int32)
        y_pred = tf.convert_to_tensor(y_pred, self.dtype)

        if sample_weight is not None:
            sample_weight = tf.convert_to_tensor(sample_weight, self.dtype)

        # Convert true labels to one-hot encoding if necessary
        # and ensure that the data type is the same as the predicted values
        if len(y_true.shape) == 1:
            n_classes = y_pred.shape[1]
            proper_y_true = tf.one_hot(y_true, n_classes, dtype=self.dtype)
        else:
            proper_y_true = tf.cast(y_true, self.dtype)

        # Get predicted values according to the signal class
        y_true_signal = tf.gather(proper_y_true, self.class_id, axis=1)
        y_pred_signal = tf.gather(y_pred, self.class_id, axis=1)

        # Compute true positives and false positives for each threshold
        for i, threshold in enumerate(self.thresholds):
            y_pred_thresholded = tf.cast(tf.greater_equal(y_pred_signal, threshold), tf.float32)
            if sample_weight is not None:
                self.true_positives[i].assign_add(
                    tf.reduce_sum(y_true_signal * y_pred_thresholded) * sample_weight
                )
                self.false_positives[i].assign_add(
                    tf.reduce_sum((1 - y_true_signal) * y_pred_thresholded) * sample_weight
                )
            else:
                self.true_positives[i].assign_add(tf.reduce_sum(y_true_signal * y_pred_thresholded))
                self.false_positives[i].assign_add(
                    tf.reduce_sum((1 - y_true_signal) * y_pred_thresholded)
                )

    def result(self) -> tf.Tensor:
        """Return the maximum significance value.

        Returns
        -------
        tf.Tensor
            Maximum significance value.
        """
        # Add epsilon to avoid division by zero
        significances = [
            tf.sqrt(2 * ((s + b) * tf.math.log(1 + s / (b + 1e-7)) - s))
            for s, b in zip(self.true_positives, self.false_positives)
        ]

        # Get the corresponding threshold and its index
        self.threshold_index = tf.argmax(significances)
        self.threshold = tf.gather(self.thresholds, self.threshold_index)

        # Get the maximum significance
        self.max_significance = tf.reduce_max(significances)

        return self.max_significance

    def reset_state(self) -> None:
        """Reset the state of the metric for a new batch."""
        for i in range(len(self.thresholds)):
            self.true_positives[i].assign(0.0)
            self.false_positives[i].assign(0.0)


@tf.keras.utils.register_keras_serializable()
class RejectionAtEfficiency(Metric):
    """Calculate the background rejection at a given signial efficiency.

    This metric is for binary classification problems. The background rejection is the inverse of
    the mistag rate, which is the fraction of background events that are incorrectly identified as
    signal. The signal efficiency is the fraction of signal events that are correctly identified as
    signal. The signal efficiency and the mistag rate are true positive and false positive rates.

    Parameters
    ----------
    efficiency : float, optional
        Signal efficiency. The default is 0.5.
    n_thresholds : int, optional
        Number of thresholds to use to compute the rejection. The thresholds are uniformly
        distributed in the [0, 1] range. The default is 101.
    class_id : int, optional
        Class ID of the signal class. The default is 1.
    name : str, optional
        Name of the metric. The default is "rejection_at_efficiency".
    dtype : tf.dtypes.DType, optional
        Data type of the metric. The default is tf.float32.

    Examples
    --------
    Standalone usage:
    >>> m = RejectionAtEfficiency()
    >>> m.update_state(
    ...    [[1, 0], [1, 0], [1, 0], [0, 1], [0, 1]],
    ...    [[1, 0], [0.7, 0.3], [0.2, 0.8], [0.7, 0.3], [0.2, 0.8]],
    >>> )
    >>> m.result().numpy()
    2.9999993
    """

    def __init__(
        self,
        efficiency: float = 0.5,
        n_thresholds: int = 101,
        class_id: int = 1,
        name: str = "rejection_at_efficiency",
        dtype: tf.dtypes.DType = tf.float32,
    ):
        super().__init__(name=name, dtype=dtype)
        self.specificity_at_sensitivity = SpecificityAtSensitivity(
            sensitivity=efficiency,
            num_thresholds=n_thresholds,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )

    def update_state(
        self,
        y_true: list | np.ndarray | tf.Tensor,
        y_pred: list | np.ndarray | tf.Tensor,
        sample_weight: list | np.ndarray | tf.Tensor | None = None,
    ):
        """Update the state of the metric in a batch-wise fashion.

        Parameters
        ----------
        y_true : list | np.ndarray | tf.Tensor
            True labels.
        y_pred : list | np.ndarray | tf.Tensor
            Predicted values (probabilities).
        sample_weight : list | np.ndarray | tf.Tensor | None, optional
            Sample weights. The default is None.
        """
        self.specificity_at_sensitivity.update_state(y_true, y_pred, sample_weight)

    def result(self) -> tf.Tensor:
        """Return the background rejection at the given signal efficiency.

        Returns
        -------
        tf.Tensor
            Background rejection.
        """
        # Specificity is the true negative rate: tn / (tn + fp).
        # Sensitivity is the true positive rate: tp / (tp + fn).
        # Background rejection is the inverse of 1 - specificity.
        # Signal efficiency is the same as sensitivity.
        specificity = 1 - self.specificity_at_sensitivity.result()
        rejection = 1 / (specificity + tf.keras.backend.epsilon())
        return rejection

    def reset_state(self) -> None:
        """Reset the state of the metric for a new batch."""
        self.specificity_at_sensitivity.reset_states()
