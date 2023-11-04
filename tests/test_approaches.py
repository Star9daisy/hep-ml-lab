import numpy as np
from sklearn.model_selection import train_test_split

from hml.approaches import CutAndCount as CBA
from hml.approaches import GradientBoostedDecisionTree as BDT
from hml.approaches import ToyMultilayerPerceptron as MLP
from hml.approaches import load_approach


def test_cba(tmp_path):
    # Four features
    # Signal is at left, right, middle, and both sides respectively
    np.random.seed(42)
    n_samples_per_class = 10000

    # feature 0: signal is at the left side of the background
    bkg_feat_0 = np.random.normal(3, 2, (n_samples_per_class, 1))
    sig_feat_0 = np.random.normal(-3, 2, (n_samples_per_class, 1))

    # feature 1: signal is at the right side of the background
    bkg_feat_1 = np.random.normal(-3, 2, (n_samples_per_class, 1))
    sig_feat_1 = np.random.normal(3, 2, (n_samples_per_class, 1))

    # feature 2: signal is in the middle of the background
    sig_feat_2 = np.random.normal(0, size=(n_samples_per_class, 1))
    bkg_feat_2 = np.concatenate(
        [
            np.random.normal(-5, size=(int(n_samples_per_class / 2), 1)),
            np.random.normal(5, size=(int(n_samples_per_class / 2), 1)),
        ],
        axis=0,
    )

    # feature 3: signal is on the both sides of the background
    sig_feat_3 = np.concatenate(
        [
            np.random.normal(-5, size=(int(n_samples_per_class / 2), 1)),
            np.random.normal(5, size=(int(n_samples_per_class / 2), 1)),
        ],
        axis=0,
    )
    bkg_feat_3 = np.random.normal(0, size=(n_samples_per_class, 1))

    sig = np.concatenate([sig_feat_0, sig_feat_1, sig_feat_2, sig_feat_3], 1)
    bkg = np.concatenate([bkg_feat_0, bkg_feat_1, bkg_feat_2, bkg_feat_3], 1)
    samples = np.concatenate([bkg, sig], 0, dtype=np.float32)

    targets_0 = np.zeros((n_samples_per_class,), dtype=np.int32)
    targets_1 = np.ones((n_samples_per_class,), dtype=np.int32)
    targets = np.concatenate([targets_0, targets_1], 0, dtype=np.int32)

    x_train, x_test, y_train, y_test = train_test_split(
        samples, targets, test_size=0.2, random_state=42
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train, y_train, test_size=0.1, random_state=42
    )

    # Create and train model on ordinal target
    m = CBA()
    m.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    history = m.fit(
        x_train,
        y_train,
        batch_size=len(x_train),
        validation_data=(x_val, y_val),
    )

    m.summary()
    m.save(tmp_path / "CBA.keras")
    loaded_m = load_approach(tmp_path / "CBA.keras")
    assert (loaded_m.cuts.numpy() == m.cuts.numpy()).all()


def test_bdt(tmp_path):
    np.random.seed(42)
    num = 10000

    # feature 0: signal is at the left side of the background
    bkg_feat_0 = np.random.normal(3, 2, (num, 1))
    sig_feat_0 = np.random.normal(-3, 2, (num, 1))

    # feature 1: signal is at the right side of the background
    bkg_feat_1 = np.random.normal(-3, 2, (num, 1))
    sig_feat_1 = np.random.normal(3, 2, (num, 1))

    # feature 2: signal is in the middle of the background
    sig_feat_2 = np.random.normal(0, size=(num, 1))
    bkg_feat_2 = np.concatenate(
        [
            np.random.normal(-5, size=(int(num / 2), 1)),
            np.random.normal(5, size=(int(num / 2), 1)),
        ],
        axis=0,
    )

    # feature 3: signal is on the both sides of the background
    sig_feat_3 = np.concatenate(
        [
            np.random.normal(-5, size=(int(num / 2), 1)),
            np.random.normal(5, size=(int(num / 2), 1)),
        ],
        axis=0,
    )
    bkg_feat_3 = np.random.normal(0, size=(num, 1))

    sig = np.concatenate([sig_feat_0, sig_feat_1, sig_feat_2, sig_feat_3], 1)
    bkg = np.concatenate([bkg_feat_0, bkg_feat_1, bkg_feat_2, bkg_feat_3], 1)
    samples = np.concatenate([bkg, sig], 0, dtype=np.float32)

    targets_0 = np.zeros((num,), dtype=np.int32)
    targets_1 = np.ones((num,), dtype=np.int32)
    targets = np.concatenate([targets_0, targets_1], 0, dtype=np.int32)

    x_train, x_test, y_train, y_test = train_test_split(
        samples, targets, test_size=0.2, random_state=42
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train, y_train, test_size=0.1, random_state=42
    )

    m = BDT()
    m.compile(metrics=["accuracy"])
    history = m.fit(x_train, y_train, validation_data=(x_val, y_val))
    m.summary()
    m.save(tmp_path / "BDT.pickle")
    loaded_m = load_approach(tmp_path / "BDT.pickle")
    assert loaded_m.n_estimators_ == m.n_estimators_


def test_mlp(tmp_path):
    np.random.seed(42)
    n_samples_per_class = 10000

    # feature 0: signal is at the left side of the background
    bkg_feat_0 = np.random.normal(3, 2, (n_samples_per_class, 1))
    sig_feat_0 = np.random.normal(-3, 2, (n_samples_per_class, 1))

    # feature 1: signal is at the right side of the background
    bkg_feat_1 = np.random.normal(-3, 2, (n_samples_per_class, 1))
    sig_feat_1 = np.random.normal(3, 2, (n_samples_per_class, 1))

    # feature 2: signal is in the middle of the background
    sig_feat_2 = np.random.normal(0, size=(n_samples_per_class, 1))
    bkg_feat_2 = np.concatenate(
        [
            np.random.normal(-5, size=(int(n_samples_per_class / 2), 1)),
            np.random.normal(5, size=(int(n_samples_per_class / 2), 1)),
        ],
        axis=0,
    )

    # feature 3: signal is on the both sides of the background
    sig_feat_3 = np.concatenate(
        [
            np.random.normal(-5, size=(int(n_samples_per_class / 2), 1)),
            np.random.normal(5, size=(int(n_samples_per_class / 2), 1)),
        ],
        axis=0,
    )
    bkg_feat_3 = np.random.normal(0, size=(n_samples_per_class, 1))

    sig = np.concatenate([sig_feat_0, sig_feat_1, sig_feat_2, sig_feat_3], 1)
    bkg = np.concatenate([bkg_feat_0, bkg_feat_1, bkg_feat_2, bkg_feat_3], 1)
    samples = np.concatenate([bkg, sig], 0, dtype=np.float32)

    targets_0 = np.zeros((n_samples_per_class,), dtype=np.int32)
    targets_1 = np.ones((n_samples_per_class,), dtype=np.int32)
    targets = np.concatenate([targets_0, targets_1], 0, dtype=np.int32)

    x_train, x_test, y_train, y_test = train_test_split(
        samples, targets, test_size=0.2, random_state=42
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train, y_train, test_size=0.1, random_state=42
    )

    m = MLP()
    m.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    history = m.fit(
        x_train,
        y_train,
        epochs=10,
        batch_size=256,
        validation_data=(x_val, y_val),
    )

    m.summary()
    m.save(tmp_path / "MLP.keras")
    loaded_m = load_approach(tmp_path / "MLP.keras")
    assert loaded_m.count_params() == m.count_params()
