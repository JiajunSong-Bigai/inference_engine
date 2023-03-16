from src.predicate import Predicate
import pytest


def test_01():
    p1 = Predicate("para", ["A", "B", "C", "D"])
    p2 = Predicate("para", ["B", "A", "C", "D"])
    p3 = Predicate("para", ["A", "B", "C", "D"])

    assert p1 != p2
    assert p1 == p3
    assert p1 not in [p2]
    assert p2 not in [p1]
    assert p1 in [p2, p3]
    assert p1 in [p3]
    assert p1 in [p1]