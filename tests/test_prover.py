from src.prover import Prover

from src.util import parse_predicates_from_file


def test_01():
    hypotheses = parse_predicates_from_file("problems/p1")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)


def test_02():
    hypotheses = parse_predicates_from_file("problems/p2")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)


def test_03():
    hypotheses = parse_predicates_from_file("problems/p3")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)


def test_04():
    hypotheses = parse_predicates_from_file("problems/p4")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)


def test_05():
    hypotheses = parse_predicates_from_file("problems/p5")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)


def test_06():
    hypotheses = parse_predicates_from_file("problems/p6")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)


def test_07():
    hypotheses = parse_predicates_from_file("problems/p7")
    prover = Prover(hypotheses=hypotheses)
    final_db = prover.fixedpoint()
    print(final_db)
