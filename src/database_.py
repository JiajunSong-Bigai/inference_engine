from src.primitives import Point, Segment, Angle, LineKey, CongKey, Ratio, Triangle
from src.predicate import Predicate


class Database:

    def __init__(self,
                 lines: dict[LineKey, set[Point]] = None,
                 congs: dict[CongKey, set[Segment]] = None,
                 midpFacts: list[list[Point]] = None,
                 paraFacts: list[set[LineKey]] = None,
                 perpFacts: list[set[LineKey]] = None,
                 eqangleFacts: list[set[Angle]] = None,
                 eqratioFacts: list[set[Ratio]] = None,
                 simtriFacts: list[set[Triangle]] = None,
                 contriFacts: list[set[Triangle]] = None) -> None:
        self.lines = lines if lines else {}
        self.congs = congs if congs else {}
        self.midpFacts = midpFacts if midpFacts else []
        self.paraFacts = paraFacts if paraFacts else []
        self.perpFacts = perpFacts if perpFacts else []
        self.eqangleFacts = eqangleFacts if eqangleFacts else []
        self.eqratioFacts = eqratioFacts if eqratioFacts else []
        self.simtriFacts = simtriFacts if simtriFacts else []
        self.contriFacts = contriFacts if contriFacts else []

    def add(self, predicate: Predicate) -> None:
        if predicate.type == "coll":
            self.collHandler(predicate)
        if predicate.type == "midp":
            self.midpHandler(predicate)
        elif predicate.type == "para":
            self.paraHandler(predicate)
        elif predicate.type == "perp":
            self.perpHandler(predicate)
        elif predicate.type == "eqangle":
            self.eqangleHandler(predicate)
        elif predicate.type == "cong":
            self.congHandler(predicate)
        elif predicate.type == "eqratio":
            self.eqratioHandler(predicate)
        elif predicate.type == "simtri":
            self.simtriHandler(predicate)
        elif predicate.type == "contri":
            self.contriHandler(predicate)

    def contriHandler(self, predicate: Predicate):
        """Example facts
        [
            {T1, T2, T3}, {T4, T5}
        ]
        """
        p1, p2, p3, p4, p5, p6 = predicate.points
        t1 = Triangle(p1, p2, p3)
        t2 = Triangle(p4, p5, p6)

        idx = 0
        found = False
        contains_idx = []
        while idx < len(self.contriFacts):
            if t1 in self.contriFacts[idx] or t2 in self.contriFacts[idx]:
                found = True
                contains_idx.append(idx)
            idx += 1

        if found:
            if len(contains_idx) == 1:
                self.contriFacts[contains_idx[0]] = self.contriFacts[
                    contains_idx[0]].union({t1, t2})
            else:
                assert len(contains_idx) == 2
                first, second = contains_idx
                self.contriFacts[first] = self.contriFacts[first].union(
                    self.contriFacts[second].union({t1, t2}))
                del self.contriFacts[second]
        else:
            self.contriFacts.append({t1, t2})

    def simtriHandler(self, predicate: Predicate):
        """Example facts
        [
            {T1, T2, T3}, {T4, T5}
        ]
        """
        p1, p2, p3, p4, p5, p6 = predicate.points
        t1 = Triangle(p1, p2, p3)
        t2 = Triangle(p4, p5, p6)

        idx = 0
        found = False
        contains_idx = []
        while idx < len(self.simtriFacts):
            if t1 in self.simtriFacts[idx] or t2 in self.simtriFacts[idx]:
                found = True
                contains_idx.append(idx)
            idx += 1

        if found:
            if len(contains_idx) == 1:
                self.simtriFacts[contains_idx[0]] = self.simtriFacts[
                    contains_idx[0]].union({t1, t2})
            else:
                assert len(contains_idx) == 2
                first, second = contains_idx
                self.simtriFacts[first] = self.simtriFacts[first].union(
                    self.simtriFacts[second].union({t1, t2}))
                del self.simtriFacts[second]
        else:
            self.simtriFacts.append({t1, t2})

    def perpHandler(self, predicate: Predicate):
        """Example facts
        [
            {l1, l2}, {l1, l3}, {l4, l5}
        ]

        Add perp(A,B,C,D)
        """
        p1, p2, p3, p4 = predicate.points
        l1 = self.matchLine([p1, p2])
        l2 = self.matchLine([p3, p4])

        found = False
        idx = 0
        while not found and idx < len(self.perpFacts):
            if self.perpFacts[idx] == {l1, l2}:
                found = True
            idx += 1

        if not found:
            self.perpFacts.append({l1, l2})

    def congHandler(self, predicate: Predicate):
        """Add cong(A,B,C,D) predicate into the congs dictionary
        {
            "cong1": [s1, s2, s3],
            "cong2": [s4, s5]
        }
        """
        p1, p2, p3, p4 = predicate.points
        self.matchLine([p1, p2])
        self.matchLine([p3, p4])

        s1 = Segment(p1, p2)
        s2 = Segment(p3, p4)
        found = False
        for congKey, cong in self.congs.items():
            if s1 in cong or s2 in cong:
                found = True
                self.congs[congKey] = self.congs[congKey].union({s1, s2})
                break

        if not found:
            self.congs[self.newCongName] = {s1, s2}
        else:
            self._congMerge()

    def collHandler(self, predicate: Predicate):
        """Add coll(A,B,C) predicate into the lines dictionary
        {
            "line1": [A, B, C],
            "line2": [A, D]
        }
        """
        points = predicate.points
        isNewLine = True
        for lineKey, pointsOnLine in self.lines.items():
            inCount = sum(p in pointsOnLine for p in points)
            if inCount >= 2:
                self.lines[lineKey] = pointsOnLine.union(points)
                isNewLine = False
                break

        if isNewLine:
            self.lines[self.newLineName] = set(points)
        else:
            self._lineMerge()

    def paraHandler(self, predicate: Predicate):
        """Example facts
        [
            {l1, l2, l3}, {l4, l5}
        ]

        Add para(A,B,C,D)
        """
        p1, p2, p3, p4 = predicate.points
        # prepare the line
        l1 = self.matchLine([p1, p2])
        l2 = self.matchLine([p3, p4])
        # in the existing facts
        # search for the lines
        idx = 0
        found = False
        while not found and idx < len(self.paraFacts):
            if l1 in self.paraFacts[idx] or l2 in self.paraFacts[idx]:
                found = True
                self.paraFacts[idx] = self.paraFacts[idx].union({l1, l2})
            idx += 1

        if not found:
            self.paraFacts.append({l1, l2})

    def eqratioHandler(self, predicate: Predicate):
        """Example facts
        [
            {R1, R2, R3}, {R4, R5}
        ]
        
        Add a eqratio(A,B,C,D,E,F,G,H) into facts
        """
        p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points
        # l1 = self.matchLine([p1, p2])
        # l2 = self.matchLine([p3, p4])
        # l3 = self.matchLine([p5, p6])
        # l4 = self.matchLine([p7, p8])

        c1 = self.matchCong([p1, p2])
        c2 = self.matchCong([p3, p4])
        c3 = self.matchCong([p5, p6])
        c4 = self.matchCong([p7, p8])

        r1, r2 = Ratio(c1, c2), Ratio(c3, c4)
        # in the existing facts
        # search for the cong
        idx = 0
        found = False
        contains_idx = []
        while idx < len(self.eqratioFacts):
            if r1 in self.eqratioFacts[idx] or r2 in self.eqratioFacts[idx]:
                found = True
                contains_idx.append(idx)
            idx += 1

        if found:
            if len(contains_idx) == 1:
                self.eqratioFacts[contains_idx[0]] = self.eqratioFacts[
                    contains_idx[0]].union({r1, r2})
            else:
                # expand first, delete second
                assert len(contains_idx) == 2
                first, second = contains_idx
                self.eqratioFacts[first] = self.eqratioFacts[first].union(
                    self.eqratioFacts[second].union({r1, r2}))
                del self.eqratioFacts[second]

        else:
            self.eqratioFacts.append({r1, r2})

    def eqangleHandler(self, predicate: Predicate):
        """Example facts
        [
            {A1, A2, A3}, {A4, A5}...
        ]

        Adding a eqangle(A,B,C,D,E,F,G,H) into the facts
        """
        p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points
        l1 = self.matchLine([p1, p2])
        l2 = self.matchLine([p3, p4])
        l3 = self.matchLine([p5, p6])
        l4 = self.matchLine([p7, p8])

        a1, a2 = Angle(l1, l2), Angle(l3, l4)
        # in the existing facts
        # search for the lines
        idx = 0
        found = False
        while not found and idx < len(self.eqangleFacts):
            if a1 in self.eqangleFacts[idx] or a2 in self.eqangleFacts[idx]:
                found = True
                self.eqangleFacts[idx] = self.eqangleFacts[idx].union({a1, a2})
            idx += 1
        if not found:
            self.eqangleFacts.append({a1, a2})

    def midpHandler(self, predicate: Predicate):
        # Adding midp(M, A, B) predicate
        p1, p2, p3 = predicate.points
        self.add(Predicate("coll", points=[p1, p2, p3]))
        p2, p3 = sorted([p2, p3])
        if ([p1, p2, p3] not in self.midpFacts):
            self.midpFacts.append([p1, p2, p3])

    @property
    def newLineName(self):
        for n in range(1, 20):
            if f'line{n}' not in self.lines:
                return f'line{n}'
        raise ValueError("Running out names for lines!")

    @property
    def newCongName(self):
        for n in range(1, 20):
            if f'cong{n}' not in self.congs:
                return f'cong{n}'
        raise ValueError("Running out names for congs!")

    def __repr__(self) -> str:
        s = "Database\n\n"

        # coll
        s += "> Coll Facts\n"
        for points in self.lines.values():
            if len(points) >= 3:
                s += f"  coll({','.join(sorted(points))})\n"

        # para
        s += "\n> Para Facts\n"
        for lines in self.paraFacts:
            s += f"  para( "
            for lineName in lines:
                s += f"[{','.join(sorted(self.lines[lineName]))}] "
            s += f")\n"

        # perp
        s += "\n> Perp Facts\n"
        for lines in self.perpFacts:
            s += f"  perp( "
            for lineName in lines:
                s += f"[{','.join(sorted(self.lines[lineName]))}] "
            s += f")\n"

        # eqangle
        s += "\n> Eqangle Facts\n"
        for angles in self.eqangleFacts:
            s += f"  eqangle( "
            angles_str = []
            for angle in angles:
                angles_str.append(self.angle_to_str(angle))
            s += ", ".join(angles_str)
            s += " )\n"

        # cong
        s += "\n> Cong Facts\n"
        for segments in self.congs.values():
            if len(segments) > 1:
                s += "  cong("
                s += ", ".join([str(s) for s in segments])
                s += ")\n"

        # eqratio
        s += "\n> Eqratio Facts\n"
        for ratios in self.eqratioFacts:
            s += "  eqratio( "
            ratios_str = []
            for ratio in ratios:
                ratios_str.append(self.ratio_to_str(ratio))
            s += ", ".join(ratios_str)
            s += " )\n"

        # simtri
        s += "\n> Simtri Facts\n"
        for tris in self.simtriFacts:
            s += "  simtri( "
            tris_str = ["".join([tri.p1, tri.p2, tri.p3]) for tri in tris]
            s += ", ".join(tris_str)
            s += ")\n"

        s += "\n" + "#" * 40 + "\n\n"

        return s

    def angle_to_str(self, angle: Angle):
        l1, l2 = angle.lk1, angle.lk2
        p1str = ','.join(sorted(self.lines[l1]))
        p2str = ','.join(sorted(self.lines[l2]))
        return f"Angle([{p1str}],[{p2str}])"

    def ratio_to_str(self, ratio: Ratio):
        c1, c2 = ratio.c1, ratio.c2
        c1str = ",".join([str(s) for s in self.congs[c1]])
        c2str = ",".join([str(s) for s in self.congs[c2]])
        return f"Ratio([{c1str}],[{c2str}])"

    def _lineMerge(self):

        def more_than_two_overlap(first, second):
            return sum(p in second for p in first) >= 2

        # greedy expandsion
        unmerged = list(self.lines.keys())
        merged = []
        while len(unmerged) > 0:
            first, rest = unmerged[0], unmerged[1:]
            unmerged = []
            merged_cur = [first]
            for c in rest:
                l1, l2 = self.lines[first], self.lines[c]
                if more_than_two_overlap(l1, l2):
                    merged_cur.append(c)
                else:
                    unmerged.append(c)
            merged.append(merged_cur)

        res = {}
        for to_merge in merged:
            name = to_merge[0]
            points = set()
            for n in to_merge:
                points = points.union(self.lines[n])

            res[name] = points

        self.lines = res

    def _congMerge(self):

        def more_than_one_overlap(first, second):
            return sum(p in second for p in first) >= 1

        # greedy expandsion
        unmerged = list(self.congs.keys())
        merged = []
        while len(unmerged) > 0:
            first, rest = unmerged[0], unmerged[1:]
            unmerged = []
            merged_cur = [first]
            for c in rest:
                s1, s2 = self.congs[first], self.congs[c]
                if more_than_one_overlap(s1, s2):
                    merged_cur.append(c)
                else:
                    unmerged.append(c)
            merged.append(merged_cur)

        res = {}
        for to_merge in merged:
            name = to_merge[0]
            segments = set()
            for n in to_merge:
                segments = segments.union(self.congs[n])

            res[name] = segments

        self.congs = res

    def matchLine(self, points: list[Point]):
        """Search for the line, if found, return the name;
        else, create a new line connecting two points and
        return the new name
        """
        assert len(points) == 2
        for name, line in self.lines.items():
            if all(p in line for p in points):
                return name

        newName = self.newLineName
        self.lines[newName] = set(points)
        return newName

    def matchCong(self, points: list[Point]):
        """Search for the cong, if found, return the name;
        else, create a new Cong object with a segment of two points and
        return the new name
        """
        assert len(points) == 2
        for name, cong in self.congs.items():
            # cong is a list of segments
            for segment in cong:
                if str(segment) == "".join(sorted(points)):
                    return name

        newName = self.newCongName
        self.congs[newName] = [Segment(*points)]
        return newName
