from typing import List


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

class Automaton:
    def __init__(self, instructions: List[Instruction]):
        self.accumulator: int = 0
        self.executed_instructions: List[int] = []
        self.instructions = instructions

    def nop(self, offset: int) -> int:
        return offset + 1

    def acc(self, offset: int, arg: int) -> int:
        self.accumulator += arg
        return offset + 1

    def jmp(self, offset: int, arg: int) -> int:
        return offset + arg

    def run_instruction(self, offset: int) -> int:
        if offset in self.executed_instructions:
            raise InfiniteLoopException

        self.executed_instructions.append(offset)
        instruction = self.instructions[offset]
        if instruction.operation == Instruction.ACC:
            return self.acc(offset=offset, arg=instruction.argument)
        elif instruction.operation == Instruction.JMP:
            return self.jmp(offset=offset, arg=instruction.argument)
        elif instruction.operation == Instruction.NOP:
            return self.nop(offset=offset)
        else:
            raise ValueError("Unsupported instruction '%s'" % instruction.operation)

    def run_until_loop(self) -> None:
        offset = 0
        try:
            while 0 <= offset < len(self.instructions):
                offset = self.run_instruction(offset)
        except InfiniteLoopException:
            return

