from src.predicate import Predicate
from src.database import Database
from src.rules import FC
from src.fact import Fact
from typing import Tuple
import time


def inference_update(
    db: Database,
    predicates_to_add: list[Predicate],
    verbose=False,
) -> Tuple[Database, set[Fact]]:
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
    facts_to_add = sorted(facts_to_add)

    increased_facts = []
    used = {}

    for fact in facts_to_add:
        if db.containsFact(fact):
            continue
        db.addFact(fact)
        increased_facts.append(fact)

    if verbose: print(db)

    while facts_to_add:

        fact = facts_to_add.pop(0)

        if fact in used and used[fact] == db.version:
            continue
        else:
            used[fact] = db.version

        if verbose: print("USING:", fact)

        all_pforms = db._predicate_all_forms(fact)

        new_facts = []
        for p in all_pforms:
            new_facts += FC(database=db).deduct(p)

        if verbose: print("\nEQANGLES:")
        for eqangles in db.eqangleFacts:
            if verbose: print(eqangles)

        if verbose: print("\nNEW FACTS:")
        for new_fact in set(new_facts):
            if db.containsFact(new_fact) or fact in facts_to_add:
                continue

            facts_to_add.append(new_fact)
            if verbose: print(new_fact)

        facts_to_add = sorted(set(facts_to_add))

        if not db.containsFact(fact):
            db.addFact(fact)
            increased_facts.append(fact)
            db.version_update()

        if verbose:
            print("\nTOADD_FACT_LIST:")
            print("\n".join(str(f) for f in facts_to_add))
            print("=" * 80, "\n")

    return db, sorted(increased_facts)


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
        print("\nFINISHED:")
        print(db)
        print("LINES:")
        for line in db.lines:
            print(line, db.lines[line])
        print("=" * 80)
        print("=" * 80)


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
    print("\n\n", db.version)
    print(db)


if __name__ == "__main__":
    test()
