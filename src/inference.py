from src.predicate import Predicate
from src.database import Database
# from src.rules import FC
from src.fact import Fact
from typing import Tuple
import time


def sort(facts: list[Fact]) -> list[Fact]:
    types = [
        "coll",
        "cong",
        "midp",
        "para",
        "perp",
        "eqangle",
        "eqratio",
        "simtri",
        "contri",
        "cyclic",
        "circle",
    ]
    return sorted(facts, key=lambda x: types.index(x.type))


def inference_update(
        db: Database,
        predicates_to_add: list[Predicate]) -> Tuple[Database, set[Fact]]:
    """
    Add facts to a database and update the database until
    fixed point is reached
    Return the updated database, reward, 
    """

    facts_to_add = []
    for p in predicates_to_add:
        to_add = db._predicate_to_fact(p)
        if to_add not in facts_to_add:
            facts_to_add.append(to_add)
    facts_to_add = sort(facts_to_add)

    increased_facts = []
    used = {}

    print("Initializing...\n")
    print("\n".join(str(f) for f in facts_to_add), "\n", "-" * 50, "\n")

    for fact in facts_to_add:
        if db.containsFact(fact):
            continue
        db.addFact(fact)
        increased_facts.append(fact)

    print(db)

    print("Start forward chaining...", "\n")

    now0 = now = time.time()

    while facts_to_add:
        print("\n")
        len_0 = len(facts_to_add)
        print("Current size", len_0)

        fact = facts_to_add.pop(0)

        if fact in used and used[fact] == db.version:
            print(fact, " skip, time spend", f"{time.time() - now:.2f}")
            now = time.time()
            continue
        else:
            used[fact] = db.version

        print(fact, " deducting...")

        all_pforms = db._predicate_all_forms(fact)
        new_facts = []
        for p in all_pforms:
            new_facts += FC(database=db).deduct(p)

        for new_fact in set(new_facts):
            if db.containsFact(new_fact):
                continue

            facts_to_add.append(new_fact)

        facts_to_add = sort(facts_to_add)

        lapsed = time.time() - now
        now = time.time()
        print(
            len(facts_to_add) - len_0, " new facts,  time spent",
            f"{lapsed:.2f}")
        if lapsed >= 0.1:
            print("<<<<<<TOOO LONG>>>>>")

        if not db.containsFact(fact):
            db.addFact(fact)
            increased_facts.append(fact)
            db.version_update()

    print(time.time() - now0)

    return db, sort(increased_facts)


def test():
    predicates_to_add = [
        [
            Predicate("perp", ["A", "D", "B", "C"]),
            Predicate("coll", ["B", "D", "C"]),
        ],
        [
            Predicate("perp", ["B", "E", "A", "C"]),
            Predicate("coll", ["A", "E", "C"]),
            Predicate("coll", ["B", "H", "E"]),
            Predicate("coll", ["A", "D", "H"]),
        ],
        [
            Predicate("coll", ["C", "H", "F"]),
            Predicate("coll", ["A", "F", "B"])
        ],
    ]

    db = Database()
    for predicates in predicates_to_add:
        db, increased_facts = inference_update(db, predicates)
        print(db.version)
        print(increased_facts)
        print(db)


def test2():
    predicates_to_add = [
        Predicate("coll", ["A", "H", "D"]),
        Predicate("coll", ["B", "H", "E"]),
        Predicate("coll", ["B", "D", "C"]),
        Predicate("coll", ["A", "E", "C"]),
        Predicate("coll", ["C", "H", "F"]),
        Predicate("coll", ["A", "F", "B"]),
        Predicate("perp", ["A", "D", "B", "C"]),
        Predicate("perp", ["B", "E", "A", "C"])
    ]
    db = Database()
    db, increased_facts = inference_update(db, predicates_to_add)
    print(db.version)
    print(db)


if __name__ == "__main__":
    test2()
