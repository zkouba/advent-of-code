import math
from typing import Tuple


DEBUG = False
TARGET = 2020


def load(file_path: str) -> list:
    ret_val = []
    with open(file_path, 'r') as input_file:
        for line in input_file:
            ret_val.append(int(line.strip()))
    log("Loaded %d values" % len(ret_val))
    return ret_val


def find_pair(
        input_list: list,
        target: int = TARGET
) -> Tuple[int, int] or None:

    half = math.ceil(len(input_list) / float(2))
    log("Going to search through %d candidates" % half)
    for i in range(half):
        candidate = input_list[0]
        input_list = input_list[1:]
        complement = target - candidate
        if complement in input_list[1:]:
            return candidate, complement
    return None


def find_triplet(
        input_list: list,
        target: int = TARGET
) -> Tuple[int, int, int] or None:

    for i in range(len(input_list) - 2):
        candidate = input_list[0]
        input_list = input_list[1:]
        sub_target = target - candidate
        pair = find_pair(input_list, sub_target)
        if pair is not None:
            return candidate, pair[0], pair[1]
    return None


def main() -> None:
    input_list = load("./input.txt")

    t = find_pair(input_list)
    print("Found: %s" % str(t))
    if t is None:
        raise RuntimeError("No pair found")
    print(t[0] * t[1])

    t = find_triplet(input_list)
    print("Found: %s" % str(t))
    if t is None:
        raise RuntimeError("No triplet found")
    print(t[0] * t[1] * t[2])


def log(msg: str) -> None:
    if DEBUG:
        print(msg)


if __name__ == "__main__":
    main()
