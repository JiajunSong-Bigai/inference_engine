"""
fact.py
"""


class Fact:

    def __init__(self, type, objects) -> None:
        self.type = type
        self.objects = objects

    def __repr__(self):
        if self.type in ["cyclic", "simtri", "contri", "perp", "para"]:
            return f"{self.type} ({sorted(self.objects)})"
        return f"{self.type} ({self.objects})"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: 'Fact') -> bool:
        if isinstance(other, Fact):
            return str(self) == str(other)
        return False

    def __lt__(self, other: 'Fact') -> bool:
        """Used by the sorting algorithm
        """
        types = [
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

        if self.type != other.type:
            return types.index(self.type) < types.index(other.type)

        return ",".join(str(o) for o in self.objects) < ",".join(
            str(o) for o in other.objects)
