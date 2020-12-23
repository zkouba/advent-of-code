from typing import List


class CodeSequence:

    def __init__(self, sequence: List[int], preamble_len=25, memory_len=None):
        self.sequence: List[int] = sequence
        self.preamble_len: int = preamble_len
        self.memory_len: int = preamble_len if memory_len is None else memory_len
        self.idx: int = preamble_len

    def reset(self) -> None:
        self.idx = self.preamble_len

    def _verify_element(self) -> bool:
        if self.idx < self.memory_len or self.idx >= len(self.sequence):
            raise ValueError("Invalid position %d, mem: %d, len: %d" % (self.idx, self.memory_len, len(self.sequence)))
        current = self.sequence[self.idx]
        mem = self.sequence[self.idx - self.memory_len:self.idx]
        for i in range(self.memory_len - 1):
            x = mem[i]
            y = current - x
            if y >= 0 and y in mem[i:] and x != y:
                return True
        return False

    def find_next_glitch(self) -> int:
        while self.idx < len(self.sequence):
            if not self._verify_element():
                return self.idx
            self.idx += 1
        return -1

    def get(self):
        return self.sequence[self.idx]

    def find_encryption_weakness(self) -> List[int] or None:
        n = self.find_next_glitch()
        if n < 0:
            raise RuntimeWarning("No weakness found")
        target = self.get()

        adds = []
        total = 0
        i = 0
        while total != target and i < len(self.sequence):
            if total < target:
                # we're below the target sum -> try adding next number
                total += self.sequence[i]
                adds.append(self.sequence[i])
                i += 1
            else:
                # we've overshot -> try removing the first number from the sum
                x = adds.pop(0)
                total -= x
        if total == target:
            return adds
        else:
            return None


def load(input_path: str) -> CodeSequence:
    ret_val = []
    with open(input_path, 'r') as input_file:
        for line in input_file:
            ret_val.append(int(line))
    return CodeSequence(ret_val)


def main() -> None:
    seq = load("./input.txt")
    print("Rule broken at index %d by number: %d" % (seq.find_next_glitch(), seq.get()))
    adds = seq.find_encryption_weakness()
    print("Encryption Weakness: %s -> %d" % (str(adds), min(adds) + max(adds)))


if __name__ == "__main__":
    main()
