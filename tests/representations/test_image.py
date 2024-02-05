import numpy as np
import pytest

from hml.observables import get_observable
from hml.representations import Image


def test_init():
    r = Image(
        height="FatJet0.Constituents:.Phi",
        width=get_observable("FatJet0.Constituents:.Eta"),
    )

    # Attributes ------------------------------------------------------------- #
    assert r.height == get_observable("FatJet0.Constituents:.Phi")
    assert r.width == get_observable("FatJet0.Constituents:.Eta")
    assert r.channel is None

    r = Image(
        height="FatJet0.Constituents:.Phi",
        width=get_observable("FatJet0.Constituents:.Eta"),
        channel="FatJet0.Constituents:.Pt",
    )

    # Attributes ------------------------------------------------------------- #
    assert r.height == get_observable("FatJet0.Constituents:.Phi")
    assert r.width == get_observable("FatJet0.Constituents:.Eta")
    assert r.channel == get_observable("FatJet0.Constituents:.Pt")


def test_register(event):
    image1 = (
        Image(
            height="FatJet0.Constituents:.Phi",
            width="FatJet0.Constituents:.Eta",
            channel="FatJet0.Constituents:.Pt",
        )
        .read_ttree(event)
        .with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
        .translate(origin="SubJet0")
        .rotate(axis="SubJet1", orientation=-90)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )

    image2 = (
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

    assert image1.config == image2.config

    image2.read_ttree(event)
    assert image1.values.shape == image2.values.shape


def test_error_cases(event):
    r = Image(
        height="FatJet0.Constituents:.Phi",
        width="FatJet0.Constituents:.Eta",
        channel="FatJet0.Constituents:.Pt",
    ).read_ttree(event)

    # translate to a non-supported origin
    with pytest.raises(ValueError):
        r.translate(origin="Jet0")

    # rotate around a non-supported axis
    with pytest.raises(ValueError):
        r.rotate(axis="Jet0", orientation=90)

    # status will be False if there are no enough subjets
    # then rotate and pixelate will not work
    r.with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)

    assert r.translate(origin="SubJet100").status is False
    assert r.rotate(axis="SubJet100", orientation=90).config == r.config
    assert (
        r.pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)]).config == r.config
    )


def test_show(event):
    r = Image(
        height="FatJet0.Constituents:.Phi",
        width="FatJet0.Constituents:.Eta",
        channel="FatJet0.Constituents:.Pt",
    ).read_ttree(event)
    r.show()

    r.with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
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
        height="FatJet0.Constituents:.Phi",
        width="FatJet0.Constituents:.Eta",
        channel="FatJet0.Constituents:.Pt",
    )
    assert Image.from_config(r.config).config == r.config

    r.with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
    assert Image.from_config(r.config).config == r.config

    r.translate(origin="SubJet0")
    assert Image.from_config(r.config).config == r.config

    r.rotate(axis="SubJet1", orientation=-90)
    assert Image.from_config(r.config).config == r.config

    r.pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    assert Image.from_config(r.config).config == r.config

    r = Image(
        height="FatJet0.Constituents:.Phi",
        width="FatJet0.Constituents:.Eta",
    )
    assert Image.from_config(r.config).config == r.config


def test_values(event):
    # values are nan if the image has not read a TTree
    r = Image(
        height="FatJet0.Constituents:.Phi",
        width="FatJet0.Constituents:.Eta",
    )

    assert isinstance(r.values, tuple)
    assert np.isnan(r.values).all()

    # values are not nan if the image has read a TTree
    r = (
        Image(
            height="FatJet0.Constituents:.Phi",
            width="FatJet0.Constituents:.Eta",
        )
        .read_ttree(event)
        .pixelate(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    )
    assert r.values.shape == (33, 33)
    assert not np.isnan(r.values).all()
