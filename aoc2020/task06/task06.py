from typing import List, Callable


class Group:
    def __init__(self):
        self.positive_questions: List[bool] or None = None


def _load(input_path: str, combiner_fn: Callable[[bool, bool], bool]) -> List[Group]:
    ret_val: List[Group] = []
    rng = range(ord("a"), ord("z") + 1)
    a = ord("a")
    grp = Group()
    with open(input_path, 'r') as input_file:
        for raw_line in input_file:
            line = raw_line.strip().lower()
            if (line == "") and (len(grp.positive_questions) > 0):
                ret_val.append(grp)
                grp = Group()
            elif grp.positive_questions is None:
                grp.positive_questions = [
                    (chr(i) in line) for i in rng
                ]
            else:
                grp.positive_questions = [
                    combiner_fn(grp.positive_questions[i - a], chr(i) in line) for i in rng
                ]
    if len(grp.positive_questions) > 0:
        ret_val.append(grp)
    return ret_val


def load_join(input_path: str) -> List[Group]:
    return _load(
        input_path=input_path,
        combiner_fn=lambda b1, b2: b1 or b2)


def load_intersection(input_path: str) -> List[Group]:
    return _load(
        input_path=input_path,
        combiner_fn=lambda b1, b2: b1 and b2)


def sum_groups(groups: List[Group]) -> int:
    return sum(
        [sum(
            [1 if a else 0 for a in grp.positive_questions]
        ) for grp in groups]
    )


def main() -> None:
    groups = load_join("./input.txt")
    total_positive_questions = sum_groups(groups)
    print("Sum of joins: %d" % total_positive_questions)

    groups = load_intersection("./input.txt")
    total_positive_questions = sum_groups(groups)
    print("Sum of intersections: %d" % total_positive_questions)


if __name__ == "__main__":
    main()
