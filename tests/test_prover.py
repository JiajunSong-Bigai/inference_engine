"""
Testing problems
"""
import pytest
from src.predicate import Predicate
from src.prover import Prover
from src.util import parse_predicates_from_file


def test_01():
    hypotheses = parse_predicates_from_file("problems/p1")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    quests = [
        Predicate("coll", ["A", "B", "D"]),
        Predicate("coll", ["A", "C", "D"])
    ]
    for quest in quests:
        assert prover.prove(quest)


def test_02():
    hypotheses = parse_predicates_from_file("problems/p2")
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    quests = [
        Predicate("para", ["A", "C", "D", "E"]),
        Predicate("para", ["D", "E", "C", "B"])
    ]
    for quest in quests:
        assert prover.prove(quest)


def test_03():
    hypotheses = parse_predicates_from_file("problems/p3")
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    quests = [
        Predicate("coll", ["A", "B", "D"]),
        Predicate("coll", ["A", "C", "E"]),
        Predicate("para", ["D", "E", "B", "C"]),
        Predicate("cong", ["A", "D", "D", "B"]),
        Predicate("eqangle", ["A", "D", "D", "E", "A", "D", "B", "C"]),
        Predicate("eqangle", ["A", "B", "D", "E", "A", "D", "B", "C"]),
        Predicate("eqangle", ["A", "B", "D", "E", "A", "B", "B", "C"]),
        Predicate("eqangle", ["D", "E", "A", "B", "C", "B", "A", "B"]),
        Predicate("eqangle", ["A", "E", "D", "E", "A", "C", "B", "C"]),
        Predicate("eqangle", ["A", "D", "D", "E", "A", "B", "B", "C"]),
        Predicate("simtri", ["A", "D", "E", "A", "B", "C"]),
    ]
    for quest in quests:
        assert prover.prove(quest), f"{quest} not proved"


def test_04():
    hypotheses = parse_predicates_from_file("problems/p4")
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    quests = [
        Predicate("cong", ["K", "M", "K", "N"]),
        Predicate("eqangle", ["A", "B", "M", "N", "M", "N", "C", "D"]),
        Predicate("simtri", ["B", "K", "N", "B", "D", "C"]),
    ]
    for quest in quests:
        assert prover.prove(quest), f"{quest} not proved"


@pytest.mark.skip()
def test_05():
    hypotheses = parse_predicates_from_file("problems/p5")
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    print(prover.database)


def test_06():
    hypotheses = parse_predicates_from_file("problems/p6")
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    quests = [
        Predicate("cong", ["A", "D", "C", "D"]),
        Predicate("circle", ["D", "A", "B", "C"])
    ]
    for quest in quests:
        assert prover.prove(quest), f"{quest} not proved"


def test_07():
    hypotheses = parse_predicates_from_file("problems/p7")
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    # quests = [
    #     Predicate("cong", ["A", "D", "C", "D"]),
    #     Predicate("circle", ["D", "A", "B", "C"])
    # ]
    # for quest in quests:
    #     assert prover.prove(quest), f"{quest} not proved
    print(prover.database)