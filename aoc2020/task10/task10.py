from typing import List, Dict


def load(input_path: str) -> List[int]:
    ret_val = []
    with open(input_path, 'r') as input_file:
        for line in input_file:
            ret_val.append(int(line))
    return ret_val


def increment(item: int, dist: Dict[int, int]) -> None:
    if item in dist.keys():
        dist[item] = dist[item] + 1
    else:
        dist[item] = 1


def count_differences(arr: List[int]) -> Dict[int, int]:
    dist: Dict[int, int] = {}
    prev = 0
    for i in arr:
        diff = i - prev
        increment(diff, dist)
        prev = i
    # validate differences
    max_step = max(dist.keys())
    if max_step > 3:
        raise ValueError("Invalid difference between steps: %d" % max_step)
    # ...and add the last step
    increment(3, dist)
    return dist


def sum_children(item: int, arr: List[int], done: Dict[int, int] = None) -> int:
    if len(arr) < 2:
        # we've reached the end - stop the recursion
        return 1
    if done is None:
        done = {}
    s = 0
    # sum options for all existing children
    for i in range(1, 4):
        x = item + i
        if x in arr[0:3]:
            # try taking advantage of already computed options, otherwise dive deeper into recursion
            n = done[x] if x in done.keys() else sum_children(x, arr[(arr.index(x) + 1):], done)
            # store the computed value for future reference
            done[x] = n
            s += n
    return s


def main() -> None:
    arr = load("./input.txt")
    arr.sort()
    print("%d -> %d" % (arr[0], arr[-1]))
    dist = count_differences(arr)
    print(str(dist))
    print("Distribution: %d" % ((dist[1] if 1 in dist.keys() else 0) * dist[3]))
    print("Options: %d" % sum_children(0, arr))


if __name__ == "__main__":
    main()
