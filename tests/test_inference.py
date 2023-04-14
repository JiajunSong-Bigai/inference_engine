"""
inference.py testing module
"""

import pytest
from src.predicate import Predicate
from src.database import Database
from src.inference import inference_update


def test_01():
    """
    The full problem is

    Predicate("coll", ["A", "H", "D"]),
    Predicate("coll", ["B", "H", "E"]),
    Predicate("coll", ["B", "D", "C"]),
    Predicate("coll", ["A", "E", "C"]),
    Predicate("coll", ["C", "H", "F"]),
    Predicate("coll", ["A", "F", "B"]),
    Predicate("perp", ["A", "D", "B", "C"]),
    Predicate("perp", ["B", "E", "A", "C"])
    """
    steps = [
        [
            # step 1
            Predicate("perp", ["A", "D", "B", "C"]),
            Predicate("coll", ["B", "D", "C"]),
        ],
        [
            # step 2
            Predicate("perp", ["B", "E", "A", "C"]),
            Predicate("coll", ["A", "E", "C"]),
            Predicate("coll", ["B", "H", "E"]),
            Predicate("coll", ["A", "D", "H"]),
        ],
        [
            # step 3
            Predicate("coll", ["C", "H", "F"]),
            Predicate("coll", ["A", "F", "B"])
        ],
    ]

    db = Database()
    # step 1
    db, increased_facts = inference_update(db, steps[0])

    assert len(db.lines) == 2
    assert len(db.eqangleFacts) == 1
    assert len(db.simtriFacts) == 0
    assert len(db.circles) == 0
    assert len(increased_facts) == 3

    # step 1
    db, increased_facts = inference_update(db, steps[1])

    assert len(db.lines) == 7
    assert len(db.eqangleFacts) == 3
    assert len(db.simtriFacts) == 3
    assert len(db.circles) == 2
    assert len(increased_facts) == 24

    # step 2
    db, increased_facts = inference_update(db, steps[2])

    assert len(db.lines) == 9
    assert len(db.eqangleFacts) == 7
    assert len(db.simtriFacts) == 8
    assert len(db.circles) == 6
    assert len(increased_facts) == 47


def test_02():
    """
    The full problem is

    Predicate("coll", ["M", "N", "E"]),
    Predicate("coll", ["A", "K", "B"]),
    Predicate("coll", ["B", "E", "C"]),
    Predicate("coll", ["C", "N", "K"]),
    Predicate("para", ["A", "B", "C", "D"]),
    Predicate("midp", ["M", "A", "C"]),
    Predicate("midp", ["N", "B", "D"])
    """

    steps = [
        [
            Predicate("para", ["A", "B", "C", "D"]),
        ],
        [
            Predicate("midp", ["M", "A", "C"]),
        ],
        [
            Predicate("midp", ["N", "B", "D"]),
        ],
        [
            Predicate("coll", ["M", "N", "E"]),
            Predicate("coll", ["B", "E", "C"]),
        ],
        [
            Predicate("coll", ["C", "N", "K"]),
            Predicate("coll", ["A", "K", "B"]),
        ],
    ]

    # db = Database()
    # # step 1
    # db, increased_facts = inference_update(db, steps[0])

    # assert len(db.lines) == 2
    # assert len(db.eqangleFacts) == 1
    # assert len(db.simtriFacts) == 0
    # assert len(db.circles) == 0
    # assert len(increased_facts) == 3
    db = Database()
    current_objects = []
    for i, step in enumerate(steps):
        print("STEP", i + 1)

        db, increased_facts = inference_update(db, step)
        for fact in increased_facts:
            if all(o in current_objects for o in fact.objects):
                print("FOUND!!!!!!", fact)
        current_objects = db.objects
        print("=" * 80, "\n")
