from src.newdatabase import Database
from src.newprover import Prover
from src.predicate import Predicate


def test_01():
    prover = Prover(hypotheses=[
        Predicate("perp", ["A", "C", "B", "C"]),
        Predicate("midp", ["D", "A", "B"])
    ])
    prover.fixedpoint()
    print(prover.database)


def test_02():
    prover = Prover(hypotheses=[
        Predicate("coll", ["A", "B", "P"]),
        Predicate("coll", ["A", "C", "Q"]),
        Predicate("simtri", ["A", "B", "C", "A", "P", "Q"])
    ])
    prover.fixedpoint()
    print(prover.database)


def test_03():
    prover = Prover(hypotheses=[
        Predicate("midp", ["D", "A", "B"]),
        Predicate("midp", ["E", "A", "C"])
    ])
    prover.fixedpoint()
    print(prover.database)


def test_04():
    prover = Prover(hypotheses=[
        Predicate("coll", ["M", "N", "E"]),
        Predicate("coll", ["A", "K", "B"]),
        Predicate("coll", ["B", "E", "C"]),
        Predicate("coll", ["C", "N", "K"]),
        Predicate("para", ["A", "B", "C", "D"]),
        Predicate("midp", ["M", "A", "C"]),
        Predicate("midp", ["N", "B", "D"])
    ])
    prover.fixedpoint()
    print(prover.database)


def test_05():
    prover = Prover(hypotheses=[
        Predicate("para", ["A", "B", "C", "D"]),
        Predicate("para", ["A", "D", "B", "C"]),
        Predicate("para", ["Q", "P", "B", "C"]),
        Predicate("para", ["Q", "B", "P", "C"]),
        #Predicate("eqangle", ["B", "A", "P", "A", "P", "C", "B", "C"])
    ])
    prover.fixedpoint()
    print(prover.database)
    print(prover.database.lines)


def test_06():
    prover = Prover(hypotheses=[
        Predicate("coll", ["A", "H", "D"]),
        Predicate("coll", ["B", "H", "E"]),
        Predicate("coll", ["B", "D", "C"]),
        Predicate("coll", ["A", "E", "C"]),
        Predicate("coll", ["C", "H", "F"]),
        Predicate("coll", ["A", "F", "B"]),
        Predicate("perp", ["A", "D", "B", "C"]),
        Predicate("perp", ["B", "E", "A", "C"])
    ])
    prover.fixedpoint()
    print(prover.database)
    print(prover.database.lines)


def test_07():
    prover = Prover(hypotheses=[
        Predicate("eqangle", ["A", "B", "B", "C", "P", "Q", "Q", "R"]),
        Predicate("cong", ["A", "B", "P", "Q"]),
        Predicate("cong", ["B", "C", "Q", "R"])
    ])
    prover.fixedpoint()
    print(prover.database)
    print(prover.database.lines)


import sys


def main():
    option = int(sys.argv[1])

    if option == 1:
        test_01()
    elif option == 2:
        test_02()
    elif option == 3:
        test_03()
    elif option == 4:
        test_04()
    elif option == 5:
        test_05()
    elif option == 6:
        test_06()
    elif option == 7:
        test_07()


if __name__ == "__main__":
    main()