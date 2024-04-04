import pytest

from hml.datasets import SetDataset
from hml.representations import Set


def test_init():
    ds = SetDataset(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"])

    # Attributes ------------------------------------------------------------- #
    assert (
        ds.set.config
        == Set(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"]).config
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
            0: {
                "class_name": "M",
                "config": {"class_name": "Mass", "physics_object": "FatJet0"},
            },
            1: {
                "class_name": "TauMN",
                "config": {
                    "class_name": "Tau21",
                    "physics_object": "FatJet0",
                    "m": 2,
                    "n": 1,
                },
            },
            2: {
                "class_name": "AngularDistance",
                "config": {"class_name": "DeltaR", "physics_object": "Jet0,Jet1"},
            },
        },
        "been_split": False,
        "seed": None,
    }


def test_read(events):
    cuts = ["fatjet.size > 0 and jet.size > 1"]
    ds = SetDataset(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"])
    ds.read(events, 1, cuts)

    assert ds.samples.shape == (75, 3)
    assert ds.targets.shape == (75, 1)


def test_from_config():
    ds = SetDataset(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"])

    assert SetDataset.from_config(ds.config).config == ds.config


def test_split(events):
    cuts = ["fatjet.size > 0 and jet.size > 1"]
    ds = SetDataset(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"])
    ds.read(events, 1, cuts)

    ds.split(0.7, 0.3)
    assert ds.train.samples.shape == (52, 3)
    assert ds.test.samples.shape == (23, 3)

    ds.split(0.7, 0.2, 0.1)
    assert ds.train.samples.shape == (52, 3)
    assert ds.test.samples.shape == (15, 3)
    assert ds.val.samples.shape == (8, 3)

    # Error cases ------------------------------------------------------------ #
    with pytest.raises(ValueError):
        ds.split(0.7, 0.5)

    with pytest.raises(ValueError):
        ds.split(0.7, 0.2, 0.5)


def test_save_load(events, tmp_path):
    cuts = ["fatjet.size > 0 and jet.size > 1"]
    ds = SetDataset(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"])
    ds.read(events, 1, cuts)
    ds.split(0.7, 0.2, 0.1)
    ds.save(f"{tmp_path}/mock.ds")

    # Lazy loading ----------------------------------------------------------- #
    loaded_ds = SetDataset.load(f"{tmp_path}/mock.ds")

    assert len(loaded_ds._samples) == 0
    assert len(loaded_ds._targets) == 0
    assert loaded_ds.samples.shape == (75, 3)
    assert loaded_ds.targets.shape == (75, 1)
    assert len(loaded_ds._samples) != 0
    assert len(loaded_ds._targets) != 0

    assert len(loaded_ds.train._samples) == 0
    assert len(loaded_ds.train._targets) == 0
    assert loaded_ds.train.samples.shape == (52, 3)
    assert loaded_ds.train.targets.shape == (52, 1)
    assert len(loaded_ds.train._samples) != 0
    assert len(loaded_ds.train._targets) != 0

    assert len(loaded_ds.test._samples) == 0
    assert len(loaded_ds.test._targets) == 0
    assert loaded_ds.test.samples.shape == (15, 3)
    assert loaded_ds.test.targets.shape == (15, 1)
    assert len(loaded_ds.test._samples) != 0
    assert len(loaded_ds.test._targets) != 0

    assert len(loaded_ds.val._samples) == 0
    assert len(loaded_ds.val._targets) == 0
    assert loaded_ds.val.samples.shape == (8, 3)
    assert loaded_ds.val.targets.shape == (8, 1)
    assert len(loaded_ds.val._samples) != 0
    assert len(loaded_ds.val._targets) != 0

    # Eager loading ---------------------------------------------------------- #
    loaded_ds = SetDataset.load(f"{tmp_path}/mock.ds", lazy=False)

    assert len(loaded_ds._samples) != 0
    assert len(loaded_ds._targets) != 0
    assert loaded_ds.samples.shape == (75, 3)
    assert loaded_ds.targets.shape == (75, 1)

    assert len(loaded_ds.train._samples) != 0
    assert len(loaded_ds.train._targets) != 0
    assert loaded_ds.train.samples.shape == (52, 3)
    assert loaded_ds.train.targets.shape == (52, 1)

    assert len(loaded_ds.test._samples) != 0
    assert len(loaded_ds.test._targets) != 0
    assert loaded_ds.test.samples.shape == (15, 3)
    assert loaded_ds.test.targets.shape == (15, 1)

    assert len(loaded_ds.val._samples) != 0
    assert len(loaded_ds.val._targets) != 0
    assert loaded_ds.val.samples.shape == (8, 3)
    assert loaded_ds.val.targets.shape == (8, 1)


def test_to_numpy(events):
    cuts = ["fatjet.size > 0 and jet.size > 1"]
    ds = SetDataset(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"])
    ds.read(events, 1, cuts)

    assert ds.to_numpy().shape == (75, 4)


def test_to_pandas(events):
    cuts = ["fatjet.size > 0 and jet.size > 1"]
    ds = SetDataset(["FatJet0.Mass", "FatJet0.Tau21", "Jet0,Jet1.DeltaR"])
    ds.read(events, 1, cuts)

    assert ds.to_pandas().shape == (75, 4)
