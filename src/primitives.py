class Point:
    pass


class LineKey:
    pass


class CongKey:
    pass


class Angle:

    def __init__(self, lk1: LineKey, lk2: LineKey) -> None:
        self.lk1 = lk1
        self.lk2 = lk2

    def __eq__(self, other: 'Angle') -> bool:
        if isinstance(other, Angle):
            return self.lk1 == other.lk1 and self.lk2 == other.lk2
        return False

    def __hash__(self) -> int:
        return hash(f"{self.lk1}, {self.lk2}")


class Segment:

    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other: 'Segment') -> bool:
        if isinstance(other, Segment):
            return sorted([self.p1, self.p2]) == sorted([other.p1, other.p2])
        return False

    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        return "".join(sorted([self.p1, self.p2]))


class Ratio:

    def __init__(self, c1: CongKey, c2: CongKey) -> None:
        self.c1 = c1
        self.c2 = c2


class Triangle:

    def __init__(self, p1: Point, p2: Point, p3: Point) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3