import awkward as ak
import numpy as np
import pytest

from hml.observables import parse
from hml.representations import Image


def test_init():
    r = Image(
        height="FatJet0.Constituents.Phi",
        width=parse("FatJet0.Constituents.Eta"),
    )

    # Attributes ------------------------------------------------------------- #
    assert r.height == parse("FatJet0.Constituents.Phi")
    assert r.width == parse("FatJet0.Constituents.Eta")
    assert r.channel is None

    r = Image(
        height="FatJet0.Constituents.Phi",
        width=parse("FatJet0.Constituents.Eta"),
        channel="FatJet0.Constituents.Pt",
    )

    # Attributes ------------------------------------------------------------- #
    assert r.height == parse("FatJet0.Constituents.Phi")
    assert r.width == parse("FatJet0.Constituents.Eta")
    assert r.channel == parse("FatJet0.Constituents.Pt")


def test_register(events):
    image1 = (
        Image(
            height="FatJet0.Constituents.Phi",
            width="FatJet0.Constituents.Eta",
            channel="FatJet0.Constituents.Pt",
        )
        .read(events)
        .with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )

    image2 = (
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

    assert image1.config == image2.config

    image2.read(events)
    assert image1.values.shape == image2.values.shape


def test_error_cases(events):
    r = Image(
        height="FatJet0.Constituents.Phi",
        width="FatJet0.Constituents.Eta",
        channel="FatJet0.Constituents.Pt",
    ).read(events)

    # translate to a non-supported origin
    with pytest.raises(ValueError):
        r.translate(origin="Jet0")

    # rotate around a non-supported axis
    with pytest.raises(ValueError):
        r.rotate(axis="Jet0", orientation=90)

    # status will be False if there are no enough subjets
    # then rotate and pixelate will not work
    r.with_subjets("FatJet0.Constituents", "kt", 0.3, 0)

    assert r.translate(origin="SubJet100").status is False
    assert r.rotate(axis="SubJet100", orientation=90).config == r.config
    assert (
        r.pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)]).config == r.config
    )


def test_show(events):
    r = Image(
        height="FatJet0.Constituents.Phi",
        width="FatJet0.Constituents.Eta",
        channel="FatJet0.Constituents.Pt",
    ).read(events)
    r.show()

    r.with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
    r.show()

    r.translate(origin="SubJet0")
    r.show()

    r.rotate(axis="SubJet1", orientation=-90)
    r.show()
    r.show(limits=[(-1.6, 1.6), (-1.6, 1.6)])

    r.pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    r.show()
    r.show(show_pixels=True)
    r.show(grid=False)
    r.show(as_point=True)


def test_class_methods():
    r = Image(
        height="FatJet0.Constituents.Phi",
        width="FatJet0.Constituents.Eta",
        channel="FatJet0.Constituents.Pt",
    )
    assert Image.from_config(r.config).config == r.config

    r.with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
    assert Image.from_config(r.config).config == r.config

    r.translate(origin="SubJet0")
    assert Image.from_config(r.config).config == r.config

    r.rotate(axis="SubJet1", orientation=-90)
    assert Image.from_config(r.config).config == r.config

    r.pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    assert Image.from_config(r.config).config == r.config

    r = Image(
        height="FatJet0.Constituents.Phi",
        width="FatJet0.Constituents.Eta",
    )
    assert Image.from_config(r.config).config == r.config


def test_values(events):
    # values are nan if the image has not read a TTree
    r = Image(
        height="FatJet0.Constituents.Phi",
        width="FatJet0.Constituents.Eta",
    )

    assert isinstance(r.values, tuple)
    assert str(r.values[0].type) == "0 * unknown"
    assert str(r.values[1].type) == "0 * unknown"

    # values are not nan if the image has read a TTree
    r = Image(
        height="FatJet0.Constituents.Phi",
        width="FatJet0.Constituents.Eta",
    ).read(events)
    assert str(r.values[0].type) == "100 * var * float32"
    assert str(r.values[1].type) == "100 * var * float32"

    # values will contain nan if the range is not enough to cover all the values
    r = (
        Image(
            height="FatJet0.Constituents.Phi",
            width="FatJet0.Constituents.Eta",
        )
        .read(events)
        .pixelate(size=(33, 33), range=[(5, 10), (5, 10)])
    )
    assert isinstance(r.values, np.ndarray)
    assert r.values.shape[1:] == (33, 33)
    assert ak.count_nonzero(ak.nan_to_num(r.height.value, 0)) == 0
    assert ak.count_nonzero(ak.nan_to_num(r.width.value, 0)) == 0

    r = (
        Image(
            height="FatJet0.Constituents.Phi",
            width="FatJet0.Constituents.Eta",
        )
        .read(events)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )
    assert isinstance(r.values, np.ndarray)
    assert r.values.shape[1:] == (33, 33)
    assert ak.count_nonzero(ak.nan_to_num(r.height.value, 0)) > 0
    assert ak.count_nonzero(ak.nan_to_num(r.width.value, 0)) > 0

    # common cases
    r = (
        Image(
            height="FatJet0.Constituents.Phi",
            width="FatJet0.Constituents.Eta",
        )
        .read(events)
        .with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )
    assert r.values.shape[1:] == (33, 33)

    r = (
        Image(
            height="FatJet0.Constituents.Phi",
            width="FatJet0.Constituents.Eta",
            channel="FatJet0.Constituents.Pt",
        )
        .read(events)
        .with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )
    assert r.values.shape[1:] == (33, 33)
