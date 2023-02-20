"""predicate.py
"""


class Predicate:
    '''Predicate is simple fact, such as coll(A,B,C) or para(A,B,C,D)
    where A,B,C,D are concrete points.

    Predicate will mostly be used when parsing the input hypotheses.
    '''

    def __init__(self, type: str, points: list[str]) -> None:
        self.type = type
        self.points = points

    @classmethod
    def from_line(cls, line: str) -> 'Predicate':
        line = line.rstrip(".").strip()
        between_parent = line[line.find("(") + 1:line.find(")")]

        type = line[:line.find("(")]
        points = [p.strip() for p in between_parent.split(",")]

        return Predicate(type=type, points=points)

    def __repr__(self) -> str:
        return f"({self.type}, points({','.join(self.points)}))"


if __name__ == "__main__":
    for test_line in [
            "coll(A,B,C).", "coll(A,  B,C)", "coll(  A,B,  C)",
            "  coll(A,B,C)    ."
    ]:
        p = Predicate.from_line(test_line)
        assert str(p) == "(coll, points(A,B,C))"