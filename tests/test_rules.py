import pytest
from src.predicate import Predicate
from src.prover import Prover


def test_rd1():
    hypotheses = [Predicate("coll", ["A", "B", "C"])]
    quest = Predicate("coll", ["A", "C", "B"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd2():
    hypotheses = [Predicate("coll", ["A", "B", "C"])]
    quest = Predicate("coll", ["B", "A", "C"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd3():
    hypotheses = [
        Predicate("coll", ["A", "B", "C"]),
        Predicate("coll", ["A", "B", "D"])
    ]
    quest = Predicate("coll", ["C", "D", "A"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd4():
    hypotheses = [Predicate("para", ["A", "B", "C", "D"])]
    quest = Predicate("para", ["A", "B", "D", "C"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd5():
    hypotheses = [Predicate("para", ["A", "B", "C", "D"])]
    quest = Predicate("para", ["C", "D", "A", "B"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


# skiping d6 to d10
# perp is not implemented yet


def test_rd11():
    hypotheses = [Predicate("midp", ["M", "B", "A"])]
    quest = Predicate("midp", ["M", "A", "B"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


# skiping d12 to d17
# cyclic is not implemented yet


def test_rd18():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "P", "Q", "U", "V"])
    ]
    quest = Predicate("eqangle", ["B", "A", "C", "D", "P", "Q", "U", "V"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd19():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "P", "Q", "U", "V"])
    ]
    quest = Predicate("eqangle", ["C", "D", "A", "B", "U", "V", "P", "Q"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd20():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "P", "Q", "U", "V"])
    ]
    quest = Predicate("eqangle", ["P", "Q", "U", "V", "A", "B", "C", "D"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd21():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "P", "Q", "U", "V"])
    ]
    quest = Predicate("eqangle", ["A", "B", "P", "Q", "C", "D", "U", "V"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd22():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
        Predicate("eqangle", ["P", "Q", "U", "V", "E", "F", "G", "H"])
    ]
    quest = Predicate("eqangle", ["A", "B", "C", "D", "E", "F", "G", "H"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd23():
    hypotheses = [Predicate("cong", ["A", "B", "C", "D"])]
    quest = Predicate("cong", ["A", "B", "D", "C"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd24():
    hypotheses = [Predicate("cong", ["A", "B", "C", "D"])]
    quest = Predicate("cong", ["C", "D", "A", "B"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd25():
    hypotheses = [
        Predicate("cong", ["A", "B", "C", "D"]),
        Predicate("cong", ["C", "D", "E", "F"])
    ]
    quest = Predicate("cong", ["A", "B", "E", "F"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


# skip d26 to d38


def test_rd39():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "P", "Q", "C", "D", "P", "Q"]),
    ]
    quest = Predicate("para", ["A", "B", "C", "D"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd40():
    hypotheses = [
        Predicate(
            "coll",
            ["P", "Q", "R"]),  # adding this to create instance for P and Q
        Predicate("para", ["A", "B", "C", "D"]),
    ]
    quest = Predicate("eqangle", ["A", "B", "P", "Q", "C", "D", "P", "Q"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


# skip d41 to d43


def test_rd44():
    hypotheses = [
        Predicate("midp", ["E", "A", "B"]),
        Predicate("midp", ["F", "A", "C"])
    ]
    quest = Predicate("para", ["E", "F", "B", "C"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)
