import shutil
from pathlib import Path

import numpy as np
import pytest
from keras.losses import CategoricalCrossentropy
from keras.metrics import CategoricalAccuracy
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
    target = np.append(np.ones(len(sig)), np.zeros(len(bkg)))
    target = to_categorical(target)

    # Train test split
    x_train, x_test, y_train, y_test = train_test_split(
        data, target, test_size=0.2, random_state=42
    )

    # Create and train model
    method = CutAndCount(name="cut_and_count", n_bins=100)
    method.compile(loss=CategoricalCrossentropy(), metrics=[CategoricalAccuracy()])
    history = method.fit(x_train, y_train)
    results = method.evaluate(x_test, y_test)
    y_pred = method.predict(x_test)

    assert method.name == "cut_and_count"
    assert method.n_parameters == 4
    assert isinstance(history, dict) and isinstance(results, dict)
    assert y_pred.shape == (4000, 2)
    assert isinstance(method.summary(return_string=True), str)

    # Save and load model
    dir_path = Path(f"tests/data/{method.name}")
    shutil.rmtree(dir_path, ignore_errors=True)

    method.save(dir_path)
    saved_method = CutAndCount.load(dir_path)

    assert dir_path.exists()
    assert saved_method.summary(return_string=True) == method.summary(return_string=True)

    with pytest.raises(FileNotFoundError):
        CutAndCount.load("tests/data/does_not_exist")

    # Clean up
    shutil.rmtree(dir_path, ignore_errors=True)


def test_boosted_decision_tree():
    # Load dataset
    dataset = load_breast_cancer()
    x = dataset.data
    y = dataset.target
    y = to_categorical(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Create and train model
    method = BoostedDecisionTree(n_estimators=10)
    method.compile(metrics=[CategoricalAccuracy()])

    history = method.fit(x_train, y_train)
    results = method.evaluate(x_test, y_test)
    y_pred = method.predict(x_test)

    assert method.name == "boosted_decision_tree"
    assert method.n_parameters == 150
    assert isinstance(history, dict) and isinstance(results, dict)
    assert y_pred.shape == (114, 2)
    assert isinstance(method.summary(return_string=True), str)

    # Save and load model
    dir_path = Path(f"tests/data/{method.name}")
    shutil.rmtree(dir_path, ignore_errors=True)

    method.save(dir_path)
    saved_method = BoostedDecisionTree.load(dir_path)

    assert dir_path.exists()
    assert saved_method.summary(return_string=True) == method.summary(return_string=True)

    with pytest.raises(FileNotFoundError):
        BoostedDecisionTree.load("tests/data/does_not_exist")

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
    assert isinstance(method.summary(return_string=True), str)

    # Save and load model
    dir_path = Path(f"tests/data/{method.name}")
    shutil.rmtree(dir_path, ignore_errors=True)

    method.save(dir_path)
    saved_method = ToyMLP.load(dir_path)

    assert dir_path.exists()
    assert saved_method.summary(return_string=True) == method.summary(return_string=True)

    with pytest.raises(FileNotFoundError):
        ToyMLP.load("tests/data/does_not_exist")

    # Clean up
    shutil.rmtree(dir_path, ignore_errors=True)
