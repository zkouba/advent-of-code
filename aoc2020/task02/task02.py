import re
from typing import Tuple, List, Callable

PATTERN = re.compile("^(\\d+)\\s*-\\s*(\\d+)\\s*([a-zA-Z]):\\s*([a-zA-Z]+)$")


class Rule:

    def __init__(self, min_occurrences: int, max_occurrences: int, char: str):
        self.min = min_occurrences
        self.max = max_occurrences
        if len(char) != 1:
            raise ValueError(
                "A single character has to be specified. " +
                "Received '%s' instead." % char
            )
        self.char = char

    def validate_occurrences(self, phrase: str) -> bool:
        occurrences = phrase.count(self.char)
        return self.min <= occurrences <= self.max

    def validate_positions(self, phrase: str) -> bool:
        lower_idx = self.min - 1
        upper_idx = self.max - 1
        lower_position: bool = (0 <= lower_idx < len(phrase)) and phrase[lower_idx] == self.char
        upper_position: bool = (0 <= upper_idx < len(phrase)) and phrase[upper_idx] == self.char
        return (lower_position and not upper_position) or (upper_position and not lower_position)


def load(input_path: str) -> List[Tuple[Rule, str]]:
    ret_val = []
    with open(input_path, 'r') as input_file:
        for line in input_file:
            m = PATTERN.match(line)
            if m:
                ret_val.append(
                    (
                        Rule(int(m.group(1)), int(m.group(2)), m.group(3)),
                        m.group(4)
                    )
                )
            else:
                raise ValueError("Cannot parse line '%s'" % line)
    return ret_val


def validate_occurrences(input_list: List[Tuple[Rule, str]]) -> int:
    return validate(input_list, lambda rule, phrase: rule.validate_occurrences(phrase))


def validate_positions(input_list: List[Tuple[Rule, str]]) -> int:
    return validate(input_list, lambda rule, phrase: rule.validate_positions(phrase))


def validate(input_list: List[Tuple[Rule, str]], test: Callable[[Rule, str], bool]) -> int:
    valid_entries = 0
    for entry in input_list:
        if test(entry[0], entry[1]):
            valid_entries += 1
    return valid_entries


def main():
    input_list = load("./input.txt")
    valid_entries = validate_occurrences(input_list)
    print("Valid entries according to occurrences: %d" % valid_entries)

    valid_entries = validate_positions(input_list)
    print("Valid entries according to positions: %d" % valid_entries)


if __name__ == "__main__":
    main()
