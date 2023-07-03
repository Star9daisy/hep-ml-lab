from pathlib import Path

import pytest
from keras.layers import Dense
from keras.models import Sequential
from sklearn.datasets import load_iris

from hml.methods.base import KerasMethod


def test_KerasMethod():
    dataset = load_iris()
    x = dataset.data
    y = dataset.target
    model = Sequential(name="simple_mlp")
    model.add(Dense(10, input_dim=4, activation="relu"))
    model.add(Dense(3, activation="softmax"))
    method = KerasMethod(model)
    method.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    history = method.fit(x, y, epochs=10, verbose=0)
    y_prob = method.predict(x)

    assert method.name == "simple_mlp"
    assert method.n_parameters == 83
    assert isinstance(history, dict)
    assert y_prob.shape == (150, 3)
    assert isinstance(method.evaluate(x, y), list)
    assert isinstance(method.summary(), str)

    file_path = Path(f"tests/data/{method.name}.h5")
    if file_path.exists():
        file_path.unlink()

    method.save(f"tests/data/{method.name}.h5")
    saved_method1 = KerasMethod.load(f"tests/data/{method.name}.h5")

    method.save(f"tests/data/{method.name}")
    saved_method2 = KerasMethod.load(f"tests/data/{method.name}.h5")

    assert Path(f"tests/data/{method.name}.h5").exists()
    assert saved_method1.summary() == method.summary()
    assert saved_method2.summary() == method.summary()

    with pytest.raises(FileNotFoundError):
        KerasMethod.load("tests/data/does_not_exist.h5")

    # Clean up
    file_path.unlink()
