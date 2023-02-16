from src.predicate import Predicate
from src.util import deduplicate


class Database:
    """
    Structure of the database

    coll. a list of points on the same line.
    para. a pair of line pointers l1 and l2 meaning that l1 // l2. 
    perp. a pair of line pointers l1 and l2 meaning that l1 |_ l2.
    midp. a three tuple of points [M, A, B], meaning that M is the midpoint of AB.
    eqangle. a four tuple of line pointers l1, l2, l3, l4 meaning that [l1,l2]=[l3,l4]
    cong. a list of pairs of points

    Attributes
        paraFacts: a list of para
        midpFacts: a list of midp
        eqangleFacts: a list of eqangle
        congFacts: a list of cong
        lineDict: a dictionary with line name, points on line as the key, value pair
    

    Methods
        add(self, predicate)
        1. adding a collinear predicate. coll(p1, p2, p3)
            call collFacts.add(predicate):
                if p1, p2, p3 dont appear in any lines before
                    create a new line
                elif any two of them appear in a line before
                    add points to the line
                    merge if possible
                    reset line dictionary


        2. adding a parallel predicate. para(p1, p2, p3, p4)
            call searchLineName for [p1, p2] and [p3, p4]
            if not exists, create new entry in the lineDict for the lines

            call paraFacts.add( para(lx, ly) ): if lx or ly exists in the
            para line pairs, append them to the parallel line set
        
        3. adding a eqangle predicate. eqangle(p1,p2,p3,p4,p5,p6,p7,p8)
            four lines: [p1,p2]...[p7,p8], call searchLineName...

            call eqangleFacts.add( eqangle(l1,l2,l3,l4) )


    """

    def __init__(self) -> None:
        self.paraFacts = []
        self.midpFacts = []
        self.eqangleFacts = []
        self.lineDict = {}
        self.congDict = {}

    def add(self, predicate: Predicate) -> None:
        if predicate.type == "coll":
            self.collHandler(predicate)
        elif predicate.type == "para":
            self.paraHandler(predicate)
        elif predicate.type == "midp":
            self.midpHandler(predicate)
        elif predicate.type == "eqangle":
            self.eqangleHandler(predicate)
        elif predicate.type == "cong":
            self.congHandler(predicate)

    def eqangleHandler(self, predicate: Predicate):
        # adding eqangle(p1,p2,p3,p4,p5,p6,p7,p8) predicate
        p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points

        name1 = self._addLine([p1, p2])
        name2 = self._addLine([p3, p4])
        name3 = self._addLine([p5, p6])
        name4 = self._addLine([p7, p8])

        if self.isParallelLine([name1, name2]) or self.isParallelLine(
            [name3, name4]):
            return

        l1_sorted = sorted([name1, name2])
        l2_sorted = sorted([name3, name4])
        found = False
        idx = 0
        while not found and idx < len(self.eqangleFacts):
            eqanglefact = self.eqangleFacts[idx]
            if l1_sorted in eqanglefact and l2_sorted in eqanglefact:
                found = True
            elif l1_sorted in eqanglefact and l2_sorted not in eqanglefact:
                found = True
                self.eqangleFacts[idx].append(l2_sorted)
            elif l2_sorted in eqanglefact and l1_sorted not in eqanglefact:
                found = True
                self.eqangleFacts[idx].append(l1_sorted)

            idx += 1

        if not found:
            self.eqangleFacts.append([l1_sorted, l2_sorted])

    def midpHandler(self, predicate: Predicate):
        # adding midp(M, A, B) predicate
        p1, p2, p3 = predicate.points

        self.add(Predicate("coll", points=[p1, p2, p3]))

        if ([p1, p2, p3] not in self.midpFacts) and ([p1, p3, p2]
                                                     not in self.midpFacts):
            self.midpFacts.append([p1, p2, p3])

    def congHandler(self, predicate: Predicate):
        # adding a cong(p1,p2,p3,p4) predicate
        p1, p2, p3, p4 = predicate.points
        self._addLine([p1, p2])
        self._addLine([p3, p4])

        p12 = sorted([p1, p2])
        p34 = sorted([p3, p4])
        found = False
        for congName, pointPairs in self.congDict.items():
            if p12 in pointPairs and p34 in pointPairs:
                found = True
            elif p12 in pointPairs and p34 not in pointPairs:
                found = True
                self.congDict[congName].append(p34)
            elif p34 in pointPairs and p12 not in pointPairs:
                found = True
                self.congDict[congName].append(p12)

            if found:
                break

        if not found:
            self.congDict[self.newCongName] = [p12, p34]
        else:
            self._congMerge()

    def collHandler(self, predicate: Predicate):
        # adding a coll(A,B,C) predicate
        points = predicate.points

        # check if [A,B,C] is a new line or not
        isNewLine = True
        for lineName, pointsOnLine in self.lineDict.items():
            inCount = sum(p in pointsOnLine for p in points)
            if inCount >= 2:
                self.lineDict[lineName] = sorted(
                    deduplicate(pointsOnLine + points))
                isNewLine = False
                break

        if isNewLine:
            self.lineDict[self.newLineName] = predicate.points
        else:
            self._lineMerge()

    def paraHandler(self, predicate: Predicate):
        # adding a para(p1, p2, p3, p4) predicate
        p1, p2, p3, p4 = predicate.points

        # add line
        name1 = self._addLine([p1, p2])
        name2 = self._addLine([p3, p4])

        # search name in the parallel lines
        exists = False
        for idx, paraLines in enumerate(self.paraFacts):
            if name1 in paraLines or name2 in paraLines:
                exists = True
                self.paraFacts[idx] = deduplicate(paraLines + [name1, name2])

        if not exists:
            self.paraFacts.append([name1, name2])

    def _addLine(self, points: list[str]) -> str:
        assert len(points) == 2
        for name, line in self.lineDict.items():
            if all(p in line for p in points):
                return name

        newName = self.newLineName
        self.lineDict[newName] = points
        return newName

    @property
    def newLineName(self):
        oldLineName = list(self.lineDict.keys())
        for c in range(1, 20):
            if f"line{c}" not in oldLineName:
                return f"line{c}"

    @property
    def newCongName(self):
        oldCongName = list(self.congDict.keys())
        for c in range(1, 20):
            if f"cong{c}" not in oldCongName:
                return f"cong{c}"

    def _lineMerge(self):
        """Merge the lines
        """

        def more_than_two_overlap(first, second):
            return sum(p in second for p in first) >= 2

        # greedy expandsion
        unmerged = list(self.lineDict.keys())
        merged = []
        while len(unmerged) > 0:
            first, rest = unmerged[0], unmerged[1:]
            unmerged = []
            merged_cur = [first]
            for c in rest:
                l1, l2 = self.lineDict[first], self.lineDict[c]
                if more_than_two_overlap(l1, l2):
                    merged_cur.append(c)
                else:
                    unmerged.append(c)
            merged.append(merged_cur)

        res = {}
        for to_merge in merged:
            name = to_merge[0]
            points = []
            for n in to_merge:
                points += self.lineDict[n]

            # Reset line dictionary
            for idx1, lines in enumerate(self.paraFacts):
                for idx2, line in enumerate(lines):
                    if line in to_merge[1:]:
                        self.paraFacts[idx1][idx2] = name
                self.paraFacts[idx1] = deduplicate(self.paraFacts[idx1])

            res[name] = deduplicate(points)

        self.lineDict = res

        return True

    def _congMerge(self):
        """Merge the lines
        """

        def more_than_one_overlap(first, second):
            return sum(ppair in second for ppair in first) >= 1

        # greedy expandsion
        unmerged = list(self.congDict.keys())
        merged = []
        while len(unmerged) > 0:
            first, rest = unmerged[0], unmerged[1:]
            unmerged = []
            merged_cur = [first]
            for r in rest:
                c1, c2 = self.congDict[first], self.congDict[r]
                if more_than_one_overlap(c1, c2):
                    merged_cur.append(r)
                else:
                    unmerged.append(r)
            merged.append(merged_cur)

        res = {}
        for to_merge in merged:
            name = to_merge[0]
            ppairs = []
            for n in to_merge:
                ppairs += self.congDict[n]

            # Reset line dictionary
            # for idx1, lines in enumerate(self.paraFacts):
            #     for idx2, line in enumerate(lines):
            #         if line in to_merge[1:]:
            #             self.paraFacts[idx1][idx2] = name
            #     self.paraFacts[idx1] = list(set(self.paraFacts[idx1]))

            res[name] = deduplicate(ppairs)

        self.congDict = res
        return True

    def __repr__(self) -> str:
        s = "Database\n\n"

        # coll
        s += "> Coll Facts\n"
        for points in self.lineDict.values():
            if len(points) >= 3:
                s += f"  coll({','.join(sorted(points))})\n"

        # para
        s += "\n> Para Facts\n"
        for lines in self.paraFacts:
            s += f"  para( "
            for lineName in lines:
                s += f"[{','.join(self.lineDict[lineName])}] "
            s += f")\n"

        # midp
        s += "\n> Midp Facts\n"
        for midfact in self.midpFacts:
            M, A, B = midfact
            s += f"  midp({M},{A},{B})\n"

        # eqangle
        s += "\n> Eqangle Facts\n"
        for eqanglefact in self.eqangleFacts:
            s += f"  eqangle("
            for angle in eqanglefact:
                l1, l2 = angle
                s += f" ([{','.join(self.lineDict[l1])}],[{','.join(self.lineDict[l2])}]) "
            s += f")\n"

        # cong
        s += "\n> Cong Facts\n"
        for congfact in self.congDict.values():
            s += f"  cong( "
            for ppair in congfact:
                s += f"[{','.join(ppair)}] "
            s += f")\n"

        s += "\n" + "#" * 40 + "\n\n"

        return s

    def isCollinear(self, points: list[str]) -> bool:
        for _, line in self.lineDict.items():
            if all(p in line for p in points):
                return True
        return False

    def isParallelLine(self, lines: list[str]) -> bool:
        for parafact in self.paraFacts:
            if all(line in parafact for line in lines):
                return True
        return False


### Examples

# paraFacts
# [ [l1,l2], [l3,l4,l5], ... ]

# eqangleFacts
# [ [ [l1,l2], [l1,l3], [l4,l5] ], [ [l1,l4], [l5,l6]  ]  ]

# congFacts
# [ [ [p1,p2], [p1,p3], [p4,p5] ],  [ [p6,p7], [p1,p8] ] ]
