from src.primitives import Triangle, Segment, Ratio


def test_01():
    t1 = Triangle("A", "B", "C")
    t2 = Triangle("A", "C", "B")

    print(t1, t2)

    assert t1 == t2
    assert t2 in [t1]
    assert t1 in [t2]


def test_02():
    s1 = Segment("A", "B")
    s2 = Segment("B", "A")
    s3 = Segment("A", "C")

    print(s1, s2)

    assert s1 == s2
    assert s1 in [s2]
    assert len({s1, s2}.intersection({s1})) == 1
    assert len({s1, s2}.intersection({s3})) == 0


def test_03():
    r1 = Ratio("cong1", "cong2")
    r2 = Ratio("cong1", "cong2")

    print(r1, r2)

    print(set([r1, r2]))

    assert r1 == r2
    assert r1 in [r2]