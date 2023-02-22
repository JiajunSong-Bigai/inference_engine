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


def test_rd6():
    hypotheses = [
        Predicate("para", ["A", "B", "C", "D"]),
        Predicate("para", ["C", "D", "E", "F"])
    ]
    quest = Predicate("para", ["A", "B", "E", "F"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd7():
    hypotheses = [Predicate("perp", ["A", "B", "C", "D"])]
    quest = Predicate("perp", ["A", "B", "D", "C"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd8():
    hypotheses = [Predicate("perp", ["A", "B", "C", "D"])]
    quest = Predicate("perp", ["C", "D", "A", "B"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd9():
    hypotheses = [
        Predicate("perp", ["A", "B", "C", "D"]),
        Predicate("perp", ["C", "D", "E", "F"])
    ]
    quest = Predicate("para", ["A", "B", "E", "F"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd10():
    hypotheses = [
        Predicate("para", ["A", "B", "C", "D"]),
        Predicate("perp", ["C", "D", "E", "F"])
    ]
    quest = Predicate("perp", ["A", "B", "E", "F"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


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


def test_rd26():
    hypotheses = [
        Predicate("eqratio", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
    ]
    quest = Predicate("eqratio", ["B", "A", "C", "D", "P", "Q", "U", "V"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd27():
    hypotheses = [
        Predicate("eqratio", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
    ]
    quest = Predicate("eqratio", ["C", "D", "A", "B", "U", "V", "P", "Q"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd28():
    hypotheses = [
        Predicate("eqratio", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
    ]
    quest = Predicate("eqratio", ["P", "Q", "U", "V", "A", "B", "C", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd29():
    hypotheses = [
        Predicate("eqratio", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
    ]
    quest = Predicate("eqratio", ["A", "B", "P", "Q", "C", "D", "U", "V"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd30():
    hypotheses = [
        Predicate("eqratio", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
        Predicate("eqratio", ["P", "Q", "U", "V", "E", "F", "G", "H"])
    ]
    quest = Predicate("eqratio", ["A", "B", "C", "D", "E", "F", "G", "H"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd31():
    hypotheses = [Predicate("simtri", ["A", "C", "B", "P", "R", "Q"])]
    quest = Predicate("simtri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd32():
    hypotheses = [Predicate("simtri", ["B", "A", "C", "Q", "P", "R"])]
    quest = Predicate("simtri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd33():
    hypotheses = [Predicate("simtri", ["P", "Q", "R", "A", "B", "C"])]
    quest = Predicate("simtri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd34():
    hypotheses = [
        Predicate("simtri", ["A", "B", "C", "E", "F", "G"]),
        Predicate("simtri", ["E", "F", "G", "P", "Q", "R"])
    ]
    quest = Predicate("simtri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd35():
    hypotheses = [Predicate("contri", ["A", "C", "B", "P", "R", "Q"])]
    quest = Predicate("contri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd36():
    hypotheses = [Predicate("contri", ["B", "A", "C", "Q", "P", "R"])]
    quest = Predicate("contri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd37():
    hypotheses = [Predicate("contri", ["P", "Q", "R", "A", "B", "C"])]
    quest = Predicate("contri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd38():
    hypotheses = [
        Predicate("contri", ["A", "B", "C", "E", "F", "G"]),
        Predicate("contri", ["E", "F", "G", "P", "Q", "R"])
    ]
    quest = Predicate("contri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


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


def test_rd45():
    hypotheses = [
        Predicate("midp", ["E", "A", "B"]),
        Predicate("para", ["E", "F", "B", "C"]),
        Predicate("coll", ["F", "A", "C"])
    ]
    quest = Predicate("midp", ["F", "A", "C"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd46():
    hypotheses = [Predicate("cong", ["O", "A", "O", "B"])]
    quest = Predicate("eqangle", ["O", "A", "A", "B", "A", "B", "O", "B"])

    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd47():
    hypotheses = [
        Predicate("eqangle", ["O", "A", "A", "B", "A", "B", "O", "B"])
    ]
    quest = Predicate("cong", ["O", "A", "O", "B"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


# skip 48, 49, 50, 51; involves circle


def test_rd52perp():
    hypotheses = [
        Predicate("perp", ["A", "B", "B", "C"]),
        Predicate("midp", ["M", "A", "C"])
    ]
    quest = Predicate("cong", ["A", "M", "B", "M"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd52midp():
    hypotheses = [
        Predicate("midp", ["M", "A", "C"]),
        Predicate("perp", ["A", "B", "B", "C"]),
    ]
    quest = Predicate("cong", ["A", "M", "B", "M"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


# skip 53, 54; involves circle


def test_rd55perp():
    hypotheses = [
        Predicate("perp", ["O", "M", "A", "B"]),
        Predicate("midp", ["M", "A", "B"]),
    ]
    quest = Predicate("cong", ["O", "A", "O", "B"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd55midp():
    hypotheses = [
        Predicate("midp", ["M", "A", "B"]),
        Predicate("perp", ["O", "M", "A", "B"]),
    ]
    quest = Predicate("cong", ["O", "A", "O", "B"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd56():
    hypotheses = [
        Predicate("cong", ["A", "P", "B", "P"]),
        Predicate("cong", ["A", "Q", "B", "Q"]),
    ]
    quest = Predicate("perp", ["A", "B", "P", "Q"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


# skip 57


def test_rd58():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "B", "C", "P", "Q", "Q", "R"]),
        Predicate("eqangle", ["A", "C", "B", "C", "P", "R", "Q", "R"]),
        # not coll(A,B,C)
    ]
    quest = Predicate("simtri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd59():
    hypotheses = [Predicate("simtri", ["A", "B", "C", "P", "Q", "R"])]
    quest = Predicate("eqratio", ["A", "B", "A", "C", "P", "Q", "P", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd60():
    hypotheses = [Predicate("simtri", ["A", "B", "C", "P", "Q", "R"])]
    quest = Predicate("eqangle", ["A", "B", "B", "C", "P", "Q", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd61():
    hypotheses = [
        Predicate("simtri", ["A", "B", "C", "P", "Q", "R"]),
        Predicate("cong", ["A", "B", "P", "Q"])
    ]
    quest = Predicate("contri", ["A", "B", "C", "P", "Q", "R"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd62():
    hypotheses = [Predicate("contri", ["A", "B", "C", "P", "Q", "R"])]
    quest = Predicate("cong", ["A", "B", "P", "Q"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd63():
    hypotheses = [
        Predicate("midp", ["M", "A", "B"]),
        Predicate("midp", ["M", "C", "D"])
    ]
    quest = Predicate("para", ["A", "C", "B", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd64():
    hypotheses = [
        Predicate("midp", ["M", "A", "B"]),
        Predicate("para", ["A", "C", "B", "D"]),
        Predicate("para", ["A", "D", "B", "C"])
    ]
    quest = Predicate("midp", ["M", "C", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd65():
    hypotheses = [
        Predicate("para", ["A", "B", "C", "D"]),
        Predicate("coll", ["O", "A", "C"]),
        Predicate("coll", ["O", "B", "D"])
    ]
    quest = Predicate("eqratio", ["O", "A", "A", "C", "O", "B", "B", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd66():
    hypotheses = [
        Predicate("para", ["A", "B", "A", "C"]),
    ]
    quest = Predicate("coll", ["A", "B", "C"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd67():
    hypotheses = [
        Predicate("coll", ["A", "B", "C"]),
        Predicate("cong", ["A", "B", "A", "C"]),
    ]
    quest = Predicate("midp", ["A", "B", "C"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd68():
    hypotheses = [Predicate("midp", ["A", "B", "C"])]
    quest = Predicate("cong", ["A", "B", "A", "C"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd69():
    hypotheses = [Predicate("midp", ["A", "B", "C"])]
    quest = Predicate("coll", ["A", "B", "C"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd70():
    hypotheses = [
        Predicate("midp", ["M", "A", "B"]),
        Predicate("midp", ["N", "C", "D"])
    ]
    quest = Predicate("eqratio", ["M", "A", "A", "B", "N", "C", "C", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd71():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "C", "D", "A", "B"])
        # not para(A,B,C,D)
    ]
    quest = Predicate("perp", ["A", "B", "C", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd72():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "C", "D", "A", "B"])
        # not perp(A,B,C,D)
    ]
    quest = Predicate("para", ["A", "B", "C", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd73():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
        Predicate("para", ["P", "Q", "U", "V"])
    ]
    quest = Predicate("para", ["A", "B", "C", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd74():
    hypotheses = [
        Predicate("eqangle", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
        Predicate("perp", ["P", "Q", "U", "V"])
    ]
    quest = Predicate("perp", ["A", "B", "C", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)


def test_rd75():
    hypotheses = [
        Predicate("cong", ["P", "Q", "U", "V"]),
        Predicate("eqratio", ["A", "B", "C", "D", "P", "Q", "U", "V"]),
    ]
    quest = Predicate("cong", ["A", "B", "C", "D"])
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    assert prover.prove(quest)
