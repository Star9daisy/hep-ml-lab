import os
import warnings

os.environ["KERAS_BACKEND"] = "torch"

import keras
import numpy as np
from sklearn.model_selection import train_test_split

from hml.approaches import CutLayer
from hml.generators import Madgraph5Run
from hml.types import Path

DATA_DIR = Path("tests/data")
run_tt = Madgraph5Run(DATA_DIR / "pp2tt", "run_01")
run_zz = Madgraph5Run(DATA_DIR / "pp2zz", "run_01")
event_tt = next(iter(run_tt.events()))
event_zz = next(iter(run_zz.events()))


def test_cut_layer_simple():
    cut = CutLayer("Jet.Pt > 10")
    assert cut.name == "Jet.Pt > 10"
    assert cut.cut == "Jet.Pt > 10"
    assert cut.count == 0
    assert cut.is_passed(event_tt) == True

    cut = CutLayer("Jet.Pt > 10 [all]")
    assert cut.is_passed(event_tt) == True

    cut = CutLayer("Jet.Pt > 10 [any]")
    assert cut.is_passed(event_tt) == True

    cut = CutLayer("veto Jet.Pt > 10 [any]")
    assert cut.is_passed(event_tt) == False
    assert cut.count == 1

    cut = CutLayer("Jet.Pt > 30")
    assert cut.is_passed(event_tt) == False

    cut = CutLayer("Jet.Pt > 30 [all]")
    assert cut.is_passed(event_tt) == False

    cut = CutLayer("Jet.Pt > 30 [any]")
    assert cut.is_passed(event_tt) == True

    cut = CutLayer("veto Jet.Pt > 30 [any]")
    assert cut.is_passed(event_tt) == False


def test_cut_layer_full(tmp_path):
    warnings.filterwarnings("ignore", category=UserWarning)
    np.random.seed(42)
    n_samples_per_class = 100

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

    # sig = np.concatenate([sig_feat_0], 1)
    # bkg = np.concatenate([bkg_feat_0], 1)
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

    inputs = keras.Input((1,), name="Observables")
    targets = keras.Input((), name="Targets")

    y_pred1 = CutLayer(feature_id=0)(inputs, targets)
    y_pred2 = CutLayer(feature_id=1)(inputs, targets)
    y_pred3 = CutLayer(feature_id=2)(inputs, targets)
    y_pred4 = CutLayer(feature_id=3)(inputs, targets)
    outputs = keras.layers.Multiply()([y_pred1, y_pred2, y_pred3, y_pred4])

    model = keras.Model(inputs=[inputs, targets], outputs=outputs)

    model.compile(
        loss="binary_crossentropy",
        optimizer="adam",
        metrics=["binary_accuracy"],
    )
    model.fit([x_train, y_train], y_train, batch_size=len(x_train))
    print(model.predict([x_test, y_test], batch_size=len(x_test)))
    print(model.evaluate([x_test, y_test], y_test, batch_size=len(x_test)))
    model.summary()

    model.save(f"{tmp_path}/model.keras")
    ckpt = keras.models.load_model(f"{tmp_path}/model.keras")

    for layer, layer_ckpt in zip(model.layers, ckpt.layers):
        if isinstance(layer, CutLayer):
            assert layer.name == layer_ckpt.name
            assert layer.feature_id == layer_ckpt.feature_id
            assert layer.cut == layer_ckpt.cut
            assert layer.count == layer_ckpt.count
            assert layer.cut == layer_ckpt.cut
