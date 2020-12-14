from typing import List


def load(input_path: str) -> List[int]:
    ret_val = []
    with open(input_path, 'r') as input_file:
        for line in input_file:
            bin = binarize_str(line)
            val = int(bin, 2)
            ret_val.append(val)
    return ret_val


def binarize_str(raw: str) -> str:
    return raw.strip().upper().replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")


def find_seat(passes: List[int]):
    passes.sort()
    prev = 7
    for i in range(len(passes)):
        curr = passes[i]
        r = curr // 8
        if r == 0:
            continue
        if r == 127:
            return None
        if curr - prev == 2:
            return curr - 1
        prev = curr
    return None


def main() -> None:
    passes = load("./input.txt")
    passes.sort()
    print(str(passes))
    highest = passes[-1]
    print("Highest seat id: %d" % highest)
    found = find_seat(passes)
    print("Found empty seat: %s" % str(found))


if __name__ == "__main__":
    main()
