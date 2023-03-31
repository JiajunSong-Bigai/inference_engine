# A note companioned with the implementation

## Difference between `fact` and `predicate`

- Fact and Predicate are different in the database. At the top level, the facts satisfying each predicate are represented by a list of structures as below

Data Structures

1. coll -> Line Dict
    Let n be the number of points on the line. We need n(n-1)(n-2) predicate forms.

2. para -> ParaLine(L1, L2, L3)
    Let l1 and l2 contains n1 and n2 points. We need 2n1(n1-1)n2(n2-1) predicate forms.

3. perp -> PerpLine(L1, L2)
    Let l1 and l2 contains n1 and n2 points. We need 2n1(n1-1)n2(n2-1) predicate forms.

4. eqangle -> EqualAngle(A1, A2)

5. cong -> Cong Dict

6. eqratio -> EqualRatio(R1, R2)

7. simtri -> SimTri(T1, T2)



## Predicates

- coll(A,B,C)
- para(A,B,C,D)
- eqangle(A,B,C,D,E,F,G,H)
- cong(A,B,C,D)
- eqratio(A,B,C,D,E,F,G,H)
- simtri(contri)(A,B,C,E,F,G)
- circle(O,A,B,C)
- cyclic(A,B,C,D)


## Database Implementation Details

1. The database should be managed incrementally. The operations we need are
    - DB(with existing facts) + new facts -> New DB(with fixed point facts)

DB structure

- lines
- congs
- mid facts
- eqangle / eqratio facts
- para facts
- perp facts
- circle facts


The process of reaching the fixed point

- Input: DB with existing facts, A list of new facts waited to be added
- Output: New DB with updated facts, which has reached the fixed points


Algorithm 1 (DB, facts_to_add) -> new DB


WHILE facts_to_add NOT EMPTY

    fact = facts_to_add.pop(0)

    # ? fact could be used before
    # if the fact was used and the database is the same
    # then no need to update
    # we need to record the version of the database

    IF fact IN used AND used[fact] == DB.version
        CONTINUE

    all_pforms = DB.all_pforms(fact)

    new_facts = { all_rules(p) for p in all_pforms }

    FOR new_fact IN new_facts

        IF DB.contains(new_fact) CONTINUE

        facts_to_add.append(new_fact)

    IF NOT DB.contains(fact)
        DB.add(fact)           # all newly added facts should be here
        DB.version_update()

