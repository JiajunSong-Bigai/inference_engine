from src.fact import Fact


def test_01():
    f1 = Fact("coll", ["A", "B", "C"])
    f2 = Fact("coll", ["A", "B", "C"])
    f3 = Fact("coll", ["A", "D", "E"])

    assert f1 == f2
    assert f1 in [f2]
    assert f1 != f3