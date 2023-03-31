import pytest
from src.predicate import Predicate
from src.fact import Fact
from src.database import Database


def test_p1():
    predicates = [
        Predicate("coll", ["A", "B", "C"]),
        Predicate("coll", ["E", "F", "G"])
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)
    assert db.lines == {'line1': {'B', 'A', 'C'}, 'line2': {'F', 'G', 'E'}}


def test_p2():
    predicates = [
        Predicate("coll", ["A", "B", "C"]),
        Predicate("coll", ["A", "D", "E"])
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)
    assert db.lines == {'line1': {'A', 'B', 'C'}, 'line2': {'E', 'A', 'D'}}


def test_p3():
    predicates = [
        Predicate("coll", ["A", "B", "C"]),
        Predicate("coll", ["A", "D", "E"]),
        Predicate("coll", ["A", "B", "D"])
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)
    assert db.lines == {'line1': {'D', 'E', 'C', 'B', 'A'}}


def test_p4():
    predicates = [
        Predicate("coll", ["A", "B", "C"]),
        Predicate("para", ["A", "B", "D", "E"]),
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)

    s = "\n"
    s += "\n".join(str(p) for p in predicates)
    s += "\n" + str(db)
    print(s)


def test_p5():
    predicates = [
        Predicate("perp", ["A", "C", "B", "C"]),
        Predicate("midp", ["D", "A", "B"]),
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)
    s = "\n"
    s += "\n".join(str(p) for p in predicates)
    s += "\n" + str(db)
    print(s)


def test_p6():
    predicates = [
        Predicate("cong", ["A", "B", "C", "D"]),
        Predicate("cong", ["A", "B", "E", "F"]),
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)
    s = "\n"
    s += "\n".join(str(p) for p in predicates)
    s += "\n" + str(db)
    print(s)


def test_p7():
    predicates = [
        Predicate("cong", ["A", "B", "C", "D"]),
        Predicate("cong", ["E", "F", "P", "Q"]),
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)
    s = "\n"
    s += "\n".join(str(p) for p in predicates)
    s += "\n" + str(db)
    print(s)


def test_p8():
    predicates = [
        Predicate("cong", ["A", "B", "C", "D"]),
        Predicate("cong", ["E", "F", "P", "Q"]),
        Predicate("cong", ["A", "B", "P", "Q"])
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)
    s = "\n"
    s += "\n".join(str(p) for p in predicates)
    s += "\n" + str(db)
    print(s)


def test_p9():
    predicates = [
        Predicate("simtri", ["A", "B", "C", "P", "Q", "R"]),
        Predicate("simtri", ["A", "C", "B", "P", "R", "Q"]),
        Predicate("simtri", ["A", "B", "C", "D", "E", "F"]),
    ]
    db = Database()
    for predicate in predicates:
        db.addPredicate(predicate=predicate)
    s = "\n"
    s += "\n".join(str(p) for p in predicates)
    s += "\n" + str(db)
    print(s)
