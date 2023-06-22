import os


def test_mg5():
    mg5_path = os.popen("which mg5_aMC").read().strip()
    assert mg5_path != "", "mg5_aMC is not an available command"
