from src.primitives import Point, Segment, Angle, Triangle, LineKey, CongKey
from src.predicate import Predicate


class Database:

    def __init__(self,
                 lines: dict[LineKey, set[Point]] = None,
                 congs: dict[CongKey, set[Segment]] = None,
                 eqangleFacts: list[set[Angle]] = None,
                 midpFacts: list[list[Point]] = None,
                 paraFacts: list[set[LineKey]] = None) -> None:
        self.lines = lines if lines else {}
        self.congs = congs if congs else {}
        self.eqangleFacts = eqangleFacts if eqangleFacts else []
        self.midpFacts = midpFacts if midpFacts else []
        self.paraFacts = paraFacts if paraFacts else []

    def add(self, predicate: Predicate) -> None:
        if predicate.type == "coll":
            self.collHandler(predicate)
        elif predicate.type == "para":
            self.paraHandler(predicate)
        elif predicate.type == "eqangle":
            self.eqangleHandler(predicate)
        elif predicate.type == "cong":
            self.congHandler(predicate)

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
        self.lines[newName] = points
        return newName

    def paraHandler(self, predicate: Predicate):
        """Example facts
        [
            {l1, l2, l3}, {l4, l5}
        ]

        Adding a para(A,B,C,D) into the facts
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

        # eqangle
        s += "\n> Eqangle Facts\n"
        for angles in self.eqangleFacts:
            s += f"  eqangle( "
            angles_str = []
            for angle in angles:
                angles_str.append(self.angle_to_str(angle))
            s += ", ".join(angles_str)
            s += f" )\n"

        # cong
        s += "\n> Cong Facts\n"
        for segments in self.congs.values():
            s += f"  cong("
            segstr = []
            for segment in segments:
                segstr.append(self.segment_to_str(segment))
            s += ", ".join(segstr)
            s += f")\n"

        s += "\n" + "#" * 40 + "\n\n"

        return s

    def angle_to_str(self, angle: Angle):
        l1, l2 = angle.lk1, angle.lk2
        p1str = ','.join(sorted(self.lines[l1]))
        p2str = ','.join(sorted(self.lines[l2]))
        return f"Angle([{p1str}],[{p2str}])"

    def segment_to_str(self, segment: Segment):
        p1, p2 = sorted([segment.p1, segment.p2])
        return p1 + p2

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
