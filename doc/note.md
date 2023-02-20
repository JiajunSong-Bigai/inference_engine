# A note companioned with the implementation

## Predicates

- coll(A,B,C)
- para(A,B,C,D)
- eqangle(A,B,C,D,E,F,G,H)
- cong(A,B,C,D)
- eqratio(A,B,C,D,E,F,G,H)
- simtri(contri)(A,B,C,E,F,G)

## A typical usage

- Get a predicate, whether inferred by the rules or given from the hypotheses.
- Convert the raw predicate to the form of facts stored in the database.
- Add the fact to the database and update.


Data Structures

1. coll -> Line Dict

2. para -> ParaLine(L1, L2)

3. eqangle -> EqualAngle(A1, A2)

4. cong -> Cong Dict

5. eqratio -> EqualRatio(R1, R2)

6. simtri -> SimTri(T1, T2)

