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
    final_db = prover.fixedpoint()
    quests = [
        Predicate("para", ["A", "C", "D", "E"]),
        Predicate("para", ["D", "E", "C", "B"])
    ]
    for quest in quests:
        assert prover.prove(quest)


def test_07():
    hypotheses = parse_predicates_from_file("problems/p7")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
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


@pytest.mark.skip()
def test_08():
    hypotheses = parse_predicates_from_file("problems/p8")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)


# @pytest.mark.skip()
def test_09():
    hypotheses = parse_predicates_from_file("problems/p9")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)
