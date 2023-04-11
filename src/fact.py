r"""
fact.py
"""


class Fact:

    def __init__(self, type, objects) -> None:
        self.type = type
        self.objects = objects

    def __repr__(self):
        return f"{self.type} ({self.objects})"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: 'Fact') -> bool:
        if isinstance(other, Fact):
            return str(self) == str(other)
        return False
