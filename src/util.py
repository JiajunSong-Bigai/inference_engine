from src.predicate import Predicate


def parse_predicates_from_file(path_to_file: str) -> list[Predicate]:
    predicates = []
    with open(path_to_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            predicate = Predicate.from_line(line)
            predicates.append(predicate)
    return predicates


def deduplicate(a_list: list):
    res = []
    for e in a_list:
        if e not in res:
            res.append(e)
    return res


if __name__ == "__main__":
    print(parse_predicates_from_file("problems/p1"))