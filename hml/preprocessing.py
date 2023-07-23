import numpy as np


def is_categorical(labels: np.ndarray) -> bool:
    """
    Check if the input labels are one-hot encoded.

    A valid one-hot encoding has exactly one '1' in each row and the rest are '0's.

    Parameters
    ----------
    labels : numpy.ndarray
        The labels to check, where each row represents one sample's label.

    Returns
    -------
    bool
        True if the labels are one-hot encoded, False otherwise.

    Examples
    --------
    >>> labels = np.array([[0, 1], [1, 0], [1, 0], [0, 1]])
    >>> print(is_categorical(labels))
    True

    >>> labels = np.array([[0, 2], [1, 0], [1, 0], [0, 1]])
    >>> print(is_categorical(labels))
    False

    >>> labels = np.array([[0, 0], [1, 0], [1, 0], [0, 1]])
    >>> print(is_categorical(labels))
    False
    """
    # each row (the label of a sample) should have exactly one '1' and the rest '0's
    for row in labels:
        if np.sum(row) != 1 or np.max(row) != 1 or np.min(row) != 0:
            return False
    return True
