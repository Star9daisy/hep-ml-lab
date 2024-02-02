import numpy as np
import pytest

from hml.datasets import SetDataset
from hml.representations import Set


def test_init():
    ds = SetDataset("FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR")

    # Attributes ------------------------------------------------------------- #
    assert (
        ds.set.config == Set("FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR").config
    )
    assert ds.been_split is False
    assert ds.seed is None
    assert ds.train is None
    assert ds.test is None
    assert ds.val is None

    assert ds.samples.shape == (0,)
    assert ds.targets.shape == (0,)
    assert ds.feature_names == ["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"]
    assert ds.config == {
        "observable_configs": {
            "Mass": {"physics_object": "FatJet0"},
            "TauMN": {"physics_object": "FatJet0", "m": 2, "n": 1},
            "DeltaR": {"physics_object": "Jet0,Jet1"},
        },
        "been_split": False,
        "seed": None,
    }


def test_read_ttree(event):
    ds = SetDataset("FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR")
    ds.read_ttree(event, 1)

    assert ds.samples.shape == (1, 3)
    assert ds.targets.shape == (1, 1)


def test_from_config():
    ds = SetDataset("FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR")

    assert SetDataset.from_config(ds.config).config == ds.config


def test_split():
    ds = SetDataset("Dummy")
    ds._samples = np.random.random((10000, 5))
    ds._targets = np.random.choice(1, (10000, 1))

    ds.split(0.7, 0.3)
    assert ds.train.samples.shape == (7000, 5)
    assert ds.test.samples.shape == (3000, 5)

    ds.split(0.7, 0.2, 0.1)
    assert ds.train.samples.shape == (7000, 5)
    assert ds.test.samples.shape == (2000, 5)
    assert ds.val.samples.shape == (1000, 5)

    # Error cases ------------------------------------------------------------ #
    with pytest.raises(ValueError):
        ds.split(0.7, 0.5)

    with pytest.raises(ValueError):
        ds.split(0.7, 0.2, 0.5)


def test_save_load(tmp_path):
    ds = SetDataset("Dummy")
    ds._samples = np.random.random((10000, 5))
    ds._targets = np.random.choice(1, (10000, 1))
    ds.split(0.7, 0.2, 0.1)
    ds.save(f"{tmp_path}/mock.ds")

    # Lazy loading ----------------------------------------------------------- #
    loaded_ds = SetDataset.load(f"{tmp_path}/mock.ds")

    assert len(loaded_ds._samples) == 0
    assert len(loaded_ds._targets) == 0
    assert loaded_ds.samples.shape == (10000, 5)
    assert loaded_ds.targets.shape == (10000, 1)
    assert len(loaded_ds._samples) != 0
    assert len(loaded_ds._targets) != 0

    assert len(loaded_ds.train._samples) == 0
    assert len(loaded_ds.train._targets) == 0
    assert loaded_ds.train.samples.shape == (7000, 5)
    assert loaded_ds.train.targets.shape == (7000, 1)
    assert len(loaded_ds.train._samples) != 0
    assert len(loaded_ds.train._targets) != 0

    assert len(loaded_ds.test._samples) == 0
    assert len(loaded_ds.test._targets) == 0
    assert loaded_ds.test.samples.shape == (2000, 5)
    assert loaded_ds.test.targets.shape == (2000, 1)
    assert len(loaded_ds.test._samples) != 0
    assert len(loaded_ds.test._targets) != 0

    assert len(loaded_ds.val._samples) == 0
    assert len(loaded_ds.val._targets) == 0
    assert loaded_ds.val.samples.shape == (1000, 5)
    assert loaded_ds.val.targets.shape == (1000, 1)
    assert len(loaded_ds.val._samples) != 0
    assert len(loaded_ds.val._targets) != 0

    # Eager loading ---------------------------------------------------------- #
    loaded_ds = SetDataset.load(f"{tmp_path}/mock.ds", lazy=False)

    assert len(loaded_ds._samples) != 0
    assert len(loaded_ds._targets) != 0
    assert loaded_ds.samples.shape == (10000, 5)
    assert loaded_ds.targets.shape == (10000, 1)

    assert len(loaded_ds.train._samples) != 0
    assert len(loaded_ds.train._targets) != 0
    assert loaded_ds.train.samples.shape == (7000, 5)
    assert loaded_ds.train.targets.shape == (7000, 1)

    assert len(loaded_ds.test._samples) != 0
    assert len(loaded_ds.test._targets) != 0
    assert loaded_ds.test.samples.shape == (2000, 5)
    assert loaded_ds.test.targets.shape == (2000, 1)

    assert len(loaded_ds.val._samples) != 0
    assert len(loaded_ds.val._targets) != 0
    assert loaded_ds.val.samples.shape == (1000, 5)
    assert loaded_ds.val.targets.shape == (1000, 1)


def test_to_numpy():
    ds = SetDataset("Dummy")
    ds._samples = np.random.random((10000, 5))
    ds._targets = np.random.choice(1, (10000, 1))

    assert ds.to_numpy().shape == (10000, 6)


def test_to_pandas():
    ds = SetDataset("Dummy", "Dummy", "Dummy", "Dummy", "Dummy")
    ds._samples = np.random.random((10000, 5))
    ds._targets = np.random.choice(1, (10000, 1))

    assert ds.to_pandas().shape == (10000, 6)
