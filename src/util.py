from src.predicate import Predicate
from typing import List


def parse_predicates_from_file(path_to_file: str) -> List[Predicate]:
    predicates = []
    with open(path_to_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            predicate = Predicate.from_line(line)
            predicates.append(predicate)
    return predicates


if __name__ == "__main__":
    print(parse_predicates_from_file("problems/p1"))