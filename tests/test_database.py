import pytest
from src.util import parse_predicates_from_file
from src.database import Database


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
