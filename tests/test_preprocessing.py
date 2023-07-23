import numpy as np


def test_is_categorical():
    from hml.preprocessing import is_categorical

    assert is_categorical(np.array([[0, 1], [1, 0], [1, 0], [0, 1]])) == True
    assert is_categorical(np.array([[0, 2], [1, 0], [1, 0], [0, 1]])) == False
    assert is_categorical(np.array([[0, 0], [1, 0], [1, 0], [0, 1]])) == False
