from src.predicate import Predicate
from typing import List


class Database:
    """
    Structure of the database

    coll. a list of points on the same line.
    para. a pair of line pointers l1 and l2 meaning that l1 // l2. 
    perp. a pair of line pointers l1 and l2 meaning that l1 |_ l2.
    midp. a three tuple of points [M, A, B], meaning that M is the midpoint of AB.

    Attributes
        collFacts: a list of coll
        paraFacts: a list of para
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


    """

    def __init__(self) -> None:
        self.paraFacts = []
        self.midpFacts = []
        self.lineDict = {}

    def add(self, predicate: Predicate) -> None:
        if predicate.type == "coll":
            self.collHandler(predicate)
        elif predicate.type == "para":
            self.paraHandler(predicate)
        elif predicate.type == "midp":
            self.midpHandler(predicate)

    def midpHandler(self, predicate: Predicate):
        # adding midp(M, A, B) predicate
        p1, p2, p3 = predicate.points

        self._addLine(predicate.points)

        midpFact = [p1, set([p2, p3])]
        if midpFact not in self.midpFacts:
            self.midpFacts.append(midpFact)

    def collHandler(self, predicate: Predicate):
        # adding a coll(A,B,C) predicate
        points = predicate.points

        # check if [A,B,C] is a new line or not
        isNewLine = True
        for lineName, pointsOnLine in self.lineDict.items():
            inCount = sum(p in pointsOnLine for p in points)
            if inCount >= 2:
                self.lineDict[lineName] = sorted(
                    list(set(pointsOnLine + points)))
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
                self.paraFacts[idx] = list(set(paraLines + [name1, name2]))

        if not exists:
            self.paraFacts.append([name1, name2])

    def _addLine(self, points: List[str]) -> str:
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
            if f"l{c}" not in oldLineName:
                return f"l{c}"

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
                self.paraFacts[idx1] = list(set(self.paraFacts[idx1]))

            res[name] = list(set(points))

        self.lineDict = res

        return True

    def __repr__(self) -> str:
        s = "Database\n\n"

        # coll
        s += "> Coll Facts\n"
        for points in self.lineDict.values():
            if len(points) >= 3:
                s += f"  coll({', '.join(sorted(points))})\n"

        # para
        s += "\n> Para Facts\n"
        for lines in self.paraFacts:
            s += f"  para( "
            for lineName in lines:
                s += f"[{', '.join(self.lineDict[lineName])}] "
            s += f")\n"

        # midp
        s += "\n> Midp Facts\n"
        for midfact in self.midpFacts:
            M, A, B = midfact[0], list(midfact[1])[0], list(midfact[1])[1]
            s += f"  midp({M}, {A}, {B})\n"

        s += "\n" + "#" * 40 + "\n\n"
        return s
