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

from src.database import Database
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
        iters = 10
        while self.newFactsList and iters > 0:
            print(self.newFactsList, "\n\n")
            iters -= 1

            predicates = []
            d: Predicate = self.newFactsList.pop(0)
            self.database.add(d)

            if d.type == "coll":
                predicates += self._ruleD01(d)
                predicates += self._ruleD02(d)
                predicates += self._ruleD03(d)
                predicates += self._ruleD67coll(d)
            if d.type == "midp":
                predicates += self._ruleD11(d)
                predicates += self._ruleD44(d)
                predicates += self._ruleD52midp(d)
                predicates += self._ruleD63(d)
                predicates += self._ruleD68(d)
                predicates += self._ruleD70(d)
            if d.type == "para":
                predicates += self._ruleD05(d)
                predicates += self._ruleD06(d)
                predicates += self._ruleD40(d)
                predicates += self._ruleD10para(d)
                predicates += self._ruleD45para(d)
                predicates += self._ruleD64(d)
                predicates += self._ruleD65(d)
                predicates += self._ruleD66(d)
            if d.type == "eqangle":
                predicates += self._ruleD18(d)
                predicates += self._ruleD19(d)
                predicates += self._ruleD20(d)
                predicates += self._ruleD21(d)
                predicates += self._ruleD22(d)
                predicates += self._ruleD39(d)
                predicates += self._ruleD47(d)
                predicates += self._ruleD58(d)
                predicates += self._ruleD71(d)
                predicates += self._ruleD72(d)
                predicates += self._ruleD73(d)
                predicates += self._ruleD74(d)
                predicates += self._ruleD42a(d)
            if d.type == "cong":
                predicates += self._ruleD23(d)
                predicates += self._ruleD24(d)
                predicates += self._ruleD25(d)
                predicates += self._ruleD12(d)
                predicates += self._ruleD46(d)
                predicates += self._ruleD56(d)
                predicates += self._ruleD67cong(d)
                predicates += self._ruleD75cong(d)
            if d.type == "cyclic":
                predicates += self._ruleD15(d)
                predicates += self._ruleD16(d)
                predicates += self._ruleD17(d)
                predicates += self._ruleD41(d)
            if d.type == "perp":
                predicates += self._ruleD08(d)
                predicates += self._ruleD09(d)
                predicates += self._ruleD10perp(d)
                predicates += self._ruleD52perp(d)
                predicates += self._ruleD55perp(d)
            if d.type == "simtri":
                predicates += self._ruleD31(d)
                predicates += self._ruleD32(d)
                predicates += self._ruleD33(d)
                predicates += self._ruleD34(d)
                predicates += self._ruleD59(d)
                predicates += self._ruleD60(d)
                predicates += self._ruleD61simtri(d)
            if d.type == "contri":
                predicates += self._ruleD35(d)
                predicates += self._ruleD36(d)
                predicates += self._ruleD37(d)
                predicates += self._ruleD38(d)
                predicates += self._ruleD62(d)
            if d.type == "eqratio":
                predicates += self._ruleD26(d)
                predicates += self._ruleD27(d)
                predicates += self._ruleD28(d)
                predicates += self._ruleD29(d)
                predicates += self._ruleD30(d)
                predicates += self._ruleD75eqratio(d)

            # print(d)
            # print(len(self.newFactsList))
            # print("\n\n")
            """
            We get new predicates, these are deducted from the rules
            """

            for predicate in predicates:
                all_forms_predicates = self._predicate_all_forms(predicate)
                for ppredicate in all_forms_predicates:
                    if ppredicate in self.newFactsList or self.prove(
                            ppredicate):
                        continue
                    self.newFactsList.append(ppredicate)

        return self.database

    def _predicate_all_forms(self, predicate: Predicate):
        if predicate.type == "eqangle":
            # eqangle(A,B,C,D,P,Q,U,V)
            A, B, C, D, P, Q, U, V = predicate.points
            lAB = self.database.matchLine([A, B])
            lCD = self.database.matchLine([C, D])
            lPQ = self.database.matchLine([P, Q])
            lUV = self.database.matchLine([U, V])

            ptsAB = self.database.lines[lAB]
            ptsCD = self.database.lines[lCD]
            ptsPQ = self.database.lines[lPQ]
            ptsUV = self.database.lines[lUV]
            predicates = []
            for [A, B] in itertools.combinations(ptsAB, 2):
                for [C, D] in itertools.combinations(ptsCD, 2):
                    for [P, Q] in itertools.combinations(ptsPQ, 2):
                        for [U, V] in itertools.combinations(ptsUV, 2):
                            predicates.append(
                                Predicate("eqangle", [A, B, C, D, P, Q, U, V]))
            return predicates

        return [predicate]

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

        if predicate.type == "circle":
            center, points = predicate.points[0], predicate.points[1:]
            for circle in self.database.circles:
                if center == circle.center and all(
                    [p in circle.points for p in points]):
                    return True

            return False

        if predicate.type == "cyclic":
            for circle in self.database.circles:
                if all([p in circle.points for p in predicate.points]):
                    return True
            return False

        raise ValueError("Invalid type of predicate ", predicate.type)

    def _ruleD01(self, predicate: Predicate):
        """
        coll(A,B,C) => coll(A,C,B)
        """
        A, B, C = predicate.points
        return [Predicate("coll", [A, C, B])]

    def _ruleD02(self, predicate: Predicate):
        """
        coll(A,B,C) => coll(B,A,C)
        """
        A, B, C = predicate.points
        return [Predicate("coll", [B, A, C])]

    def _ruleD03(self, predicate: Predicate):
        """
        coll(A,B,C) & coll(A,B,D) => coll(C,D,A)
        """
        A, B, C = predicate.points
        lAB = self.database.matchLine([A, B])
        predicates = []
        for D in self.database.lines[lAB]:
            if D not in [A, B, C]:
                predicates.append(Predicate("coll", [C, D, A]))
        return predicates

    def _ruleD04(self, predicate: Predicate):
        """
        para(A,B,C,D) => para(A,B,D,C)
        """
        A, B, C, D = predicate.points
        return [Predicate("para", [A, B, D, C])]

    def _ruleD05(self, predicate: Predicate):
        """
        para(A,B,C,D) => para(C,D,A,B)
        """
        A, B, C, D = predicate.points
        return [Predicate("para", [C, D, A, B])]

    def _ruleD06(self, predicate: Predicate):
        """
        para(A,B,C,D) & para(C,D,E,F) => para(A,B,E,F)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])

        predicates = []
        for paraLines in self.database.paraFacts:
            if lCD not in paraLines:
                continue

            for lEF in paraLines:
                if lEF in [lAB, lCD]:
                    continue
                for (E, F) in itertools.combinations(self.database.lines[lEF],
                                                     2):
                    predicates.append(Predicate("para", [A, B, E, F]))
        return predicates

    def _ruleD07(self, predicate: Predicate):
        """
        perp(A,B,C,D) => perp(A,B,D,C)
        """
        A, B, C, D = predicate.points
        return [Predicate("perp", [A, B, D, C])]

    def _ruleD08(self, predicate: Predicate):
        """
        perp(A,B,C,D) => perp(C,D,A,B)
        """
        A, B, C, D = predicate.points
        return [Predicate("perp", [C, D, A, B])]

    def _ruleD09(self, predicate: Predicate):
        """
        perp(A,B,C,D) & perp(C,D,E,F) => para(A,B,E,F)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])

        predicates = []
        # find perp(lCD, ..) in perpfacts
        for lines in self.database.perpFacts:
            if lCD not in lines:
                continue
            lEF = list(lines)[0] if list(lines)[1] == lCD else list(lines)[1]
            if lEF == lAB or lEF == lCD:
                continue

            for ppair in itertools.combinations(self.database.lines[lEF], 2):
                E, F = ppair
                predicate = Predicate("para", [A, B, E, F])
                predicates.append(predicate)

        return predicates

    def _ruleD10para(self, predicate: Predicate):
        """
        para(A,B,C,D) & perp(C,D,E,F) => perp(A,B,E,F)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])

        predicates = []
        # find perp(lCD, ..) in perpfacts
        for lines in self.database.perpFacts:
            if lCD not in lines:
                continue
            lEF = list(lines)[0] if list(lines)[1] == lCD else list(lines)[1]
            if lEF == lAB or lEF == lCD:
                continue

            for ppair in itertools.combinations(self.database.lines[lEF], 2):
                E, F = ppair
                predicate = Predicate("perp", [A, B, E, F])
                predicates.append(predicate)

        return predicates

    def _ruleD10perp(self, predicate: Predicate):
        """
        perp(C,D,E,F) & para(A,B,C,D) => perp(A,B,E,F)
        """
        C, D, E, F = predicate.points
        lCD = self.database.matchLine([C, D])
        lEF = self.database.matchLine([E, F])

        predicates = []
        # find para(lAB, lCD) in perpfacts
        for lines in self.database.paraFacts:
            if lCD not in lines:
                continue
            lAB = list(lines)[0] if list(lines)[1] == lCD else list(lines)[1]
            if lAB == lCD or lAB == lEF:
                continue

            for ppair in itertools.combinations(self.database.lines[lAB], 2):
                A, B = ppair
                predicate = Predicate("perp", [A, B, E, F])
                predicates.append(predicate)

        return predicates

    def _ruleD11(self, predicate: Predicate):
        """
        midp(M,A,B) => midp(M,B,A)
        """
        M, A, B = predicate.points
        return [Predicate("midp", [M, B, A])]

    def _ruleD12(self, predicate: Predicate):
        """
        cong(O,A,O,B) & cong(O,A,O,C) => circle(O,A,B,C)
        """
        O1, A, O2, B = predicate.points
        predicates = []
        if O1 != O2 or A == B:
            return predicates

        cOA = self.database.matchCong([O1, A])
        for segment in self.database.congs[cOA]:
            if O1 not in [segment.p1, segment.p2]:
                continue

            C = segment.p1 if segment.p2 == O1 else segment.p2
            if C == B or C == A:
                continue
            predicates.append(Predicate("circle", [O1, A, B, C]))

        return predicates

    # missing rule d13

    def _ruleD14(self, predicate: Predicate):
        """
        cyclic(A,B,C,D) => cyclic(A,B,D,C)
        """
        A, B, C, D = predicate.points
        return [Predicate("cyclic", [A, B, D, C])]

    def _ruleD15(self, predicate: Predicate):
        """
        cyclic(A,B,C,D) => cyclic(A,C,B,D)
        """
        A, B, C, D = predicate.points
        return [Predicate("cyclic", [A, C, B, D])]

    def _ruleD16(self, predicate: Predicate):
        """
        cyclic(A,B,C,D) => cyclic(B,A,C,D)
        """
        A, B, C, D = predicate.points
        return [Predicate("cyclic", [B, A, C, D])]

    def _ruleD17(self, predicate: Predicate):
        """
        cyclic(A,B,C,D) & cyclic(A,B,C,E) => cyclic(B,C,D,E)
        """
        A, B, C, D = predicate.points
        predicates = []
        for circle in self.database.circles:
            incount = sum(p in circle.points for p in predicate.points)
            if incount < 3:
                continue
            for E in circle.points:
                if E in [A, B, C, D]:
                    continue
                predicates.append(Predicate("cyclic", [B, C, D, E]))
        return predicates

    def _ruleD18(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) => eqangle(B,A,C,D,P,Q,U,V)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        return [Predicate("eqangle", [B, A, C, D, P, Q, U, V])]

    def _ruleD19(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) => eqangle(C,D,A,B,U,V,P,Q)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        return [Predicate("eqangle", [C, D, A, B, U, V, P, Q])]

    def _ruleD20(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) => eqangle(P,Q,U,V,A,B,C,D)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        return [Predicate("eqangle", [P, Q, U, V, A, B, C, D])]

    def _ruleD21(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) => eqangle(A,B,P,Q,C,D,U,V)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        if sorted([A, B]) != sorted([P, Q]) and sorted([C, D]) != sorted(
            [U, V]):
            return [Predicate("eqangle", [A, B, P, Q, C, D, U, V])]
        return []

    def _ruleD22(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) & eqangle(P,Q,U,V,E,F,G,H)
        => eqangle(A,B,C,D,E,F,G,H)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])
        lPQ = self.database.matchLine([P, Q])
        lUV = self.database.matchLine([U, V])

        a1 = Angle(lAB, lCD)
        a2 = Angle(lPQ, lUV)

        predicates = []
        for angles in self.database.eqangleFacts:
            if a2 not in angles:
                continue
            for angle in angles:
                if angle in [a1, a2]:
                    continue
                lEF, lGH = angle.lk1, angle.lk2
                for (E, F) in itertools.combinations(self.database.lines[lEF],
                                                     2):
                    for (G,
                         H) in itertools.combinations(self.database.lines[lGH],
                                                      2):
                        predicates.append(
                            Predicate("eqangle", [P, Q, U, V, E, F, G, H]))

        return predicates

    def _ruleD23(self, predicate: Predicate):
        """
        cong(A,B,C,D) => cong(A,B,D,C)
        """
        A, B, C, D = predicate.points
        return [Predicate("cong", [A, B, D, C])]

    def _ruleD24(self, predicate: Predicate):
        """
        cong(A,B,C,D) => cong(C,D,A,B)
        """
        A, B, C, D = predicate.points
        return [Predicate("cong", [C, D, A, B])]

    def _ruleD25(self, predicate: Predicate):
        """
        cong(A,B,C,D) & cong(C,D,E,F) => cong(A,B,E,F)
        """
        A, B, C, D = predicate.points
        cAB = self.database.matchCong([A, B])
        cCD = self.database.matchCong([C, D])
        predicates = []
        for segment in self.database.congs[cCD]:
            if segment in [cAB, cCD]:
                continue

            E, F = segment.p1, segment.p2
            predicates.append(Predicate("cong", [A, B, E, F]))
        return predicates

    def _ruleD26(self, predicate: Predicate):
        """
        eqratio(A,B,C,D,P,Q,U,V) => eqratio(B,A,C,D,P,Q,U,V)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        return [Predicate("eqratio", [B, A, C, D, P, Q, U, V])]

    def _ruleD27(self, predicate: Predicate):
        """
        eqratio(A,B,C,D,P,Q,U,V) => eqratio(C,D,A,B,U,V,P,Q)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        return [Predicate("eqratio", [C, D, A, B, U, V, P, Q])]

    def _ruleD28(self, predicate: Predicate):
        """
        eqratio(A,B,C,D,P,Q,U,V) => eqratio(P,Q,U,V,A,B,C,D)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        return [Predicate("eqratio", [P, Q, U, V, A, B, C, D])]

    def _ruleD29(self, predicate: Predicate):
        """
        eqratio(A,B,C,D,P,Q,U,V) => eqratio(A,B,P,Q,C,D,U,V)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        return [Predicate("eqratio", [A, B, P, Q, C, D, U, V])]

    def _ruleD30(self, predicate: Predicate):
        """
        eqratio(A,B,C,D,P,Q,U,V) & eqratio(P,Q,U,V,E,F,G,H) => eqratio(A,B,C,D,E,F,G,H)
        """
        A, B, C, D, P, Q, U, V = predicate.points

        cAB = self.database.matchCong([A, B])
        cCD = self.database.matchCong([C, D])
        cPQ = self.database.matchCong([P, Q])
        cUV = self.database.matchCong([U, V])

        predicates = []
        for ratios in self.database.eqratioFacts:
            if Ratio(cPQ, cUV) not in ratios:
                continue

            for ratio in ratios:
                if ratio == Ratio(cPQ, cUV) or ratio == Ratio(cAB, cCD):
                    continue

                for sEF in self.database.congs[ratio.c1]:
                    for sGH in self.database.congs[ratio.c2]:
                        E, F = sEF.p1, sEF.p2
                        G, H = sGH.p1, sGH.p2
                        predicates.append(
                            Predicate("eqratio", [A, B, C, D, E, F, G, H]))

        return predicates

    def _ruleD31(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => simtri(A,C,B,P,R,Q)
        """
        A, B, C, P, Q, R = predicate.points
        return [Predicate("simtri", [A, C, B, P, R, Q])]

    def _ruleD32(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => simtri(B,A,C,Q,P,R)
        """
        A, B, C, P, Q, R = predicate.points
        return [Predicate("simtri", [B, A, C, Q, P, R])]

    def _ruleD33(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => simtri(P,Q,R,A,B,C)
        """
        A, B, C, P, Q, R = predicate.points
        return [Predicate("simtri", [P, Q, R, A, B, C])]

    def _ruleD34(self, predicate: Predicate):
        """
        simtri(A,B,C,E,F,G) & simtri(E,F,G,P,Q,R) => simtri(A,B,C,P,Q,R)
        """
        A, B, C, E, F, G = predicate.points
        tABC, tEFG = Triangle(A, B, C), Triangle(E, F, G)
        predicates = []
        for triangles in self.database.simtriFacts:
            if tEFG not in triangles:
                continue
            for tPQR in triangles:
                if tPQR in [tABC, tEFG]:
                    continue
                P, Q, R = tPQR.p1, tPQR.p2, tPQR.p3
                predicates.append(Predicate("simtri", [A, B, C, P, Q, R]))
        return predicates

    def _ruleD35(self, predicate: Predicate):
        """
        contri(A,B,C,P,Q,R) => contri(A,C,B,P,R,Q)
        """
        A, B, C, P, Q, R = predicate.points
        return [Predicate("contri", [A, C, B, P, R, Q])]

    def _ruleD36(self, predicate: Predicate):
        """
        contri(A,B,C,P,Q,R) => contri(B,A,C,Q,P,R)
        """
        A, B, C, P, Q, R = predicate.points
        return [Predicate("contri", [B, A, C, Q, P, R])]

    def _ruleD37(self, predicate: Predicate):
        """
        contri(A,B,C,P,Q,R) => contri(P,Q,R,A,B,C)
        """
        A, B, C, P, Q, R = predicate.points
        return [Predicate("contri", [P, Q, R, A, B, C])]

    def _ruleD38(self, predicate: Predicate):
        """
        contri(A,B,C,E,F,G) & contri(E,F,G,P,Q,R) => contri(A,B,C,P,Q,R)
        """
        A, B, C, E, F, G = predicate.points
        tABC, tEFG = Triangle(A, B, C), Triangle(E, F, G)
        predicates = []
        for triangles in self.database.contriFacts:
            if tEFG not in triangles:
                continue
            for tPQR in triangles:
                if tPQR in [tABC, tEFG]:
                    continue
                P, Q, R = tPQR.p1, tPQR.p2, tPQR.p3
                predicates.append(Predicate("contri", [A, B, C, P, Q, R]))
        return predicates

    def _ruleD39(self, predicate: Predicate):
        """
        eqangle(A,B,P,Q,C,D,P,Q) => para(A,B,C,D)
        """
        A, B, P1, Q1, C, D, P2, Q2 = predicate.points
        if P1 != P2 or Q1 != Q2:
            return []

        lAB = self.database.matchLine([A, B])
        lPQ = self.database.matchLine([P1, Q1])
        lCD = self.database.matchLine([C, D])

        if lAB == lCD or lAB == lPQ or lCD == lPQ:
            return []

        return [Predicate("para", [A, B, C, D])]

    def _ruleD40(self, predicate: Predicate):
        """
        para(A,B,C,D) => eqangle(A,B,P,Q,C,D,P,Q)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])

        predicates = []
        if lAB == lCD:
            return predicates

        for line, points in self.database.lines.items():
            if line in [lAB, lCD]:
                continue

            for [P, Q] in itertools.combinations(points, 2):
                predicates += [
                    Predicate(type="eqangle", points=[A, B, P, Q, C, D, P, Q]),
                ]

        return predicates

    def _ruleD41(self, predicate: Predicate):
        """
        cyclic(A,B,P,Q) => eqangle(P,A,P,B,Q,A,Q,B)
        """
        A, B, P, Q = predicate.points
        return [Predicate("eqangle", [P, A, P, B, Q, A, Q, B])]

    def _ruleD42a(self, predicate: Predicate):
        """
        eqangle(P,A,P,B,Q,A,Q,B) & not coll(P,Q,A) => cyclic(A,B,P,Q)
        """
        P1, A1, P2, B1, Q1, A2, Q2, B2 = predicate.points
        if P1 != P2 or A1 != A2 or B1 != B2 or Q1 != Q2:
            return []

        if self.prove(Predicate("coll", [P1, Q1, A1])):
            return []

        return [Predicate("cyclic", [A1, B1, P1, Q1])]

    def _ruleD44(self, predicate: Predicate):
        """
        midp(E,A,B) & midp(F,A,C) => para(E,F,B,C)        
        """
        E, A1, B = predicate.points
        predicates = []
        for midfact in self.database.midpFacts:
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
        O1, A, O2, B = predicate.points

        if O1 != O2 or A == B or O1 == A or self.prove(
                Predicate("coll", [O1, A, B])):
            return []

        return [Predicate("eqangle", [O1, A, A, B, A, B, O1, B])]

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
        A, B1, B2, C = predicate.points
        predicates = []
        if B1 != B2 or A == C or A == B1:
            return predicates

        for midfact in self.database.midpFacts:
            if sorted([A, C]) == midfact[1:]:
                M = midfact[0]
                predicates.append(Predicate("cong", [A, M, B1, M]))

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
        A, P1, B, P2 = predicate.points
        predicates = []
        if A == B or P1 != P2:
            return predicates

        for _, segments in self.database.congs.items():
            containsA = [s for s in segments if A in [s.p1, s.p2]]
            containsB = [s for s in segments if B in [s.p1, s.p2]]

            if containsA and containsB:
                qA = [p for s in containsA for p in [s.p1, s.p2] if p != A]
                qB = [p for s in containsB for p in [s.p1, s.p2] if p != B]
                qs = [p for p in qA if p in qB and p != P1]
                for Q in qs:
                    predicate = Predicate("perp", [A, B, P1, Q])
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
                                Predicate("eqangle", [
                                    A, C, B, C, P, R, Q, R
                                ])) and Triangle(A, B, C) != Triangle(P, Q, R):
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
        ]

    def _ruleD60(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => eqangle(A,B,A,C,P,Q,P,R)
        """
        A, B, C, P, Q, R = predicate.points
        return [
            Predicate("eqangle", [A, B, B, C, P, Q, Q, R]),
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
        return [
            Predicate("cong", [A, B, P, Q]),
            Predicate("cong", [A, C, P, R]),
            Predicate("cong", [B, C, Q, R])
        ]

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

    def _ruleD67coll(self, predicate: Predicate):
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

    def _ruleD67cong(self, predicate: Predicate):
        """
        cong(A,B,A,C) & coll(A,B,C) => midp(A,B,C)
        """
        A1, B, A2, C = predicate.points
        predicates = []
        if A1 != A2 or B == C:
            return predicates

        for points in self.database.lines.values():
            if all([A1 in points, B in points, C in points]):
                predicates.append(Predicate("midp", [A1, B, C]))

        return predicates

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

    def _ruleD75cong(self, predicate: Predicate):
        """
        cong(P,Q,U,V) & eqratio(A,B,C,D,P,Q,U,V) => cong(A,B,C,D)
        """
        P, Q, U, V = predicate.points
        cPQ = self.database.matchCong([P, Q])
        cUV = self.database.matchCong([U, V])

        predicates = []
        for ratios in self.database.eqratioFacts:
            for ratioPair in itertools.combinations(ratios, 2):
                ratioA, ratioB = ratioPair
                a1, a2 = ratioA.c1, ratioA.c2
                b1, b2 = ratioB.c1, ratioB.c2
                # a1/a2 = b1/b2
                if a1 in [cPQ, cUV] and b1 in [cPQ, cUV]:
                    # a2 = b2
                    segsA2 = self.database.congs[a2]
                    segsB2 = self.database.congs[b2]
                    for s1 in segsA2:
                        for s2 in segsB2:
                            A, B, C, D = s1.p1, s1.p2, s2.p1, s2.p2
                            predicates.append(Predicate("cong", [A, B, C, D]))

                if a2 in [cPQ, cUV] and b2 in [cPQ, cUV]:
                    # a1 = b1
                    segsA1 = self.database.congs[a1]
                    segsB1 = self.database.congs[b1]
                    for s1 in segsA1:
                        for s2 in segsB1:
                            A, B, C, D = s1.p1, s1.p2, s2.p1, s2.p2
                            predicates.append(Predicate("cong", [A, B, C, D]))

                if a1 in [cPQ, cUV] and a2 in [cPQ, cUV]:
                    # b1 = b2
                    segsB1 = self.database.congs[b1]
                    segsB2 = self.database.congs[b2]
                    for s1 in segsB1:
                        for s2 in segsB2:
                            A, B, C, D = s1.p1, s1.p2, s2.p1, s2.p2
                            predicates.append(Predicate("cong", [A, B, C, D]))

                if b1 in [cPQ, cUV] and b2 in [cPQ, cUV]:
                    # a1 = a2
                    segsA1 = self.database.congs[a1]
                    segsA2 = self.database.congs[a2]
                    for s1 in segsA1:
                        for s2 in segsA2:
                            A, B, C, D = s1.p1, s1.p2, s2.p1, s2.p2
                            predicates.append(Predicate("cong", [A, B, C, D]))

        return predicates

    def _ruleD75eqratio(self, predicate: Predicate):
        """
        eqratio(A,B,C,D,P,Q,U,V) & cong(P,Q,U,V) => cong(A,B,C,D)

        This is not geometry properties but numerically correct
        """
        A, B, C, D, P, Q, U, V = predicate.points
        cAB = self.database.matchCong([A, B])
        cCD = self.database.matchCong([C, D])
        cPQ = self.database.matchCong([P, Q])
        cUV = self.database.matchCong([U, V])

        if cAB == cPQ:
            return [Predicate("cong", [C, D, U, V])]
        if cAB == cCD:
            return [Predicate("cong", [P, Q, U, V])]
        if cCD == cUV:
            return [Predicate("cong", [A, B, P, Q])]
        if cPQ == cUV:
            return [Predicate("cong", [A, B, C, D])]
        return []

    # @staticmethod
    # def _predicates_permutations(predicate: Predicate) -> list[Predicate]:
    #     """
    #     Why need this?
    #     A predicate goes into one rule and outputs a concluded predicate.

    #     If the concluded predicate is used before, no need to go further.
    #     Otherwise we need the concluded predicate to trigger new predicates
    #     in the next round and forward.

    #     However, the concluded predicate have equivalent forms under
    #     premutation. We need to generate these as well.
    #     """
    #     if predicate.type == "cong":
    #         # cong(A,B,C,D)
    #         A, B, C, D = predicate.points
    #         return [
    #             Predicate("cong", [A, B, C, D]),
    #             Predicate("cong", [A, B, D, C]),
    #             Predicate("cong", [B, A, C, D]),
    #             Predicate("cong", [B, A, D, C]),
    #             Predicate("cong", [C, D, A, B]),
    #             Predicate("cong", [D, C, A, B]),
    #             Predicate("cong", [C, D, B, A]),
    #             Predicate("cong", [D, C, B, A]),
    #         ]
    #     if predicate.type == "para":
    #         # para(A,B,C,D)
    #         A, B, C, D = predicate.points
    #         return [
    #             Predicate("para", [A, B, C, D]),
    #             Predicate("para", [A, B, D, C]),
    #             Predicate("para", [B, A, C, D]),
    #             Predicate("para", [B, A, D, C]),
    #             Predicate("para", [C, D, A, B]),
    #             Predicate("para", [D, C, A, B]),
    #             Predicate("para", [C, D, B, A]),
    #             Predicate("para", [D, C, B, A]),
    #         ]
    #     if predicate.type == "perp":
    #         # perp(A,B,C,D)
    #         A, B, C, D = predicate.points
    #         return [
    #             Predicate("perp", [A, B, C, D]),
    #             Predicate("perp", [A, B, D, C]),
    #             Predicate("perp", [B, A, C, D]),
    #             Predicate("perp", [B, A, D, C]),
    #             Predicate("perp", [C, D, A, B]),
    #             Predicate("perp", [D, C, A, B]),
    #             Predicate("perp", [C, D, B, A]),
    #             Predicate("perp", [D, C, B, A]),
    #         ]
    #     if predicate.type == "eqratio":
    #         # eqratio(A,B,C,D,P,Q,U,V)
    #         A, B, C, D, P, Q, U, V = predicate.points
    #         return [
    #             Predicate("eqratio", [A, B, C, D, P, Q, U, V]),
    #             Predicate("eqratio", [B, A, C, D, P, Q, U, V]),
    #             Predicate("eqratio", [A, B, D, C, Q, P, U, V]),
    #             Predicate("eqratio", [A, B, C, D, P, Q, V, U]),
    #             Predicate("eqratio", [B, A, C, D, P, Q, U, V]),
    #             Predicate("eqratio", [A, B, D, C, P, Q, U, V]),
    #             Predicate("eqratio", [A, B, C, D, P, Q, U, V]),
    #             Predicate("eqratio", [B, A, C, D, P, Q, U, V]),
    #             Predicate("eqratio", [A, B, D, C, P, Q, U, V])
    #         ]
    #     if predicate.type == "eqangle":
    #         return [predicate]

    #     return [predicate]


def test():
    from src.util import parse_predicates_from_file
    hypotheses = parse_predicates_from_file("problems/p3")
    prover = Prover(hypotheses=hypotheses)
    prover.fixedpoint()
    print(prover.database)
    quests = [
        Predicate("coll", ["A", "B", "D"]),
        Predicate("coll", ["A", "C", "E"]),
        Predicate("para", ["D", "E", "B", "C"]),
        Predicate("cong", ["A", "D", "D", "B"]),
        Predicate("eqangle", ["A", "D", "D", "E", "A", "D", "B", "C"]),
        Predicate("eqangle", ["A", "B", "D", "E", "A", "D", "B", "C"]),
        Predicate("eqangle", ["A", "B", "D", "E", "A", "B", "B", "C"]),
        Predicate("eqangle", ["D", "E", "A", "B", "C", "B", "A", "B"]),
        Predicate("eqangle", ["A", "E", "D", "E", "A", "C", "B", "C"]),
        Predicate("eqangle", ["A", "D", "D", "E", "A", "B", "B", "C"]),
        Predicate("simtri", ["A", "D", "E", "A", "B", "C"]),
    ]
    for quest in quests:
        assert prover.prove(quest), f"{quest} not proved"


test()