from pathlib import Path

import numpy as np

from hml.methods.cuts import CutBasedAnalysis as CBA
from hml.methods.cuts import plot_cuts


def test_cut_based_analysis():
    # Four features
    # Signal is at left, right, middle, and both sides respectively
    np.random.seed(42)
    feat1 = np.random.normal(0, size=10000)
    feat2 = np.random.normal(5, size=10000)
    feat3 = np.random.normal(0, size=10000)
    feat4 = np.append(
        np.random.normal(5, size=5000),
        np.random.normal(-5, size=5000),
    )

    sig = np.stack([feat1, feat2, feat3, feat4], axis=1)

    feat1 = np.random.normal(5, size=10000)
    feat2 = np.random.normal(0, size=10000)
    feat3 = np.append(
        np.random.normal(5, size=5000),
        np.random.normal(-5, size=5000),
    )
    feat4 = np.random.normal(0, size=10000)

    bkg = np.stack([feat1, feat2, feat3, feat4], axis=1)

    data = np.concatenate([sig, bkg])
    target = np.append(np.ones(len(sig)), np.zeros(len(bkg)))

    cba = CBA()
    cba.compile()
    cba.fit(data, target)
    y_pred = cba.predict(data)

    assert cba.signal_locations == ["left", "right", "middle", "both_sides"]
    assert y_pred.shape == target.shape

    for i in range(4):
        assert plot_cuts(sig[:, i], bkg[:, i], 100, cba.cuts[i], cba.signal_locations[i]) == None

    assert isinstance(cba.summary(), str)
    cba.save("tests/data/cut_based_analysis1.json")
    assert Path("tests/data/cut_based_analysis1.json").exists()
    cba.save("tests/data/cut_based_analysis2")
    assert Path("tests/data/cut_based_analysis2.json").exists()
