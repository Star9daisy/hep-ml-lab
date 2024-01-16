from hml.generators import Madgraph5Run
from hml.representations import Image, Set
from hml.types import Path

DATA_DIR = Path("tests/data")
# run_tt = Madgraph5Run(DATA_DIR / "pp2tt", "run_01")
run_zz = Madgraph5Run(DATA_DIR / "pp2zz", "run_01")
# event_tt = next(iter(run_tt.events()))
event_zz = next(iter(run_zz.events()))


def test_image_rotate_first():
    image = Image(
        height="FatJet0.Constituents.Phi",
        width="FatJet0.Constituents.Eta",
        channel="FatJet0.Constituents.Pt",
    )
    image.read(event_zz)
    image.with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
    image.show()

    image.translate(origin="SubJet0")
    image.show()

    image.rotate(axis="SubJet1", orientation=-90)
    image.show()

    image.pixelize(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    image.show(as_point=True)
    image.show(norm="log")
    image.show(show_pixels=True)


def test_image_pixelize_first():
    image = Image(
        height="FatJet0.Constituents.Phi",
        width="FatJet0.Constituents.Eta",
        channel=None,
    )

    image.read(event_zz)
    image.with_subjets("FatJet0.Constituents", "kt", 0.3, 0)
    image.translate(origin="SubJet0")
    image.show()
    image.pixelize(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    image.show(as_point=True)
    image.show()
    image.rotate(axis="SubJet1", orientation=-90)
    image.show(as_point=True)
    image.show()
    image.show(show_pixels=True)
    image.pixelize(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    image.show(as_point=True)
    image.show()
    image.show(show_pixels=True)


def test_set():
    set = Set("FatJet0.Pt", "FatJet0.Eta", "FatJet0.Phi", "FatJet0.Mass")
    set.read(event_zz)

    assert set.names == ["FatJet0.Pt", "FatJet0.Eta", "FatJet0.Phi", "FatJet0.Mass"]
    assert set.values.shape == (4,)
