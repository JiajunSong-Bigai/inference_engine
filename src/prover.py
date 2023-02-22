"""prover.py

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
from src.primitives import Angle, Ratio, Point, Segment, Triangle


class Prover:

    def __init__(self, hypotheses: list[Predicate]) -> None:
        self.database = Database()
        self.newFactsList = []

        for h in hypotheses:
            self.database.add(h)
            self.newFactsList.append(h)

    def fixedpoint(self):
        predicates = []
        while self.newFactsList:
            d = self.newFactsList.pop(0)
            if not self.prove(d):
                self.database.add(d)
            if d.type == "midp":
                predicates += self._ruleD44(d)
                predicates += self._ruleD52midp(d)
            if d.type == "para":
                predicates += self._ruleD40(d)
                predicates += self._ruleD10para(d)
                predicates += self._ruleD45para(d)
            if d.type == "eqangle":
                predicates += self._ruleD39(d)
                predicates += self._ruleD47(d)
            if d.type == "cong":
                predicates += self._ruleD46(d)
            if d.type == "perp":
                predicates += self._ruleD09(d)
                predicates += self._ruleD10perp(d)
                predicates += self._ruleD52perp(d)

            for predicate in predicates:
                if self.prove(predicate):
                    continue
                self.newFactsList.append(predicate)

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

        if predicate.type == "eqratio":
            p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points
            c1 = self.database.matchCong([p1, p2])
            c2 = self.database.matchCong([p3, p4])
            c3 = self.database.matchCong([p5, p6])
            c4 = self.database.matchCong([p7, p8])

            for ratios in self.database.eqratioFacts:
                if Ratio(c1, c2) in ratios and Ratio(c3, c4) in ratios:
                    return True
                if Ratio(c2, c1) in ratios and Ratio(c4, c3) in ratios:
                    return True
                if Ratio(c1, c3) in ratios and Ratio(c2, c4) in ratios:
                    return True
                if Ratio(c3, c1) in ratios and Ratio(c4, c2) in ratios:
                    return True
            return False

        if predicate.type == "perp":
            p1, p2, p3, p4 = predicate.points
            l1 = self.database.matchLine([p1, p2])
            l2 = self.database.matchLine([p3, p4])
            return {l1, l2} in self.database.perpFacts

        if predicate.type == "simtri":
            p1, p2, p3, p4, p5, p6 = predicate.points
            t1 = Triangle(p1, p2, p3)
            t2 = Triangle(p4, p5, p6)
            for tris in self.database.simtriFacts:
                if t1 in tris and t2 in tris:
                    return True
            return False

        if predicate.type == "contri":
            p1, p2, p3, p4, p5, p6 = predicate.points
            t1 = Triangle(p1, p2, p3)
            t2 = Triangle(p4, p5, p6)
            for tris in self.database.contriFacts:
                if t1 in tris and t2 in tris:
                    return True
            return False

        raise ValueError("Invalid type of predicate ", predicate.type)

    def _ruleD09(self, predicate: Predicate):
        """
        perp(A,B,C,D) & perp(C,D,E,F) => para(A,B,E,F)
        """
        p1, p2, p3, p4 = predicate.points
        l1 = self.database.matchLine([p1, p2])
        l2 = self.database.matchLine([p3, p4])

        predicates = []
        # find perp(l2, ..) in perpfacts
        for lines in self.database.perpFacts:
            if l2 not in lines:
                continue
            if list(lines)[0] == l2:
                l3 = list(lines)[1]
            else:
                l3 = list(lines)[0]

            valid = all([l1 != l3, l2 != l3])
            if valid:
                for ppair in itertools.combinations(self.database.lines[l3],
                                                    2):
                    predicate = Predicate("para", [p1, p2, ppair[0], ppair[1]])
                    predicates.append(predicate)

        return predicates

    def _ruleD10para(self, predicate: Predicate):
        """
        para(A,B,C,D) & perp(C,D,E,F) => perp(A,B,E,F)
        """
        p1, p2, p3, p4 = predicate.points
        l1 = self.database.matchLine([p1, p2])
        l2 = self.database.matchLine([p3, p4])

        predicates = []
        for lines in self.database.perpFacts:
            if l2 not in lines:
                continue
            if l2 == list(lines)[0]:
                l3 = list(lines)[1]
            else:
                l3 = list(lines)[0]

            valid = all([l2 != l3, l1 != l3])
            if valid:
                for ppair in itertools.combinations(self.database.lines[l3],
                                                    2):
                    predicates.append(
                        Predicate("perp", [p1, p2, ppair[0], ppair[1]]))

        return predicates

    def _ruleD10perp(self, predicate: Predicate):
        """
        perp(C,D,E,F) & para(A,B,C,D) => perp(A,B,E,F)
        """
        p1, p2, p3, p4 = predicate.points
        l1 = self.database.matchLine([p1, p2])
        l2 = self.database.matchLine([p3, p4])

        predicates = []
        for lines in self.database.paraFacts:
            if l1 not in lines:
                continue

            otherlines = [l for l in list(lines) if not l in [l1, l2]]
            for otherline in otherlines:
                for ppair in itertools.combinations(
                        self.database.lines[otherline], 2):
                    predicates.append(
                        Predicate("perp", [ppair[0], ppair[1], p3, p4]))

        return predicates

    def _ruleD39(self, predicate: Predicate):
        """
        eqangle(A,B,P,Q,C,D,P,Q) => para(A,B,C,D)
        """
        p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points
        l1 = self.database.matchLine([p1, p2])
        l2 = self.database.matchLine([p3, p4])
        l3 = self.database.matchLine([p5, p6])
        l4 = self.database.matchLine([p7, p8])

        if l2 == l4 and l1 != l3 and l1 != l2:
            predicate = Predicate("para", [p1, p2, p5, p6])
            return [predicate]

        return []

    def _ruleD40(self, predicate: Predicate):
        """
        para(A,B,C,D) => eqangle(A,B,P,Q,C,D,P,Q)
        """
        p1, p2, p3, p4 = predicate.points
        l1 = self.database.matchLine([p1, p2])
        l2 = self.database.matchLine([p3, p4])

        predicates = []
        for line, points in self.database.lines.items():
            if line in [l1, l2]:
                continue

            for ppair in itertools.combinations(points, 2):
                predicate = Predicate(type="eqangle",
                                      points=[
                                          p1, p2, ppair[0], ppair[1], p3, p4,
                                          ppair[0], ppair[1]
                                      ])
                predicates.append(predicate)

        return predicates

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

        return predicates

    def _ruleD45midp(self, predicate: Predicate):
        return []

    def _ruleD45para(self, predicate: Predicate):
        return []

    def _ruleD45coll(self, predicate: Predicate):
        return []

    def _ruleD46(self, predicate: Predicate):
        """
        cong(O, A, O, B) => eqangle(O,A,A,B,A,B,O,B)
        """
        p1, p2, p3, p4 = predicate.points
        valid = all([
            p1 == p3, p1 != p2, p1 != p4,
            not self.prove(Predicate("coll", [p1, p2, p4]))
        ])
        if valid:
            predicate = Predicate("eqangle", [p1, p2, p2, p4, p2, p4, p1, p4])
            return [predicate]
        return []

    def _ruleD47(self, predicate: Predicate):
        """
        eqangle(O,A,A,B,A,B,O,B) => cong(O,A,O,B)
        """
        p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points
        valid = all([
            p2 == p3, p2 == p5, p4 == p6, p4 == p8,
            not self.prove(Predicate("coll", [p1, p2, p4]))
        ])

        if valid:
            predicate = Predicate("cong", [p1, p2, p1, p4])
            return [predicate]
        return []

    def _ruleD52perp(self, predicate: Predicate):
        """
        perp(A,B,B,C) & midp(M,A,C) => cong(A,M,B,M)
        """
        p1, p2, p3, p4 = predicate.points
        valid_inputs = all([p1 != p2, p4 != p2, p2 == p3])
        if not valid_inputs:
            return []

        predicates = []
        for midfact in self.database.midpFacts:
            if sorted([p1, p4]) == midfact[1:]:
                predicate = Predicate("cong", [p1, midfact[0], p2, midfact[1]])
                predicates.append(predicate)

        return predicates

    def _ruleD52midp(self, predicate: Predicate):
        """
        midp(M,A,C) & perp(A,B,B,C) => cong(A,M,B,M)
        """
        M, A, C = predicate.points

        predicates = []
        for linepair in self.database.perpFacts:
            l1, l2 = list(linepair)
            ptsl1, ptsl2 = self.database.lines[l1], self.database.lines[l2]
            if A in ptsl1 and C in ptsl2:
                ip = ptsl1.intersection(ptsl2)
                if len(ip) == 1:
                    predicate = Predicate("cong", [A, M, list(ip)[0], M])
                    predicates.append(predicate)
            elif C in ptsl1 and A in ptsl2:
                ip = ptsl1.intersection(ptsl2)
                if len(ip) == 1:
                    predicate = Predicate("cong", [A, M, list(ip)[0], M])
                    predicates.append(predicate)

        return predicates

    def _ruleD55midp(self, predicate: Predicate):
        return []

    def _ruleD55perp(self, predicate: Predicate):
        return []

    def _ruleD56(self, predicate: Predicate):
        return []

    def _ruleD58(self, predicate: Predicate):
        return []

    def _ruleD59(self, predicate: Predicate):
        return []

    def _ruleD60(self, predicate: Predicate):
        return []

    def _ruleD61(self, predicate: Predicate):
        return []

    def _ruleD62(self, predicate: Predicate):
        return []

    def _ruleD63(self, predicate: Predicate):
        return []

    def _ruleD64(self, predicate: Predicate):
        return []
