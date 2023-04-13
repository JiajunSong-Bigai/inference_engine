from src.fact import Fact


def test_01():
    f1 = Fact("coll", ["A", "B", "C"])
    f2 = Fact("coll", ["A", "B", "C"])
    f3 = Fact("coll", ["A", "D", "E"])

    assert f1 == f2
    assert f1 in [f2]
    assert f1 != f3


def test_02():
    f1 = Fact("coll", ["A", "B", "C"])
    f2 = Fact("coll", ["A", "B", "C"])
    f3 = Fact("coll", ["A", "D", "E"])
    f4 = Fact("perp", ["A", "B", "C", "D"])
    f5 = Fact("perp", ["A", "C", "C", "D"])
    f6 = Fact("eqangle", ["line1", "line2", "line3", "line4"])

    print(sorted([f2, f3, f1, f4, f5]))
    print(sorted((set([f1, f2, f3, f4, f5]))))

    print(sorted(set([f6, f6])))
