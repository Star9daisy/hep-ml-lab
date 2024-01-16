import numpy as np

from hml.datasets import SetDataset


def test_set_dataset(tmp_path):
    mock_dataset = SetDataset("Dummy")
    mock_dataset._samples = np.random.random((10000, 5))
    mock_dataset._targets = np.random.choice(1, (10000, 1))
    mock_dataset.split(0.7, 0.3)
    mock_dataset.save(f"{tmp_path}/mock.ds")

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
    assert loaded_ds.test.samples.shape == (3000, 5)
    assert loaded_ds.test.targets.shape == (3000, 1)
    assert len(loaded_ds.test._samples) != 0
    assert len(loaded_ds.test._targets) != 0

    mock_dataset.split(0.7, 0.2, 0.1)
    mock_dataset.save(f"{tmp_path}/mock.ds")
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
