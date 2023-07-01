from pathlib import Path

from sklearn.datasets import load_iris

from hml.methods.trees import BoostedDecisionTree


def test_boosted_decision_tree():
    dataset = load_iris()
    x = dataset.data
    y = dataset.target
    m = BoostedDecisionTree()
    m.compile()
    m.fit(x, y)

    assert m.predict(x).shape == y.shape
    assert m.predict_proba(x).shape == (y.shape[0], len(set(y)))
    assert isinstance(m.summary(), str)
    assert isinstance(m.n_parameters, int)

    m.save("tests/data/boosted_decision_tree1.pkl")
    assert Path("tests/data/boosted_decision_tree1.pkl").exists()
    m.save("tests/data/boosted_decision_tree2")
    assert Path("tests/data/boosted_decision_tree2.pkl").exists()
