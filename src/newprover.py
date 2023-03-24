"""
Step 1. Set the hypotheses of the statement to be initial new-fact-list
and the initial database. While the new-fact-list is not empty, do Step 2.

Step 2.Let d be the first new fact in the list. Delete it from the list,
add it to the database, and do Step 3.

Step 3.Let r be a rule whose body contains a predicate P0 of the fact d. 
To apply the rule r, we need to instantiate other predicates in r.
Since predicate P0 will be instantiated as the new fact d, other predicates
in r need to be instantiated for all the facts in the database.
For all the predicate forms of fact d (notice that a fact could have many
predicate forms) and for all the facts of the other predicates in r, do Step 4.

Step 4. Apply rule r to obtain a fact d0. If d0 is in the database, do nothing.
Otherwise, add it to the end of the new-fact-list.
"""

from src.primitives import Angle, Triangle, Ratio, Segment
from src.predicate import Predicate
from src.fact import Fact
from src.newdatabase import Database


class Prover:

    def __init__(self, hypotheses: list[Predicate]) -> None:
        self.database = Database()
        self.newFactsList = []

        for h in hypotheses:
            self.database.addPredicate(h)

        for h in hypotheses:
            newFact = self.database._predicate_to_fact(h)
            if newFact not in self.newFactsList:
                self.newFactsList.append(newFact)

        self.types = [
            "coll",
            "cong",
            "midp",
            "para",
            "perp",
            "eqangle",
            "eqratio",
            "simtri",
            "contri",
            "cyclic",
            "circle",
        ]

        self.newFactsList = sorted(self.newFactsList,
                                   key=lambda x: self.types.index(x.type))

    def prove(self, predicate: Predicate) -> bool:
        fact = self.database._predicate_to_fact(predicate)
        return self.database.containsFact(fact)

    def fixedpoint(self):
        i = UPPER = 20000
        while self.newFactsList and i > 0:
            i -= 1
            d: Fact = self.newFactsList.pop(0)
            self.database.addFact(d)

            print(d)
            oldnum = len(self.newFactsList)

            newFacts = []
            all_predicate_forms = self.database._predicate_all_forms(d)

            for predicate in all_predicate_forms:
                newFacts += self._rules(predicate)

            for fact in set(newFacts):
                if self.database.containsFact(fact):
                    continue
                self.newFactsList.append(fact)
                print(f"{fact} added")

            print(
                f"{len(self.newFactsList) - oldnum} added, {len(self.newFactsList)}\n"
            )

            self.newFactsList = sorted(self.newFactsList,
                                       key=lambda x: self.types.index(x.type))

        if i > 0:
            print(UPPER - i)

        return self.database

    def _rules(self, p: Predicate) -> list[Fact]:
        facts = []
        if p.type == "midp":
            facts += self._ruleD44(p)
            facts += self._ruleD63(p)
            facts += self._ruleD68(p)
            facts += self._ruleD69(p)
            facts += self._ruleD70(p)
        if p.type == "para":
            facts += self._ruleD40(p)
            facts += self._ruleD10para(p)
            facts += self._ruleD45para(p)
            facts += self._ruleD64(p)
            facts += self._ruleD65(p)
        if p.type == "eqangle":
            facts += self._ruleX1(p)
            facts += self._ruleD39(p)
            facts += self._ruleD47(p)
            facts += self._ruleD58(p)
            facts += self._ruleD71(p)
            facts += self._ruleD72(p)
            facts += self._ruleD73(p)
            facts += self._ruleD74(p)
            facts += self._ruleD42a(p)
        if p.type == "cong":
            facts += self._ruleD12(p)
            facts += self._ruleD46(p)
            facts += self._ruleD75cong(p)
        if p.type == "cyclic":
            facts += self._ruleD41(p)
        if p.type == "perp":
            facts += self._ruleD09(p)
            facts += self._ruleD10perp(p)
            facts += self._ruleD52perp(p)
            facts += self._ruleX2(p)
        if p.type == "simtri":
            facts += self._ruleD59(p)
            facts += self._ruleD60(p)
            facts += self._ruleD61simtri(p)
        if p.type == "contri":
            facts += self._ruleD62(p)
        if p.type == "eqratio":
            facts += self._ruleD75eqratio(p)

        return list(set(facts))

    def _ruleX1(self, predicate: Predicate) -> list[Fact]:
        """
        eqangle(A,B,B,C,P,Q,Q,R) & cong(A,B,P,Q) & cong(B,C,Q,R)
        => contri(A,B,C,P,Q,R)
        """
        A, B1, B2, C, P, Q1, Q2, R = predicate.points
        if B1 != B2 or Q1 != Q2 or self.prove(Predicate(
                "coll", [A, B1, C])) or self.prove(
                    Predicate("coll", [P, Q1, R])):
            return []

        if self.prove(Predicate("cong", [A, B1, P, Q1])) and self.prove(
                Predicate("cong", [B1, C, Q1, R])):
            return [Fact("contri", [Triangle(A, B1, C), Triangle(P, Q1, R)])]
        return []

    def _ruleX2(self, predicate: Predicate) -> list[Fact]:
        """
        perp(A,B,C,D) & perp(P,Q,U,V) => eqangle(A,B,C,D,P,Q,U,V)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])
        facts = []
        for [lPQ, lUV] in self.database.perpFacts:
            if lAB == lPQ and lCD == lUV:
                continue
            facts.append(Fact("eqangle", [lAB, lCD, lPQ, lUV]))
        return facts

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

        facts = []
        for angles in self.database.eqangleFacts:
            if Angle(lPQ, lUV) not in angles:
                continue
            for angle in angles:
                if angle == Angle(lPQ, lUV):
                    continue
                lEF, lGH = angle.lk1, angle.lk2
                facts.append(Fact("eqangle", [lAB, lCD, lEF, lGH]))
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
            if lPQ in [lAB, lCD] or self.database.containsFact(
                    Fact("para", [lPQ, lAB])) or self.database.containsFact(
                        Fact("para", [lPQ, lCD])):
                continue
            facts.append(Fact("eqangle", [lAB, lPQ, lCD, lPQ]))
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
        if lPA != lPB and lQA != lQB:
            return [Fact("eqangle", [lPA, lPB, lQA, lQB])]
        return []

    def _ruleD42a(self, predicate: Predicate):
        """
        eqangle(P,A,P,B,Q,A,Q,B) & not coll(P,Q,A) => cyclic(A,B,P,Q)
        """
        P1, A1, P2, B1, Q1, A2, Q2, B2 = predicate.points
        if P1 != P2 or A1 != A2 or B1 != B2 or Q1 != Q2:
            return []

        if self.prove(Predicate("coll", [P1, Q1, A1])):
            return []

        # print("Reaching here", predicate.points)

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
            A1 == A2, A1 == A3, B1 == B2, B1 == B3, O1 == O2,
            not self.prove(Predicate("coll", [O1, A1, B1]))
        ])
        if not valid:
            return []

        return [Fact("cong", [Segment(O1, A1), Segment(O1, B1)])]

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
                facts.append(Fact("cong", [Segment(A, M), Segment(B1, M)]))

        return facts

    def _ruleD58(self, predicate: Predicate):
        """
        eqangle(A,B,B,C,P,Q,Q,R) & eqangle(A,C,B,C,P,R,Q,R) & ~ coll(A,B,C)
        => simtri(A,B,C,P,Q,R)
        """

        A, B1, B2, C, P, Q1, Q2, R = predicate.points
        if B1 != B2 or Q1 != Q2 or self.prove(Predicate("coll", [A, B1, C])):
            return []

        if self.prove(Predicate(
                "eqangle", [A, C, B1, C, P, R, Q1, R
                            ])) and Triangle(A, B1, C) != Triangle(P, Q1, R):
            return [Fact("simtri", [Triangle(A, B1, C), Triangle(P, Q1, R)])]

        return []

    def _ruleD59(self, predicate: Predicate):
        """
        simtri(A,B,C,P,Q,R) => eqratio(A,B,A,C,P,Q,P,R)
        """
        A, B, C, P, Q, R = predicate.points
        return [
            Fact("eqratio",
                 [Segment(A, B),
                  Segment(A, C),
                  Segment(P, Q),
                  Segment(P, R)]),
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
        if Angle(lAB, lAC) == Angle(lPQ, lPR):
            return []
        return [
            Fact("eqangle", [lAB, lAC, lPQ, lPR]),
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
        return [Fact("cong", [Segment(A, B), Segment(P, Q)])]

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
                C, D = sorted([C, D])
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
            if O == A or O == B:
                continue
            facts.append(
                Fact("eqratio", [
                    Segment(O, A),
                    Segment(A, C),
                    Segment(O, B),
                    Segment(B, D)
                ]))
        return facts

    def _ruleD68(self, predicate: Predicate):
        """
        midp(A,B,C) => cong(A,B,A,C)
        """
        A, B, C = predicate.points
        return [Fact("cong", [Segment(A, B), Segment(A, C)])]

    def _ruleD69(self, predicate: Predicate):
        """
        midp(A,B,C) => coll(A,B,C)
        """
        A, B, C = predicate.points
        return [Fact("coll", [A, B, C])]

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
                facts.append(
                    Fact("eqratio", [
                        Segment(M, A),
                        Segment(A, B),
                        Segment(N, C),
                        Segment(C, D)
                    ]))

        return facts

    def _ruleD71(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,C,D,A,B) & ~ para(A,B,C,D) => perp(A,B,C,D)
        """
        A1, B1, C1, D1, C2, D2, A2, B2 = predicate.points
        if not all([
                A1 == A2, B1 == B2, C1 == C2, D1 == D2,
                not self.prove(Predicate("para", [A1, B1, C1, D1]))
        ]):
            return []
        lAB = self.database.matchLine([A1, B1])
        lCD = self.database.matchLine([C1, D1])
        if lAB == lCD:
            return []
        return [Fact("perp", [lAB, lCD])]

    def _ruleD72(self, predicate: Predicate):
        # """
        # eqangle(A,B,C,D,C,D,A,B) & ~ perp(A,B,C,D) => para(A,B,C,D)
        # """
        # A1, B1, C1, D1, C2, D2, A2, B2 = predicate.points
        # if not all([
        #         A1 == A2, B1 == B2, C1 == C2, D1 == D2,
        #         not self.prove(Predicate("perp", [A1, B1, C1, D1]))
        # ]):
        #     return []
        # lAB = self.database.matchLine([A1, B1])
        # lCD = self.database.matchLine([C1, D1])

        # if lAB == lCD:
        #     return []
        # return [Fact("para", [lAB, lCD])]
        return []

    def _ruleD73(self, predicate: Predicate):
        """
        eqangle(A,B,C,D,P,Q,U,V) & para(P,Q,U,V) => para(A,B,C,D)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        if self.prove(Predicate("para", [P, Q, U, V])):
            lAB = self.database.matchLine([A, B])
            lCD = self.database.matchLine([C, D])
            if lAB == lCD:
                return []
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
            if lAB == lCD:
                return []
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
                for [A, B] in self.database.congs[ratio.c1]:
                    for [C, D] in self.database.congs[ratio.c2]:
                        facts.append(
                            Fact("cong",
                                 [Segment(A, B), Segment(C, D)]))
        return facts

    def _ruleD75eqratio(self, predicate: Predicate):
        """
        eqratio(A,B,C,D,P,Q,U,V) & cong(P,Q,U,V) => cong(A,B,C,D)
        """
        A, B, C, D, P, Q, U, V = predicate.points
        facts = []
        for segments in self.database.congs.values():
            if Segment(P, Q) in segments and Segment(U, V) in segments:
                facts.append(Fact("cong", [Segment(A, B), Segment(C, D)]))
        return facts
