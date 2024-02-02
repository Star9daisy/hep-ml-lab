from hml.representations import Image


def test_image_rotate_first(event):
    image = Image(
        height="FatJet0.Constituents:.Phi",
        width="FatJet0.Constituents:.Eta",
        channel="FatJet0.Constituents:.Pt",
    )
    image.read_ttree(event)
    image.with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
    image.show()

    image.translate(origin="SubJet0")
    image.show()

    image.rotate(axis="SubJet1", orientation=-90)
    image.show()

    image.pixelated(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    image.show(as_point=True)
    image.show(norm="log")
    image.show(show_pixels=True)


def test_image_pixelate_first(event):
    image = Image(
        height="FatJet0.Constituents:.Phi",
        width="FatJet0.Constituents:.Eta",
        channel=None,
    )

    image.read_ttree(event)
    image.with_subjets("FatJet0.Constituents:", "kt", 0.3, 0)
    image.translate(origin="SubJet0")
    image.show()
    image.pixelated(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    image.show(as_point=True)
    image.show()
    image.rotate(axis="SubJet1", orientation=-90)
    image.show(as_point=True)
    image.show()
    image.show(show_pixels=True)
    image.pixelated(size=(33, 33), range=[(-1.6, 1.6), (-1.6, 1.6)])
    image.show(as_point=True)
    image.show()
    image.show(show_pixels=True)
