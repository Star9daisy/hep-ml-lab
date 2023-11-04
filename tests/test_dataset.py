import numpy as np
import pytest

from hml.datasets import TabularDataset, load_dataset


def test_save_and_load(tmp_path):
    np.random.seed(42)
    dataset = TabularDataset(
        samples=np.random.random((100, 5)),
        targets=np.random.randint(0, 2, (100, 1)),
        feature_names=["a", "b", "c", "d", "e"],
        target_names=["background", "signal"],
        description="Demo dataset",
    )
    dataset.save(tmp_path / "demo_dataset")

    with pytest.raises(FileNotFoundError):
        load_dataset(tmp_path / "wrong_dir.npz")

    loaded_dataset1 = load_dataset(tmp_path / "demo_dataset.npz")
    loaded_dataset2 = TabularDataset.load(tmp_path / "demo_dataset.npz")
    assert type(loaded_dataset1) == TabularDataset

    assert np.all(dataset.samples == loaded_dataset2.samples)
    assert np.all(dataset.targets == loaded_dataset2.targets)
    assert (dataset.feature_names == loaded_dataset2.feature_names).all()
    assert (dataset.target_names == loaded_dataset2.target_names).all()
    assert dataset.description == loaded_dataset2.description
