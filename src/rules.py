from src.database import Database
from src.predicate import Predicate
from src.fact import Fact
from src.primitives import Angle, Triangle, Ratio, Segment


class FC:
    """
    One step forward chaining, deduct all the new facts
    that can be infered with the database, the predicate,
    and the rules
    """

    def __init__(self, database: Database):
        self.database = database

    def deduct(self, p: Predicate) -> set[Fact]:
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
            facts += self._ruleD22(p)
            facts += self._ruleD39(p)
            facts += self._ruleD47(p)
            # facts += self._ruleD58auto(p)
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
            facts += self._ruleX4(p)
        if p.type == "cyclic":
            facts += self._ruleD41(p)
        if p.type == "perp":
            facts += self._ruleD09(p)
            facts += self._ruleD10perp(p)
            facts += self._ruleD52perp(p)
            facts += self._ruleX2(p)
            facts += self._ruleX3(p)
        if p.type == "simtri":
            facts += self._ruleD59(p)
            facts += self._ruleD60(p)
            facts += self._ruleD61simtri(p)
        if p.type == "contri":
            facts += self._ruleD62(p)
        if p.type == "eqratio":
            facts += self._ruleD75eqratio(p)

        return list(set(facts))

    def _ruleX2(self, predicate: Predicate) -> list[Fact]:
        """
        perp(A,B,C,D) & perp(P,Q,U,V) => eqangle(A,B,C,D,P,Q,U,V)
        """
        if len(predicate.lines) == 2:
            lAB, lCD = predicate.lines
        else:
            A, B, C, D = predicate.points
            lAB = self.database.matchLine([A, B])
            lCD = self.database.matchLine([C, D])
        facts = []
        for [lPQ, lUV] in self.database.perpFacts:
            # print(lPQ, lUV, A, B, C, D)
            if lAB == lPQ and lCD == lUV:
                continue
            if lAB == lUV and lCD == lPQ:
                continue
            facts += [
                Fact("eqangle", [lAB, lCD, lPQ, lUV]),
                Fact("eqangle", [lAB, lCD, lUV, lPQ])
            ]
        return facts

    def _ruleX3(self, predicate: Predicate) -> list[Fact]:
        """
        perp(A,B,C,D) => eqangle(A,B,C,D,C,D,A,B)
        """
        A, B, C, D = predicate.points
        lAB = self.database.matchLine([A, B])
        lCD = self.database.matchLine([C, D])

        return [Fact("eqangle", [lAB, lCD, lCD, lAB])]

    def _ruleX4(self, predicate: Predicate) -> list[Fact]:
        """
        cong(M,A,M,B) & coll(M,A,B) => midp(M,A,B)
        """
        M1, A, M2, B = predicate.points
        if M1 != M2:
            return []
        if self.database.containsFact(Fact("coll", [M1, A, B])):
            return [Fact("midp", [M1, A, B])]
        return []

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
        lAB, lCD, lPQ, lUV = predicate.lines

        facts = []
        # TODO: check the S_2 symmetric form.
        for angles in self.database.eqangleFacts:
            if Angle(lAB, lCD) in angles:
                angles = [
                    angle for angle in angles
                    if angle not in [Angle(lAB, lCD),
                                     Angle(lPQ, lUV)]
                ]
                for angle in angles:
                    lEF, lGH = angle.lk1, angle.lk2
                    facts.append(Fact("eqangle", [lPQ, lUV, lEF, lGH]))
            elif Angle(lPQ, lUV) in angles:
                angles = [
                    angle for angle in angles
                    if angle not in [Angle(lAB, lCD),
                                     Angle(lPQ, lUV)]
                ]
                for angle in angles:
                    lEF, lGH = angle.lk1, angle.lk2
                    facts.append(Fact("eqangle", [lAB, lCD, lEF, lGH]))
        return facts

    def _ruleD39(self, predicate: Predicate):
        """
        eqangle(A,B,P,Q,C,D,P,Q) => para(A,B,C,D)
        """
        if len(predicate.lines) == 4:
            lAB, lPQ, lCD, lUV = predicate.lines
            if lPQ != lUV:
                return []
        else:
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
        if len(predicate.lines) == 4:
            l1, l2, l3, l4 = predicate.lines
            if l1 == l3:  # Q: Maybe check parallelization also?
                return []
            for la, lb in [(l1, l2), (l3, l4), (l1, l3), (l2, l4)]:
                if not self.database.lineIntersection(la, lb):
                    # print("Warning: fail to find intersections between",
                    #       f"lines {la} and {lb}.",
                    #       "This may cause incompleteness of facts.")
                    # TODO: one possible solution is to define adhoc points and
                    #       define a mechanics to identify
                    #       when intersection shows up
                    return []
            A = self.database.lineIntersection(l1, l2)[0]
            B = self.database.lineIntersection(l3, l4)[0]
            P = self.database.lineIntersection(l3, l1)[0]
            Q = self.database.lineIntersection(l2, l4)[0]
            # print("\nCandidates FOR CYCLIC", A, B, P, Q, "\n")
            if len(set([A, B, P, Q])) < 4:
                return []
            return [Fact("cyclic", [A, B, P, Q])]

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
            if self.database.containsFact(Fact("coll", [A, B, C])):
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

        if O1 != O2 or A == B or O1 == A or self.database.containsFact(
                Fact("coll", [O1, A, B])):
            return []

        lOA = self.database.matchLine([O1, A])
        lAB = self.database.matchLine([A, B])
        lOB = self.database.matchLine([O1, B])
        return [Fact("eqangle", [lOA, lAB, lAB, lOB])]

    def _ruleD47(self, predicate: Predicate):
        """
        eqangle(O,A,A,B,A,B,O,B) => cong(O,A,O,B)
        """
        if len(predicate.lines) == 4:
            l1, l2, l3, l4 = predicate.lines
            if l2 != l3:
                return []
            for la, lb in [(l1, l2), (l1, l4), (l2, l4)]:
                if not self.database.lineIntersection(la, lb):
                    # print("Warning: fail to find intersections between",
                    #       f"lines {la} and {lb}.",
                    #       "This may cause incompleteness of facts.")
                    # TODO: one possible solution is to define adhoc points and
                    #       define a mechanics to identify
                    #       when intersection shows up
                    return []
            A1 = self.database.lineIntersection(l1, l2)[0]
            O1 = self.database.lineIntersection(l1, l4)[0]
            B1 = self.database.lineIntersection(l2, l4)[0]
            if A1 == O1 or A1 == B1 or O1 == B1:
                return []
            return [Fact("cong", [Segment(O1, A1), Segment(O1, B1)])]

        O1, A1, A2, B1, A3, B2, O2, B3 = predicate.points
        valid = all([
            A1 == A2, A1 == A3, B1 == B2, B1 == B3, O1 == O2,
            not self.database.containsFact(Predicate("coll", [O1, A1, B1]))
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

    def _ruleD58auto(self, predicate: Predicate):
        """
        eqangle(A,B,B,D,A,C,C,D) & intersect(E,A,C,B,D)
        => simtri(A,B,E,D,C,E)
        """
        ret = []
        l1, l2, l3, l4 = predicate.lines
        if len(set([l1, l2, l3, l4])) < 4:
            return []

        A = self.database.lineIntersection(l1, l3)
        B = self.database.lineIntersection(l1, l2)
        C = self.database.lineIntersection(l3, l4)
        D = self.database.lineIntersection(l2, l4)
        E = self.database.lineIntersection(l2, l3)
        F = self.database.lineIntersection(l1, l4)
        if not (A and B and C and D):
            return []
        A, B, C, D = A[0], B[0], C[0], D[0]
        if E:
            E = E[0]
            ret += [Fact("simtri", [Triangle(A, B, E), Triangle(D, C, E)])]
        if F:
            F = F[0]
            ret += [Fact("simtri", [Triangle(A, C, F), Triangle(D, B, F)])]

        return ret

    def _ruleD58(self, predicate: Predicate):
        """
        eqangle(A,B,B,C,P,Q,Q,R) & eqangle(A,C,B,C,P,R,Q,R) & ~ coll(A,B,C)
        => simtri(A,B,C,P,Q,R)
        """
        # print("PROVER::_RULE58", predicate)

        l1, l2, l3, l4 = predicate.lines
        if l1 == l2:
            return []
        for (la, lb) in [(l1, l2), (l3, l4)]:
            # print("PROVER::_RULED58", la, lb)
            if not self.database.lineIntersection(la, lb):
                # print("Warning: _RULED58 fail to find intersections between",
                #       f"lines {la} and {lb}.",
                #       "This may cause incompleteness of facts.")
                # TODO: one possible solution is to define adhoc points and
                #       define a mechanics to identify
                #       when intersection shows up
                return []
            for (la, lb) in [(l1, l2), (l3, l4)]:
                # print("PROVER::_RULED58", la, lb)
                if not self.database.lineIntersection(la, lb):
                    # print("Warning: _RULED58 fail to find intersections between",
                    #       f"lines {la} and {lb}.",
                    #       "This may cause incompleteness of facts.")
                    # TODO: one possible solution is to define adhoc points and
                    #       define a mechanics to identify
                    #       when intersection shows up
                    return []
            B = self.database.lineIntersection(l1, l2)[0]
            Q = self.database.lineIntersection(l3, l4)[0]
            # MARK next we should call `self.prove`, but we do not need, just
            # check for all existing lines, whether admit any existing eqangle.
            ret = []
            for e in self.database.eqangleFacts:
                if (Angle(l1, l2) in e or Angle(l2, l1) in e
                        or Angle(l3, l4) in e or Angle(l4, l3) in e):
                    continue
                a1 = [(l2 == a.lk1, a) for a in e
                      if l2 == a.lk1 or l2 == a.lk2]
                a2 = [(l4 == a.lk1, a) for a in e
                      if l4 == a.lk1 or l4 == a.lk2]
                for f1, angle1 in a1:
                    for f2, angle2 in a2:
                        if f1 != f2:
                            # full angle does not fit in the eqangle.
                            # does not imply simtri.
                            continue
                        if self.database.containsFact(
                                Fact("eqangle", [
                                    angle1.lk1, angle1.lk2, angle2.lk1,
                                    angle2.lk2
                                ])):
                            C = self.database.lineIntersection(
                                angle1.lk1, angle1.lk2)
                            R = self.database.lineIntersection(
                                angle2.lk1, angle2.lk2)
                            if f1:
                                A = self.database.lineIntersection(
                                    angle1.lk2, l1)
                                P = self.database.lineIntersection(
                                    angle2.lk2, l3)
                            else:
                                A = self.database.lineIntersection(
                                    angle1.lk1, l1)
                                P = self.database.lineIntersection(
                                    angle2.lk1, l3)
                            if not (A and P and C and R):
                                continue

                            A, P, C, R = A[0], P[0], C[0], R[0]
                            if ((B != Q or C != R or A != P)
                                    and len(set([A, B, C])) +
                                    len(set([P, Q, R])) == 6):
                                ret += [
                                    Fact(
                                        "simtri",
                                        [Triangle(A, B, C),
                                         Triangle(P, Q, R)])
                                ]
        return ret

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
        if len(predicate.lines) == 4:
            l1, l2, l3, l4 = predicate.lines
            if (l1 != l4 or l2 != l3
                    or self.database.containsFact(Fact("para", [l1, l2]))):
                return []
            return [Fact("perp", [l1, l2])]

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
        if len(predicate.lines) == 4:
            l1, l2, l3, l4 = predicate.lines
            if self.database.containsFact(Fact("para", [l3, l4])) and l1 != l2:
                return [Fact("para", [l1, l2])]
            return []

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
        if len(predicate.lines) == 4:
            l1, l2, l3, l4 = predicate.lines
            if self.database.containsFact(Fact("perp", [l3, l4])):
                return [Fact("perp", [l1, l2])]
            return []

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
                for sAB in self.database.congs[ratio.c1]:
                    for sCD in self.database.congs[ratio.c2]:
                        facts.append(Fact("cong", [sAB, sCD]))
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
