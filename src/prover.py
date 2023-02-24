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
            if d.type == "coll":
                predicates += self._ruleD67(d)
            if d.type == "midp":
                predicates += self._ruleD44(d)
                predicates += self._ruleD52midp(d)
                predicates += self._ruleD63(d)
                predicates += self._ruleD68(d)
                predicates += self._ruleD70(d)
            if d.type == "para":
                predicates += self._ruleD40(d)
                predicates += self._ruleD10para(d)
                predicates += self._ruleD45para(d)
                predicates += self._ruleD64(d)
                predicates += self._ruleD65(d)
                predicates += self._ruleD66(d)
            if d.type == "eqangle":
                predicates += self._ruleD39(d)
                predicates += self._ruleD47(d)
                predicates += self._ruleD58(d)
                predicates += self._ruleD71(d)
                predicates += self._ruleD72(d)
                predicates += self._ruleD73(d)
                predicates += self._ruleD74(d)
            if d.type == "cong":
                predicates += self._ruleD46(d)
                predicates += self._ruleD56(d)
            if d.type == "perp":
                predicates += self._ruleD09(d)
                predicates += self._ruleD10perp(d)
                predicates += self._ruleD52perp(d)
                predicates += self._ruleD55perp(d)
            if d.type == "simtri":
                predicates += self._ruleD59(d)
                predicates += self._ruleD60(d)
                predicates += self._ruleD61simtri(d)
            if d.type == "contri":
                predicates += self._ruleD62(d)

            for predicate in predicates:
                if self.prove(predicate) or predicate in self.newFactsList:
                    continue
                self.newFactsList.append(predicate)

            # print(self.newFactsList)

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
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])

        predicates = []
        for line, points in self.database.lines.items():
            if line in [lAB, lCD]:
                continue

            for [P, Q] in itertools.combinations(points, 2):
                predicates += [
                    Predicate(type="eqangle", points=[A, B, P, Q, C, D, P, Q]),
                    Predicate(type="eqangle", points=[P, Q, A, B, P, Q, C, D])
                ]

        return predicates

    def _ruleD44(self, predicate: Predicate):
        """
        midp(E,A,B) & midp(F,A,C) => para(E,F,B,C)        
        """
        E, A1, B = predicate.points
        predicates = []
        for midfact in self.database.midpFacts:
            # p1, p2, p3 = midfact

            # # [p1, p2, p3]
            # # p1 != E, p2 = A, p3 != B
            # if p1 != E and p2 == A and p3 != B and not self.prove(
            #         Predicate("coll", [A, B, p3])):
            #     predicate = Predicate(type="para", points=[E, p1, B, p3])
            #     predicates.append(predicate)
            # # [p1, p3, p2]
            # # p1 != E, p3 = A, p2 != B
            # elif p1 != E and p3 == A and p2 != B and not self.prove(
            #         Predicate("coll", [A, B, p2])):
            #     predicate = Predicate(type="para", points=[E, p3, B, p2])
            #     predicates.append(predicate)
            F, A2, C = midfact
            if E == F:
                continue

            As = [p for p in [A1, B] if p in [A2, C]]
            if len(As) != 1:
                continue

            A = As[0]
            B = B if A == A1 else A1
            C = C if A == A2 else A2
            if self.prove(Predicate("coll", [A, B, C])):
                continue

            predicates.append(Predicate("para", [E, F, B, C]))

        return predicates

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

            return [
                Predicate("eqangle", [p1, p2, p2, p4, p2, p4, p1, p4]),
                Predicate("eqangle", [p2, p4, p1, p2, p1, p4, p2, p4])
            ]
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

    def _ruleD55perp(self, predicate: Predicate):
        """
        perp(O,M,A,B) & midp(M,A,B) => cong(O,A,O,B)
        """
        O, M, A, B = predicate.points
        predicates = []
        for midpfact in self.database.midpFacts:
            A_, B_ = sorted([A, B])
            if [M, A_, B_] == midpfact:
                predicate = Predicate("cong", [O, A, O, B])
                predicates.append(predicate)

        return predicates

    def _ruleD56(self, predicate: Predicate):
        """
        cong(A,P,B,P) & cong(A,Q,B,Q) => perp(A,B,P,Q)
        """
        A, P, B, P = predicate.points
        predicates = []
        if A == B:
            return predicates

        for _, segments in self.database.congs.items():
            containsA = [s for s in segments if A in [s.p1, s.p2]]
            containsB = [s for s in segments if B in [s.p1, s.p2]]

            if containsA and containsB:
                qA = [p for s in containsA for p in [s.p1, s.p2] if p != A]
                qB = [p for s in containsB for p in [s.p1, s.p2] if p != B]
                qs = [p for p in qA if p in qB and p != P]
                for Q in qs:
                    predicate = Predicate("perp", [A, B, P, Q])
                    predicates.append(predicate)

        return predicates

    def _ruleD58(self, predicate: Predicate):
        """
        eqangle(A,B,B,C,P,Q,Q,R) & eqangle(A,C,B,C,P,R,Q,R) & ~ coll(A,B,C)
        => simtri(A,B,C,P,Q,R)
        """
        # # A and C can be replaced by other points on the line
        # A, B1, B2, C, P, Q1, Q2, R = predicate.points

        # Input eqangle predicates only specifies the lines that construct
        # the angle, but not the specific point
        # i.e., \angle <l1, l2> = \angle <l3, l4>
        # but the exact \angle ABC = \angle CDE is unknown

        predicates = []
        p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points
        lAB = self.database.matchLine([p1, p2])
        lBC = self.database.matchLine([p3, p4])
        lPQ = self.database.matchLine([p5, p6])
        lQR = self.database.matchLine([p7, p8])

        ptsAB = self.database.lines[lAB]
        ptsBC = self.database.lines[lBC]
        ptsPQ = self.database.lines[lPQ]
        ptsQR = self.database.lines[lQR]

        # lAB and lBC intersects, at B
        Bs = ptsAB.intersection(ptsBC)
        Qs = ptsPQ.intersection(ptsQR)

        if len(Bs) != 1 or len(Qs) != 1:
            return []

        # print("Reaching here: rule 58 on", ptsAB, ptsBC, ptsPQ, ptsQR)

        B = list(Bs)[0]
        Q = list(Qs)[0]

        As = [p for p in ptsAB if p != B]
        Cs = [p for p in ptsBC if p != B]
        Ps = [p for p in ptsPQ if p != Q]
        Rs = [p for p in ptsQR if p != Q]

        predicates = []
        for A in As:
            for C in Cs:
                for P in Ps:
                    for R in Rs:
                        if self.prove(
                                Predicate("eqangle",
                                          [A, C, B, C, P, R, Q, R])):
                            predicate = Predicate("simtri", [A, B, C, P, Q, R])
                            predicates.append(predicate)

        return predicates

    def _ruleD59(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => eqratio(A,B,A,C,P,Q,P,R)
        """
        A, B, C, P, Q, R = predicate.points
        return [
            Predicate("eqratio", [A, B, A, C, P, Q, P, R]),
            Predicate("eqratio", [A, B, B, C, P, Q, Q, R]),
            Predicate("eqratio", [A, C, B, C, P, R, Q, R]),
            Predicate("eqratio", [A, B, P, Q, B, C, Q, R])
        ]

    def _ruleD60(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => eqangle(A,B,A,C,P,Q,P,R)
        """
        A, B, C, P, Q, R = predicate.points
        return [
            Predicate("eqangle", [A, B, B, C, P, Q, Q, R]),
            Predicate("eqangle", [B, C, A, B, Q, R, P, Q])
        ]

    def _ruleD61simtri(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) & cong(A,B,P,Q) => contri(A,B,C,P,Q,R)
        """
        A, B, C, P, Q, R = predicate.points
        sab = Segment(A, B)
        spq = Segment(P, Q)
        for _, segments in self.database.congs.items():
            if sab in segments and spq in segments:
                return [Predicate("contri", [A, B, C, P, Q, R])]
        return []

    def _ruleD62(self, predicate: Predicate):
        """
        contri(A,B,C,P,Q,R) => cong(A,B,P,Q)
        """
        A, B, C, P, Q, R = predicate.points
        return [Predicate("cong", [A, B, P, Q])]

    def _ruleD63(self, predicate: Predicate):
        """
        midp(M,A,B) & midp(M,C,D) => para(A,C,B,D)
        """
        M, A, B = predicate.points

        predicates = []
        for midp in self.database.midpFacts:
            if midp[0] != M:
                continue
            A_, B_ = sorted([A, B])
            if [M, A_, B_] != midp:
                C, D = midp[1:]
                predicate = Predicate("para", [A, C, B, D])
                predicates.append(predicate)

        return predicates

    def _ruleD64(self, predicate: Predicate):
        """
        para(A,C,B,D) & para(A,D,B,C) & midp(M,A,B) => midp(M,C,D)
        """
        A, C, B, D = predicate.points
        predicates = []
        lad = self.database.matchLine([A, D])
        lbc = self.database.matchLine([B, C])

        found = False
        for lines in self.database.paraFacts:
            if lad in lines and lbc in lines:
                found = True
                break

        if not found:
            return predicates

        for midp in self.database.midpFacts:
            A_, B_ = sorted([A, B])
            if [A_, B_] == midp[1:]:
                M = midp[0]
                return [Predicate("midp", [M, C, D])]

        return predicates

    def _ruleD65(self, predicate: Predicate):
        """
        para(A,B,C,D) & coll(O,A,C) & coll(O,B,D) => eqratio(O,A,A,C,O,B,B,D)
        """
        A, B, C, D = predicate.points
        predicates = []
        lac = self.database.matchLine([A, C])
        lbd = self.database.matchLine([B, D])

        pac = self.database.lines[lac]
        pbd = self.database.lines[lbd]

        Os = [p for p in pac if p in pbd]
        for O in Os:
            predicate = Predicate("eqratio", [O, A, A, C, O, B, B, D])
            predicates.append(predicate)
        return predicates

    def _ruleD66(self, predicate: Predicate):
        """
        para(A,B,A,C) => coll(A,B,C)
        """
        A1, B, A2, C = predicate.points
        if A1 == A2:
            return [Predicate("coll", [A1, B, C])]
        return []

    def _ruleD67(self, predicate: Predicate):
        """
        coll(A,B,C) & cong(A,B,A,C) => midp(A,B,C)
        """
        A, B, C = predicate.points
        sab = Segment(A, B)
        sac = Segment(A, C)

        for _, segments in self.database.congs.items():
            if sab in segments and sac in segments:
                return [Predicate("midp", [A, B, C])]
        return []

    def _ruleD68(self, predicate: Predicate):
        """
        midp(A,B,C) => cong(A,B,A,C)
        """
        A, B, C = predicate.points
        return [Predicate("cong", [A, B, A, C])]

    def _ruleD70(self, predicate: Predicate):
        """
        midp(M,A,B) & midp(N,C,D) => eqratio(M,A,A,B,N,C,C,D)
        """
        M, A, B = predicate.points
        predicates = []
        for midp in self.database.midpFacts:
            A_, B_ = sorted([A, B])
            if [M, A_, B_] != midp:
                N, C, D = midp
                predicate = Predicate("eqratio", [M, A, A, B, N, C, C, D])
                predicates.append(predicate)

        return predicates

    def _ruleD71(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,C,D,A,B) & ~ para(A,B,C,D) => perp(A,B,C,D)
        """
        A1, B1, C1, D1, C2, D2, A2, B2 = predicate.points
        if not all([
                A1 == A2, B1 == B2, C1 == C2, D1 == D2,
                not self.prove(Predicate("para", [A1, B1, A2, B2]))
        ]):
            return []
        return [Predicate("perp", [A1, B1, C1, D1])]

    def _ruleD71(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,C,D,A,B) & ~ para(A,B,C,D) => perp(A,B,C,D)
        """
        A1, B1, C1, D1, C2, D2, A2, B2 = predicate.points
        if not all([
                A1 == A2, B1 == B2, C1 == C2, D1 == D2,
                not self.prove(Predicate("para", [A1, B1, A2, B2]))
        ]):
            return []
        return [Predicate("perp", [A1, B1, C1, D1])]

    def _ruleD72(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,C,D,A,B) & ~ perp(A,B,C,D) => para(A,B,C,D)
        """
        A1, B1, C1, D1, C2, D2, A2, B2 = predicate.points
        if not all([
                A1 == A2, B1 == B2, C1 == C2, D1 == D2,
                not self.prove(Predicate("perp", [A1, B1, A2, B2]))
        ]):
            return []
        return [Predicate("para", [A1, B1, C1, D1])]

    def _ruleD73(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) & para(P,Q,U,V) => para(A,B,C,D)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        if self.prove(Predicate("para", [P, Q, U, V])):
            return [Predicate("para", [A, B, C, D])]
        return []

    def _ruleD74(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) & perp(P,Q,U,V) => perp(A,B,C,D)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        if self.prove(Predicate("perp", [P, Q, U, V])):
            return [Predicate("perp", [A, B, C, D])]
        return []
