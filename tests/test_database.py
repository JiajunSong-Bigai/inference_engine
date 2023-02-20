import pytest
from src.util import parse_predicates_from_file
from src.database_ import Database


def test_p1():
    predicates = parse_predicates_from_file("problems/p1")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p2():
    predicates = parse_predicates_from_file("problems/p2")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p3():
    predicates = parse_predicates_from_file("problems/p3")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p4():
    predicates = parse_predicates_from_file("problems/p4")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p5():
    predicates = parse_predicates_from_file("problems/p5")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p6():
    predicates = parse_predicates_from_file("problems/p6")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p7():
    predicates = parse_predicates_from_file("problems/p7")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p8():
    predicates = parse_predicates_from_file("problems/p8")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p9():
    predicates = parse_predicates_from_file("problems/p9")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)


def test_p10():
    predicates = parse_predicates_from_file("problems/p10")
    db = Database()
    for p in predicates:
        db.add(p)

    print(db)
