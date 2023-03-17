from src.primitives import Angle, Triangle, Ratio, Segment
from src.database import Database
from src.predicate import Predicate
from src.fact import Fact
import itertools


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

            if d.type == "midp":
                predicates += self._ruleD44(d)
                predicates += self._ruleD63(d)
                predicates += self._ruleD68(d)
                predicates += self._ruleD70(d)
            if d.type == "para":
                predicates += self._ruleD40(d)
                predicates += self._ruleD10para(d)
                predicates += self._ruleD45para(d)
                predicates += self._ruleD64(d)
                predicates += self._ruleD65(d)
            if d.type == "eqangle":
                predicates += self._ruleD39(d)
                predicates += self._ruleD47(d)
                predicates += self._ruleD58(d)
                predicates += self._ruleD71(d)
                predicates += self._ruleD72(d)
                predicates += self._ruleD73(d)
                predicates += self._ruleD74(d)
                predicates += self._ruleD42a(d)
            if d.type == "cong":
                predicates += self._ruleD12(d)
                predicates += self._ruleD46(d)
                predicates += self._ruleD75cong(d)
            if d.type == "cyclic":
                predicates += self._ruleD41(d)
            if d.type == "perp":
                predicates += self._ruleD09(d)
                predicates += self._ruleD10perp(d)
                predicates += self._ruleD52perp(d)
            if d.type == "simtri":
                predicates += self._ruleD59(d)
                predicates += self._ruleD60(d)
                predicates += self._ruleD61simtri(d)
            if d.type == "contri":
                predicates += self._ruleD62(d)
            if d.type == "eqratio":
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

    def _ruleD09(self, predicate: Predicate) -> list[Fact]:
        """
        perp(A,B,C,D) & perp(C,D,E,F) => para(A,B,E,F)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])

        facts = []
        for lines in self.database.perpFacts:
            if lCD not in lines:
                continue
            lEF = list(lines)[0] if list(lines)[1] == lCD else list(lines)[1]
            if lEF == lAB or lEF == lCD:
                continue
            facts.append(Fact("para", [lAB, lEF]))

        return facts

    def _ruleD10para(self, predicate: Predicate):
        """
        para(A,B,C,D) & perp(C,D,E,F) => perp(A,B,E,F)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])

        facts = []
        # find perp(lCD, ..) in perpfacts
        for lines in self.database.perpFacts:
            if lCD not in lines:
                continue
            lEF = list(lines)[0] if list(lines)[1] == lCD else list(lines)[1]
            if lEF == lAB or lEF == lCD:
                continue
            facts.append(Fact("perp", [lAB, lEF]))

        return facts

    def _ruleD10perp(self, predicate: Predicate):
        """
        perp(C,D,E,F) & para(A,B,C,D) => perp(A,B,E,F)
        """
        C, D, E, F = predicate.points
        lCD = self.database.matchLine([C, D])
        lEF = self.database.matchLine([E, F])

        facts = []
        # find para(lAB, lCD) in perpfacts
        for lines in self.database.paraFacts:
            if lCD not in lines:
                continue
            lAB = list(lines)[0] if list(lines)[1] == lCD else list(lines)[1]
            if lAB == lCD or lAB == lEF:
                continue
            facts.append(Fact("perp", [lAB, lEF]))
        return facts

    def _ruleD12(self, predicate: Predicate):
        """
        cong(O,A,O,B) & cong(O,A,O,C) => circle(O,A,B,C)
        """
        O1, A, O2, B = predicate.points
        facts = []
        if O1 != O2 or A == B:
            return facts

        cOA = self.database.matchCong([O1, A])
        for segment in self.database.congs[cOA]:
            if O1 not in [segment.p1, segment.p2]:
                continue

            C = segment.p1 if segment.p2 == O1 else segment.p2
            if C == B or C == A:
                continue
            facts.append(Fact("circle", [O1, A, B, C]))

        return facts

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

        return [Fact("para", [lAB, lCD])]

    def _ruleD40(self, predicate: Predicate):
        """
        para(A,B,C,D) => eqangle(A,B,P,Q,C,D,P,Q)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])
        facts = []
        if lAB == lCD:
            return facts
        for lPQ in self.database.lines:
            if lPQ in [lAB, lCD]:
                continue
            facts.append(Fact("eqangle", points=[lAB, lPQ, lCD, lPQ]))
        return facts

    def _ruleD41(self, predicate: Predicate):
        """
        cyclic(A,B,P,Q) => eqangle(P,A,P,B,Q,A,Q,B)
        """
        A, B, P, Q = predicate.points
        lPA = self.database.matchLine([P, A])
        lPB = self.database.matchLine([P, B])
        lQA = self.database.matchLine([Q, A])
        lQB = self.database.matchLine([Q, B])
        return [Fact("eqangle", [lPA, lPB, lQA, lQB])]

    def _ruleD42a(self, predicate: Predicate):
        """
        eqangle(P,A,P,B,Q,A,Q,B) & not coll(P,Q,A) => cyclic(A,B,P,Q)
        """
        P1, A1, P2, B1, Q1, A2, Q2, B2 = predicate.points
        if P1 != P2 or A1 != A2 or B1 != B2 or Q1 != Q2:
            return []

        if self.prove(Predicate("coll", [P1, Q1, A1])):
            return []

        return [Fact("cyclic", [A1, B1, P1, Q1])]

    def _ruleD44(self, predicate: Predicate):
        """
        midp(E,A,B) & midp(F,A,C) => para(E,F,B,C)        
        """
        E, A1, B = predicate.points
        facts = []
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

            lEF = self.database.matchLine([E, F])
            lBC = self.database.matchLine([B, C])

            facts.append(Fact("para", [lEF, lBC]))

        return facts

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

        lOA = self.database.matchLine([O1, A])
        lAB = self.database.matchLine([A, B])
        lOB = self.database.matchLine([O1, B])
        return [Fact("eqangle", [lOA, lAB, lAB, lOB])]

    def _ruleD47(self, predicate: Predicate):
        """
        eqangle(O,A,A,B,A,B,O,B) => cong(O,A,O,B)
        """
        O1, A1, A2, B1, A3, B2, O2, B3 = predicate.points
        valid = all([
            A1 == A2, A1 == A3, B1 == B2, B1 == B3,
            not self.prove(Predicate("coll", [O1, A1, B1]))
        ])
        if not valid:
            return []
        c1 = self.database.matchCong([O1, A1])
        c2 = self.database.matchCong([O1, B1])
        return [Fact("cong", [c1, c2])]

    def _ruleD52perp(self, predicate: Predicate):
        """
        perp(A,B,B,C) & midp(M,A,C) => cong(A,M,B,M)
        """
        A, B1, B2, C = predicate.points
        facts = []
        if B1 != B2 or A == C or A == B1:
            return facts

        for midfact in self.database.midpFacts:
            if sorted([A, C]) == midfact[1:]:
                M = midfact[0]
                c1 = self.database.matchCong([A, M])
                c2 = self.database.matchCong([B1, M])
                facts.append(Predicate("cong", [c1, c2]))

        return facts

    def _ruleD58(self, predicate: Predicate):
        """
        eqangle(A,B,B,C,P,Q,Q,R) & eqangle(A,C,B,C,P,R,Q,R) & ~ coll(A,B,C)
        => simtri(A,B,C,P,Q,R)
        """
        A, B1, B2, C, P, Q1, Q2, R = predicate.points
        if B1 != B2 or Q1 != Q2 or self.prove(Predicate("coll", [A, B1, C])):
            return []

        if self.prove(Predicate("eqangle", [A, C, B1, C, P, R, Q1, R])):
            return [Fact("simtri", [Triangle(A, B1, C), Triangle(P, Q1, R)])]

        return []

    def _ruleD59(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => eqratio(A,B,A,C,P,Q,P,R)
        """
        A, B, C, P, Q, R = predicate.points
        cAB = self.database.matchCong([A, B])
        cAC = self.database.matchCong([A, C])
        cPQ = self.database.matchCong([P, Q])
        cPR = self.database.matchCong([P, R])
        return [
            Fact("eqratio", [Ratio(cAB, cAC), Ratio(cPQ, cPR)]),
        ]

    def _ruleD60(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => eqangle(A,B,A,C,P,Q,P,R)
        """
        A, B, C, P, Q, R = predicate.points
        lAB = self.database.matchLine([A, B])
        lAC = self.database.matchLine([A, C])
        lPQ = self.database.matchLine([P, Q])
        lPR = self.database.matchLine([P, R])
        return [
            Predicate("eqangle",
                      [Angle(lAB, lAC), Angle(lPQ, lPR)]),
        ]

    def _ruleD61simtri(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) & cong(A,B,P,Q) => contri(A,B,C,P,Q,R)
        """
        A, B, C, P, Q, R = predicate.points
        for _, segments in self.database.congs.items():
            if Segment(A, B) in segments and Segment(P, Q) in segments:
                return [Fact("contri", [Triangle(A, B, C), Triangle(P, Q, R)])]
        return []

    def _ruleD62(self, predicate: Predicate):
        """
        contri(A,B,C,P,Q,R) => cong(A,B,P,Q)
        """
        A, B, C, P, Q, R = predicate.points
        cAB = self.database.matchCong([A, B])
        cPQ = self.database.matchCong([P, Q])
        return [Fact("cong", [cAB, cPQ])]

    def _ruleD63(self, predicate: Predicate):
        """
        midp(M,A,B) & midp(M,C,D) => para(A,C,B,D)
        """
        M, A, B = predicate.points

        facts = []
        for midp in self.database.midpFacts:
            if midp[0] != M:
                continue
            A_, B_ = sorted([A, B])
            if [M, A_, B_] != midp:
                C, D = midp[1:]
                lAC = self.database.matchLine([A, C])
                lBD = self.database.matchLine([B, D])
                facts.append(Fact("para", [lAC, lBD]))

        return facts

    def _ruleD64(self, predicate: Predicate):
        """
        para(A,C,B,D) & para(A,D,B,C) & midp(M,A,B) => midp(M,C,D)
        """
        A, C, B, D = predicate.points
        facts = []
        lad = self.database.matchLine([A, D])
        lbc = self.database.matchLine([B, C])

        found = False
        for lines in self.database.paraFacts:
            if lad in lines and lbc in lines:
                found = True
                break

        if not found:
            return facts

        for midp in self.database.midpFacts:
            A_, B_ = sorted([A, B])
            if [A_, B_] == midp[1:]:
                M = midp[0]
                return [Fact("midp", [M, C, D])]

        return facts

    def _ruleD65(self, predicate: Predicate):
        """
        para(A,B,C,D) & coll(O,A,C) & coll(O,B,D) => eqratio(O,A,A,C,O,B,B,D)
        """
        A, B, C, D = predicate.points
        facts = []
        lac = self.database.matchLine([A, C])
        lbd = self.database.matchLine([B, D])

        pac = self.database.lines[lac]
        pbd = self.database.lines[lbd]

        Os = [p for p in pac if p in pbd]
        for O in Os:
            cOA = self.database.matchCong([O, A])
            cAC = self.database.matchCong([A, C])
            cOB = self.database.matchCong([O, B])
            cBD = self.database.matchCong([B, D])
            facts.append(Fact("eqratio", [Ratio(cOA, cAC), Ratio(cOB, cBD)]))
        return facts

    def _ruleD68(self, predicate: Predicate):
        """
        midp(A,B,C) => cong(A,B,A,C)
        """
        A, B, C = predicate.points
        cAB = self.database.matchCong([A, B])
        cAC = self.database.matchCong([A, C])
        return [Fact("cong", [cAB, cAC])]

    def _ruleD70(self, predicate: Predicate):
        """
        midp(M,A,B) & midp(N,C,D) => eqratio(M,A,A,B,N,C,C,D)
        """
        M, A, B = predicate.points
        facts = []
        for midp in self.database.midpFacts:
            A_, B_ = sorted([A, B])
            if [M, A_, B_] != midp:
                N, C, D = midp
                cMA = self.database.matchCong([M, A])
                cAB = self.database.matchCong([A, B])
                cNC = self.database.matchCong([N, C])
                cCD = self.database.matchCong([C, D])
                facts.append(
                    Fact("eqratio",
                         [Ratio(cMA, cAB), Ratio(cNC, cCD)]))

        return facts

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
        lAB = self.database.matchLine([A1, B1])
        lCD = self.database.matchLine([C1, D1])
        return [Fact("perp", [lAB, lCD])]

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
        lAB = self.database.matchLine([A1, B1])
        lCD = self.database.matchLine([C1, D1])
        return [Fact("para", [lAB, lCD])]

    def _ruleD73(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) & para(P,Q,U,V) => para(A,B,C,D)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        if self.prove(Predicate("para", [P, Q, U, V])):
            lAB = self.database.matchLine([A, B])
            lCD = self.database.matchLine([C, D])
            return [Fact("para", [lAB, lCD])]
        return []

    def _ruleD74(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) & perp(P,Q,U,V) => perp(A,B,C,D)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        if self.prove(Predicate("perp", [P, Q, U, V])):
            lAB = self.database.matchLine([A, B])
            lCD = self.database.matchLine([C, D])
            return [Fact("perp", [lAB, lCD])]
        return []

    def _ruleD75cong(self, predicate: Predicate):
        """
        cong(P,Q,U,V) & eqratio(A,B,C,D,P,Q,U,V) => cong(A,B,C,D)
        """
        P, Q, U, V = predicate.points
        cPQ = self.database.matchCong([P, Q])
        cUV = self.database.matchCong([U, V])

        facts = []
        for ratios in self.database.eqratioFacts:
            if Ratio(cPQ, cUV) not in ratios:
                continue
            for ratio in ratios:
                if ratio == Ratio(cPQ, cUV):
                    continue
                facts.append(Fact("cong", [ratio.c1, ratio.c2]))
        return facts

    def _ruleD75eqratio(self, predicate: Predicate):
        """
        eqratio(A,B,C,D,P,Q,U,V) & cong(P,Q,U,V) => cong(A,B,C,D)

        This is not geometry properties but numerically correct
        """
        A, B, C, D, P, Q, U, V = predicate.points
        cAB = self.database.matchCong([A, B])
        cCD = self.database.matchCong([C, D])
        facts = []
        for segments in self.database.congs.values():
            if Segment(P, Q) in segments and Segment(U, V) in segments:
                facts.append(Fact("cong", [cAB, cCD]))
        return facts