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

from src.database_ import Database
from src.predicate import Predicate
from src.primitives import Angle, Ratio, Point, Segment


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

    def prove(self, predicate: Predicate) -> bool:
        if predicate.type == "coll":
            for _, pointsOnLine in self.database.lines.items():
                if all(p in pointsOnLine for p in predicate.points):
                    return True
            return False

        if predicate.type == "midp":
            p1, p2, p3 = predicate.points
            p2, p3 = sorted([p2, p3])
            return [p1, p2, p3] in self.database.midpFacts

        if predicate.type == "para":
            p1, p2, p3, p4 = predicate.points
            name1 = self.database.matchLine([p1, p2])
            name2 = self.database.matchLine([p3, p4])

            for parafact in self.database.paraFacts:
                if name1 in parafact and name2 in parafact:
                    return True
            return False

        if predicate.type == "eqangle":
            p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points
            l1 = self.database.matchLine([p1, p2])
            l2 = self.database.matchLine([p3, p4])
            l3 = self.database.matchLine([p5, p6])
            l4 = self.database.matchLine([p7, p8])

            for angles in self.database.eqangleFacts:
                if Angle(l1, l2) in angles and Angle(l3, l4) in angles:
                    return True
                if Angle(l2, l1) in angles and Angle(l4, l3) in angles:
                    return True
                if Angle(l1, l3) in angles and Angle(l2, l4) in angles:
                    return True
            return False

        if predicate.type == "cong":
            p1, p2, p3, p4 = predicate.points
            s1 = Segment(p1, p2)
            s2 = Segment(p3, p4)

            for segments in self.database.congs.values():
                if s1 in segments and s2 in segments:
                    return True
            return False

        return False

    def _ruleD44(self, predicate: Predicate):
        """
        midp(E,A,B) & midp(F,A,C) => para(E,F,B,C)        
        """
        E, A, B = predicate.points
        predicates = []
        for midfact in self.database.midpFacts:
            p1, p2, p3 = midfact

            # [p1, p2, p3]
            # p1 != E, p2 = A, p3 != B
            if p1 != E and p2 == A and p3 != B and not self.prove(
                    Predicate("coll", [A, B, p3])):
                predicate = Predicate(type="para", points=[E, p1, B, p3])
                predicates.append(predicate)
            # [p1, p3, p2]
            # p1 != E, p3 = A, p2 != B
            elif p1 != E and p3 == A and p2 != B and not self.prove(
                    Predicate("coll", [A, B, p2])):
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
        name1 = self.database.matchLine([p1, p2])
        name2 = self.database.matchLine([p3, p4])

        predicates = []
        for n, line in self.database.lines.items():
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
