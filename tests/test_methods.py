import shutil
from pathlib import Path

import numpy as np
import pytest
from keras.losses import CategoricalCrossentropy, SparseCategoricalCrossentropy
from keras.metrics import CategoricalAccuracy, SparseCategoricalAccuracy
from keras.optimizers import Adam
from keras.utils import to_categorical
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from hml.methods import BoostedDecisionTree, CutAndCount, ToyMLP


def test_cut_and_count():
    # Four features
    # Signal is at left, right, middle, and both sides respectively
    np.random.seed(42)
    feat1 = np.random.normal(0, size=10000)
    feat2 = np.random.normal(5, size=10000)
    feat3 = np.random.normal(0, size=10000)
    feat4 = np.append(
        np.random.normal(5, size=5000),
        np.random.normal(-5, size=5000),
    )

    sig = np.stack([feat1, feat2, feat3, feat4], axis=1)

    feat1 = np.random.normal(5, size=10000)
    feat2 = np.random.normal(0, size=10000)
    feat3 = np.append(
        np.random.normal(5, size=5000),
        np.random.normal(-5, size=5000),
    )
    feat4 = np.random.normal(0, size=10000)

    bkg = np.stack([feat1, feat2, feat3, feat4], axis=1)

    data = np.concatenate([sig, bkg])
    ordinal_target = np.append(np.ones(len(sig)), np.zeros(len(bkg)))
    onehot_target = to_categorical(ordinal_target)

    # Create and train model on ordinal target
    method = CutAndCount(name="cut_and_count", n_bins=100)
    method.compile(loss=SparseCategoricalCrossentropy(), metrics=[SparseCategoricalAccuracy()])
    _ = method.fit(data, ordinal_target)

    # Create and train model on onehot target
    method = CutAndCount(name="cut_and_count", n_bins=100)
    # compile case1: loss is not None
    method.compile(loss=CategoricalCrossentropy(), metrics=[CategoricalAccuracy()])
    # compile case2: loss is None
    with pytest.raises(ValueError):
        method.compile()

    history = method.fit(data, onehot_target)
    results = method.evaluate(data, onehot_target)
    y_pred = method.predict(data)

    assert method.name == "cut_and_count"
    assert method.n_parameters == 4
    assert isinstance(history, dict) and isinstance(results, dict)
    assert y_pred.shape == (20000, 2)
    # summary case1: return_string is True
    assert isinstance(method.summary(return_string=True), str)
    # summary case2: return_string is False
    assert method.summary(return_string=False) is None

    # Save and load model
    dir_path = Path(f"tests/data/{method.name}")
    dir_path.mkdir(parents=True, exist_ok=True)

    method.save(dir_path)
    saved_method = CutAndCount.load(dir_path)

    assert dir_path.exists()
    assert saved_method.summary(return_string=True) == method.summary(return_string=True)

    with pytest.raises(FileNotFoundError):
        CutAndCount.load("tests/data/does_not_exist")
    with pytest.raises(TypeError):
        Path.unlink(dir_path / "metadata.yml")
        CutAndCount.load(dir_path)

    # Plot
    from hml.methods.cuts import plot_cuts

    for i in range(4):
        plot_cuts(sig[:, i], bkg[:, i], 100, method.cuts[i], method.signal_locations[i])

    # Clean up
    shutil.rmtree(dir_path, ignore_errors=True)


def test_boosted_decision_tree():
    # Load dataset
    dataset = load_breast_cancer()
    x = dataset.data
    y_ordinal = dataset.target
    y_onehot = to_categorical(y_ordinal)

    # Create and train model on ordinal target
    method = BoostedDecisionTree(n_estimators=10)
    method.compile(metrics=[SparseCategoricalAccuracy()])
    _ = method.fit(x, y_ordinal)

    # Create and train model on onehot target
    method = BoostedDecisionTree(n_estimators=10)
    # compile case1: metrics is None
    method.compile()
    _ = method.fit(x, y_onehot)
    # compile case2: metrics is not None
    method.compile(metrics=[CategoricalAccuracy()])
    history = method.fit(x, y_onehot)
    results = method.evaluate(x, y_onehot)
    y_pred = method.predict(x)

    assert method.name == "boosted_decision_tree"
    assert method.n_parameters == 150
    assert isinstance(history, dict) and isinstance(results, dict)
    assert y_pred.shape == (569, 2)
    # summary case1: return_string is True
    assert isinstance(method.summary(return_string=True), str)
    # summary case2: return_string is False
    assert method.summary(return_string=False) is None

    # Save and load model
    dir_path = Path(f"tests/data/{method.name}")
    dir_path.mkdir(parents=True, exist_ok=True)

    method.save(dir_path)
    saved_method = BoostedDecisionTree.load(dir_path)

    assert dir_path.exists()
    assert saved_method.summary(return_string=True) == method.summary(return_string=True)

    with pytest.raises(FileNotFoundError):
        BoostedDecisionTree.load("tests/data/does_not_exist")
    with pytest.raises(TypeError):
        Path.unlink(dir_path / "metadata.yml")
        BoostedDecisionTree.load(dir_path)

    # Clean up
    shutil.rmtree(dir_path, ignore_errors=True)


def test_toy_mlp():
    # Load dataset
    dataset = load_breast_cancer()
    x = dataset.data
    y = dataset.target
    y = to_categorical(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Create and train model
    method = ToyMLP(input_shape=(x.shape[1],), name="toy_mlp")
    method.compile(
        optimizer=Adam(),
        loss=CategoricalCrossentropy(),
        metrics=[CategoricalAccuracy()],
    )
    history = method.fit(x_train, y_train, epochs=10)
    results = method.evaluate(x_test, y_test)
    y_pred = method.predict(x_test)

    assert method.name == "toy_mlp"
    assert method.n_parameters == 4130
    assert isinstance(history, dict) and isinstance(results, dict)
    assert y_pred.shape == (114, 2)
    # summary case1: return_string is True
    assert isinstance(method.summary(return_string=True), str)
    # summary case2: return_string is False
    assert method.summary(return_string=False) is None

    # Save and load model
    dir_path = Path(f"tests/data/{method.name}")
    dir_path.mkdir(parents=True, exist_ok=True)

    method.save(dir_path)
    saved_method = ToyMLP.load(dir_path)

    assert dir_path.exists()
    assert saved_method.summary(return_string=True) == method.summary(return_string=True)

    with pytest.raises(FileNotFoundError):
        ToyMLP.load("tests/data/does_not_exist")
    with pytest.raises(TypeError):
        Path.unlink(dir_path / "metadata.yml")
        ToyMLP.load(dir_path)

    # Clean up
    shutil.rmtree(dir_path, ignore_errors=True)
