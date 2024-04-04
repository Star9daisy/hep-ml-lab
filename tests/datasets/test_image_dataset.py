import numpy as np
import pytest

from hml.datasets import ImageDataset
from hml.representations import Image


def test_init():
    image = (
        Image(
            height="FatJet0.Constituents.Phi",
            width="FatJet0.Constituents.Eta",
            channel="FatJet0.Constituents.Pt",
        )
        .with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )

    ds = ImageDataset(image)

    # Attributes ------------------------------------------------------------- #
    assert ds.image.config == image.config

    assert ds._samples == []
    assert ds._targets == []

    assert ds.been_split is False
    assert ds.seed is None

    assert ds.train is None
    assert ds.test is None
    assert ds.val is None

    assert ds._data is None
    assert ds._been_read is None

    assert ds.features == {
        "height": "FatJet0.Constituents.Phi",
        "width": "FatJet0.Constituents.Eta",
        "channel": "FatJet0.Constituents.Pt",
    }

    assert ds.samples.size == 0
    assert ds.targets.size == 0


def test_read(events):
    # No pixelation, samples are a tuple of height and width ----------------- #
    image = (
        Image(
            height="FatJet0.Constituents.Phi",
            width="FatJet0.Constituents.Eta",
            channel="FatJet0.Constituents.Pt",
        )
        .with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
    )

    cuts = ["fatjet.size > 0"]
    ds = ImageDataset(image)
    ds.read(events, 1, cuts)

    assert isinstance(ds.samples, tuple)
    assert isinstance(ds.samples[0], np.ndarray)
    assert isinstance(ds.samples[1], np.ndarray)
    assert ds.targets.shape == (99, 1)

    # Pixelation, samples are a single array for an image -------------------- #
    image = (
        Image(
            height="FatJet0.Constituents:.Phi",
            width="FatJet0.Constituents:.Eta",
            channel="FatJet0.Constituents:.Pt",
        )
        .with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )

    ds = ImageDataset(image)
    ds.read(events, 1, cuts)

    assert isinstance(ds.samples, np.ndarray)
    assert ds.samples.shape == (99, 33, 33)
    assert ds.targets.shape == (99, 1)


def test_split():
    image = Image(
        height="FatJet0.Constituents:.Phi",
        width="FatJet0.Constituents:.Eta",
        channel="FatJet0.Constituents:.Pt",
    )
    ds = ImageDataset(image)

    # Fake non-pixelated data ------------------------------------------------ #
    # Since it's not supported yet, we leave this test for the future.

    # Fake pixelated data ---------------------------------------------------- #
    ds.image.been_pixelated = True
    ds._samples = np.random.random((10000, 33, 33))
    ds._targets = np.random.choice(1, (10000, 1))

    # Common cases ----------------------------------------------------------- #
    ds.split(0.7, 0.3)
    assert ds.train.samples.shape == (7000, 33, 33)
    assert ds.test.samples.shape == (3000, 33, 33)

    ds.split(0.7, 0.2, 0.1)
    assert ds.train.samples.shape == (7000, 33, 33)
    assert ds.test.samples.shape == (2000, 33, 33)
    assert ds.val.samples.shape == (1000, 33, 33)

    # Error cases ------------------------------------------------------------ #
    with pytest.raises(ValueError):
        ds.split(0.7, 0.5)

    with pytest.raises(ValueError):
        ds.split(0.7, 0.2, 0.5)


def test_save_load(events, tmp_path):
    image = (
        Image(
            height="FatJet0.Constituents.Phi",
            width="FatJet0.Constituents.Eta",
            channel="FatJet0.Constituents.Pt",
        )
        .with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )
    ds = ImageDataset(image)
    cuts = ["fatjet.size > 0"]
    ds.read(events, 1, cuts)
    ds.split(0.7, 0.2, 0.1)
    ds.save(f"{tmp_path}/mock.ds")

    # No lazy loading -------------------------------------------------------- #
    loaded_ds = ImageDataset.load(f"{tmp_path}/mock.ds", lazy=False)

    assert loaded_ds._samples.size != 0
    assert loaded_ds._targets.size != 0
    assert (loaded_ds.samples == ds.samples).all()
    assert (loaded_ds.targets == ds.targets).all()

    # Lazy loading ----------------------------------------------------------- #
    loaded_ds = ImageDataset.load(f"{tmp_path}/mock.ds")

    # It's [] because it's been pixelated and is expected to be an image
    assert loaded_ds._samples == []
    assert loaded_ds._targets == []
    assert (loaded_ds.samples == ds.samples).all()
    assert (loaded_ds.targets == ds.targets).all()

    # Non-pixelated data ---------------------------------------------------- #
    image = (
        Image(
            height="FatJet0.Constituents:.Phi",
            width="FatJet0.Constituents:.Eta",
            channel="FatJet0.Constituents:.Pt",
        )
        .with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
    )
    ds = ImageDataset(image)
    ds.read(events, 1, cuts)

    # non-pixelated data is not supported for split method yet
    ds.save(f"{tmp_path}/mock.ds")

    # No lazy loading -------------------------------------------------------- #
    loaded_ds = ImageDataset.load(f"{tmp_path}/mock.ds", lazy=False)

    assert loaded_ds._samples.size != 0
    assert loaded_ds._targets.size != 0
    assert (
        np.nan_to_num(ds.samples[0], nan=0.0)
        == np.nan_to_num(loaded_ds.samples[0], nan=0.0)
    ).all()
    assert (
        np.nan_to_num(ds.samples[1], nan=0.0)
        == np.nan_to_num(loaded_ds.samples[1], nan=0.0)
    ).all()

    # Lazy loading ----------------------------------------------------------- #
    loaded_ds = ImageDataset.load(f"{tmp_path}/mock.ds")

    # It's [[], []] because it's not been pixelated and is expected to be a tuple
    assert loaded_ds._samples == [[], []]
    assert loaded_ds._targets == []
    assert (
        np.nan_to_num(ds.samples[0], nan=0.0)
        == np.nan_to_num(loaded_ds.samples[0], nan=0.0)
    ).all()
    assert (
        np.nan_to_num(ds.samples[1], nan=0.0)
        == np.nan_to_num(loaded_ds.samples[1], nan=0.0)
    ).all()
    assert (loaded_ds.targets == ds.targets).all()


def test_show(events):
    # Pixelated data --------------------------------------------------------- #
    image = (
        Image(
            height="FatJet0.Constituents:.Phi",
            width="FatJet0.Constituents:.Eta",
            channel="FatJet0.Constituents:.Pt",
        )
        .with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )
    ds = ImageDataset(image)
    cuts = ["fatjet.size > 0"]
    ds.read(events, 1, cuts)

    # Total image
    ds.show(show_pixels=True, norm="log")
    ds.show(show_pixels=True, norm="log", target=1)

    # Non-pixelated data --------------------------------------------------------- #
    image = (
        Image(
            height="FatJet0.Constituents:.Phi",
            width="FatJet0.Constituents:.Eta",
            channel="FatJet0.Constituents:.Pt",
        )
        .with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
    )
    ds = ImageDataset(image)
    cuts = ["fatjet.size > 0"]
    ds.read(events, 1, cuts)

    # Non-pixelated data should be shown as a scatter plot
    ds.show(limits=[(-1.6, 1.6), (-1.6, 1.6)])
