from src.primitives import LineKey, CongKey, Point, Segment, Angle, Triangle
from src.predicate import Predicate
from src.util import deduplicate


class LineBase:

    def __init__(self, lines: dict[LineKey, set[Point]] = {}) -> None:
        self.lines = lines

    def addCollLine(self, predicate: Predicate):
        """adding coll(A,B,C) predicate into the linebase dictionary"""
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
            self._merge()

    def connectLine(self, points: list[Point]):
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

    def _merge(self):

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
            points = []
            for n in to_merge:
                points += self.lines[n]

            res[name] = deduplicate(points)

        self.lines = res

    @property
    def newLineName(self):
        for n in range(1, 20):
            if f'line{n}' not in self.lines:
                return f'line{n}'
        raise ValueError("Running out names for lines!")


class ParaBase:
    """Example facts
    [
        {l1, l2, l3}, {l4, l5}
    ]
    """

    def __init__(self,
                 lineBase: LineBase,
                 facts: list[set[LineKey]] = None) -> None:
        self.lineBase = lineBase
        self.facts = facts if facts else []

    def addPara(self, predicate: Predicate):
        """Adding a para(A,B,C,D) predicate"""
        p1, p2, p3, p4 = predicate.points
        # prepare the line
        l1 = self.lineBase.connectLine([p1, p2])
        l2 = self.lineBase.connectLine([p3, p4])
        # in the existing facts
        # search for the lines
        idx = 0
        found = False
        while not found and idx < len(self.facts):
            if l1 in self.facts[idx] or l2 in self.facts[idx]:
                found = True
                self.facts[idx] = self.facts[idx].union({l1, l2})
            idx += 1

        if not found:
            self.facts.append({l1, l2})


class EqualAngleBase:
    """Example facts
    [
        {A1, A2, A3}, {A4, A5}...
    ]
    """

    def __init__(self,
                 lineBase: LineBase,
                 facts: list[set[Angle]] = None) -> None:
        self.lineBase = lineBase
        self.facts = facts if facts else []

    def addEqangle(self, predicate: Predicate):
        p1, p2, p3, p4, p5, p6, p7, p8 = predicate.points
        l1 = self.lineBase.connectLine([p1, p2])
        l2 = self.lineBase.connectLine([p3, p4])
        l3 = self.lineBase.connectLine([p5, p6])
        l4 = self.lineBase.connectLine([p7, p8])
        # in the existing facts
        # search for the lines
        idx = 0
        found = False
        while not found and idx < len(self.facts):
            a1, a2 = Angle(l1, l2), Angle(l3, l4)
            if a1 in self.facts[idx] or a2 in self.facts[idx]:
                found = True
                self.facts[idx] = self.facts[idx].union({a1, a2})
            idx += 1
        if not found:
            self.facts.append({a1, a2})


# class CongBase:

#     def __init__(self, congs: dict[CongKey, set[Segment]] = {}) -> None:
#         self.congs = congs

#     def add_cong(self, fact):
#         pass

#     def _merge(self):
#         pass

# class EqualRatioBase:

#     def __init__(self, congBase: CongBase) -> None:
#         self.congBase = congBase

#     def add_eqratio(self, fact):
#         pass