"""prover.py

fof(ruleD39,axiom,
    ! [A,B,C,D,P,Q] :
      ( eqangle(A,B,P,Q,C,D,P,Q)
     => para(A,B,C,D) ) ).

fof(ruleD40,axiom,
    ! [A,B,C,D,P,Q] :
      ( para(A,B,C,D)
     => eqangle(A,B,P,Q,C,D,P,Q) ) ).

fof(ruleD42a,axiom,
    ! [A,B,P,Q] :
      ( ( eqangle(P,A,P,B,Q,A,Q,B)
        & ~ coll(P,Q,A) )
     => cyclic(A,B,P,Q) ) ).

fof(ruleD42b,axiom,
    ! [A,B,P,Q] :
      ( ( eqangle(P,A,P,B,Q,A,Q,B)
        & ~ coll(P,Q,B) )
     => cyclic(A,B,P,Q) ) ).


fof(ruleD44,axiom,
    ! [A,B,C,E,F] :
      ( ( midp(E,A,B)
        & midp(F,A,C) )
     => para(E,F,B,C) ) ).


Data-driven Forward chaining

1. Maintain NEW_FACTS_LIST and DATABASE, and initialize both of them to be the list of hypotheses
2. Pop the first fact/predicate `d` from NEW_FACTS_LIST
    1. Fetch rules based on the type of the fact/predicate
    2. Apply rules, obtain new fact `d'`
    3. Insert `d'` into the DATABASE
    4. IF `d'` is not in the NEWFACTSLIST, attach it to the list
3. Continue step 2 until the NEWFACTSLIST is empty
"""
import itertools

from src.database import Database
from src.predicate import Predicate


class Prover:

    def __init__(self, hypotheses: list[Predicate]) -> None:
        self.database = Database()
        self.newFactsList = []

        for h in hypotheses:
            self.database.add(h)
            self.newFactsList.append(h)

    def fixedpoint(self):
        while self.newFactsList:
            d = self.newFactsList.pop()
            if d.type == "midp":
                self._ruleD44(d)
            if d.type == "para":
                self._ruleD40(d)

        return self.database

    def _ruleD44(self, predicate: Predicate):
        """
        midp(E,A,B) & midp(F,A,C) => para(E,F,B,C)
        
        Given E, A, B and generate predicates
        """
        E, A, B = predicate.points
        predicates = []
        for midfact in self.database.midpFacts:
            p1, p2, p3 = midfact

            # [p1, p2, p3]
            # p1 != E, p2 = A, p3 != B
            if p1 != E and p2 == A and p3 != B and not self.database.isCollinear(
                [A, B, p3]):
                predicate = Predicate(type="para", points=[E, p1, B, p3])
                predicates.append(predicate)
            # [p1, p3, p2]
            # p1 != E, p3 = A, p2 != B
            elif p1 != E and p3 == A and p2 != B and not self.database.isCollinear(
                [A, B, p2]):
                predicate = Predicate(type="para", points=[E, p3, B, p2])
                predicates.append(predicate)

        for predicate in predicates:
            self.database.add(predicate)

            if predicate not in self.newFactsList:
                self.newFactsList.append(predicate)

    def _ruleD40(self, predicate: Predicate):
        """
        para(A,B,C,D) => eqangle(A,B,P,Q,C,D,P,Q)
        """
        p1, p2, p3, p4 = predicate.points
        name1 = self.database._addLine([p1, p2])
        name2 = self.database._addLine([p3, p4])

        predicates = []
        for n, line in self.database.lineDict.items():
            if n in [name1, name2]:
                continue

            for ppair in itertools.combinations(line, 2):
                predicate = Predicate(type="eqangle",
                                      points=[
                                          p1, p2, ppair[0], ppair[1], p3, p4,
                                          ppair[0], ppair[1]
                                      ])
                predicates.append(predicate)

        for predicate in predicates:
            self.database.add(predicate)

            if predicate not in self.newFactsList:
                self.newFactsList.append(predicate)
