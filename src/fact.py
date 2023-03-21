"""
fact.py
"""


class Fact:

    def __init__(self, type, objects) -> None:
        self.type = type
        self.objects = objects

    def __repr__(self):
        return f"{self.type} ({self.objects})"