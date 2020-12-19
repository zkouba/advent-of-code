import re
from typing import List


GRP_NAME_OPERATION = "operation"
GRP_NAME_ARGUMENT = "arg"
PATTERN_INSTRUCTION = re.compile(
    "^\\s*(?P<%s>[a-zA-Z]+)\\s+(?P<%s>(-|\\+)?\\d+)\\s*$" % (GRP_NAME_OPERATION, GRP_NAME_ARGUMENT)
)


class InfiniteLoopException(RuntimeError):
    pass


class Instruction:

    ACC = "acc"
    JMP = "jmp"
    NOP = "nop"

    INSTRUCTIONS = [
        ACC, JMP, NOP
    ]

    def __init__(self, operation: str, argument: int):
        operation = operation.lower()
        if operation not in Instruction.INSTRUCTIONS:
            raise ValueError("Unsupported operation '%s'" % operation)
        self.operation = operation
        self.argument = argument

    def counterpart(self):
        if self.operation == Instruction.JMP:
            return Instruction.NOP
        if self.operation == Instruction.NOP:
            return Instruction.JMP
        return None


class State:
    def __init__(
            self,
            accumulator: int = 0,
            current_offset: int = 0,
            offset_history: List[int] = None,
            is_clone: bool = False,
            swap_next: bool = False
    ):
        self.accumulator: int = accumulator
        self.current_offset: int = current_offset
        self.offset_history: List[int] = [] if offset_history is None else offset_history
        self.is_clone: bool = is_clone
        self.swap_next: bool = swap_next

    def clone(self):
        return State(
            accumulator=self.accumulator,
            current_offset=self.current_offset,
            offset_history=self.offset_history[:],
            is_clone=True,
            swap_next=True
        )


class Automaton:
    def __init__(self, instructions: List[Instruction], state: State = State()):
        self.state = state
        self.instructions = instructions
        self.branch_candidates: List[State] = []

    def _nop(self, offset: int) -> int:
        return offset + 1

    def _acc(self, offset: int, arg: int) -> int:
        self.state.accumulator += arg
        return offset + 1

    def _jmp(self, offset: int, arg: int) -> int:
        return offset + arg

    def _run_next_instruction(self) -> None:
        if self.state.current_offset in self.state.offset_history:
            raise InfiniteLoopException
        self.state.offset_history.append(self.state.current_offset)

        instruction = self.instructions[self.state.current_offset]
        if instruction.operation == Instruction.ACC:
            self.state.current_offset = self._acc(offset=self.state.current_offset, arg=instruction.argument)
        else:
            if instruction.operation == Instruction.JMP:
                if self.state.swap_next:
                    self.state.current_offset = self._nop(offset=self.state.current_offset)
                    self.state.swap_next = False
                else:
                    self.state.current_offset = self._jmp(offset=self.state.current_offset, arg=instruction.argument)
            elif instruction.operation == Instruction.NOP:
                if self.state.swap_next:
                    self.state.current_offset = self._jmp(offset=self.state.current_offset, arg=instruction.argument)
                    self.state.swap_next = False
                else:
                    self.state.current_offset = self._nop(offset=self.state.current_offset)
            else:
                raise ValueError("Unsupported instruction '%s'" % instruction.operation)
            if not self.state.is_clone:
                self.branch_candidates.append(self.state.clone())

    def run_until_loop(self) -> None:
        program_len = len(self.instructions)
        while 0 <= self.state.current_offset < program_len:
            try:
                self._run_next_instruction()
            except InfiniteLoopException:
                if len(self.branch_candidates) > 0:
                    self.state = self.branch_candidates.pop()
                    print(
                        "Changing instruction at offset %d from (%s %d) to (%s %d)" %
                        (self.state.current_offset,
                         self.instructions[self.state.current_offset].operation,
                         self.instructions[self.state.current_offset].argument,
                         self.instructions[self.state.current_offset].counterpart(),
                         self.instructions[self.state.current_offset].argument)
                    )
                else:
                    raise InfiniteLoopException("Unrecoverable infinite loop")
        if not self.state.current_offset == program_len:
            raise RuntimeWarning("Unexpected program termination - expected %d, got %d" % (program_len, self.state.current_offset))


def load(input_path: str) -> List[Instruction]:
    instructions: List[Instruction] = []
    with open(input_path, 'r') as input_file:
        i = 1
        for line in input_file:
            m = PATTERN_INSTRUCTION.match(line)
            if m:
                operation = m.group(GRP_NAME_OPERATION)
                argument = int(m.group(GRP_NAME_ARGUMENT))
                instructions.append(Instruction(operation, argument))
            else:
                raise ValueError("Syntax error on line %d: \n\t%s" % (i, line))
            i += 1
    return instructions


def main() -> None:
    instructions = load("./input.txt")
    automaton = Automaton(instructions)
    automaton.run_until_loop()
    print("Accumulator value before entering loop: %d" % automaton.state.accumulator)


if __name__ == "__main__":
    main()
