# A note companioned with the implementation

## Difference between `fact` and `predicate`

- Fact and Predicate are different in the database. At the top level, the facts
satisfying each predicate are represented by a list of structures as below

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
