import math
import re
from typing import List, Tuple


class Instruction:

    GRP_NAME_INSTRUCTION = "instruction"
    GRP_NAME_VALUE = "value"
    PATTERN = re.compile("^\\s*(?P<%s>[NSWELRF])\\s*(?P<%s>\\d+)\\s*$" % (GRP_NAME_INSTRUCTION, GRP_NAME_VALUE))

    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    CW = "R"
    CCW = "L"
    FORWARD = "F"

    def __init__(self, kind: str, value: float):
        self.kind: str = kind
        self.value: float = value

    def __str__(self) -> str:
        return "%s\t%s" % (self.kind, str(self.value))


def get_N_E_increments(azimut_rads: float, radius: float) -> Tuple[float, float]:
    return radius * math.sin(azimut_rads), radius * math.cos(azimut_rads)


class Ship:
    def __init__(self, azimut: float = 0, north: float = 0, east: float = 0):
        self.azimut: float = azimut
        self.north: float = north
        self.east: float = east

    def __str__(self) -> str:
        return "Ship(N=%s, E=%s, @ %s°)" % (
            str(self.north), str(self.east), str(self.azimut)
        )

    def move(self, instruction: Instruction) -> None:
        if instruction.kind == Instruction.NORTH:
            self.north += instruction.value
        elif instruction.kind == Instruction.SOUTH:
            self.north -= instruction.value
        elif instruction.kind == Instruction.EAST:
            self.east += instruction.value
        elif instruction.kind == Instruction.WEST:
            self.east -= instruction.value
        elif instruction.kind == Instruction.CCW:
            self.azimut = (self.azimut + instruction.value) % 360
        elif instruction.kind == Instruction.CW:
            self.azimut = (self.azimut - instruction.value) % 360
        elif instruction.kind == Instruction.FORWARD:
            (n, e) = get_N_E_increments(math.radians(self.azimut), instruction.value)
            self.north += n
            self.east += e

    def sail(self, instructions: List[Instruction]) -> None:
        for instruction in instructions:
            self.move(instruction)

    def get_manhattan_dist(self) -> float:
        return math.fabs(self.north) + math.fabs(self.east)


class Waypoint:
    def __init__(self, north: float = 1, east: float = 10):
        self.north: float = north
        self.east: float = east

    def move_N_S(self, value: float) -> None:
        self.north += value

    def move_E_W(self, value: float) -> None:
        self.east += value

    def rotate(self, degrees: float) -> None:
        # new_heading = self.get_heading_rads() + math.radians(degrees)
        # radius = math.sqrt(self.north**2 + self.east**2)
        # (n, e) = get_N_E_increments(new_heading, radius)
        # self.north += n
        # self.east += e
        d = degrees % 360
        s = math.sin(math.radians(d))
        c = math.cos(math.radians(d))
        (n, e) = (
            (self.east * s) + (self.north * c),
            (self.east * c) - (self.north * s)
        )
        # self.north += n
        # self.east += e
        self.north = n
        self.east = e

    def get_heading_rads(self) -> float:
        return math.atan2(self.north, self.east)

    def __str__(self) -> str:
        return "Waypoint(N=%s, E=%s)" % (self.north, self.east)


class WaypointDrivenShip(Ship):
    def __init__(self, azimut: float = 0, north: float = 0, east: float = 0, waypoint: Waypoint = Waypoint()):
        super().__init__(azimut=azimut, north=north, east=east)
        self.waypoint: Waypoint = waypoint

    def move(self, instruction: Instruction) -> None:
        if instruction.kind == Instruction.NORTH:
            self.waypoint.move_N_S(instruction.value)
        elif instruction.kind == Instruction.SOUTH:
            self.waypoint.move_N_S(-instruction.value)
        elif instruction.kind == Instruction.EAST:
            self.waypoint.move_E_W(instruction.value)
        elif instruction.kind == Instruction.WEST:
            self.waypoint.move_E_W(-instruction.value)
        elif instruction.kind == Instruction.CCW:
            self.waypoint.rotate(instruction.value)
        elif instruction.kind == Instruction.CW:
            self.waypoint.rotate(-instruction.value)
        elif instruction.kind == Instruction.FORWARD:
            # (n, e) = get_N_E_increments(
            #     azimut_rads=self.waypoint.get_heading_rads(),
            #     radius=instruction.value
            # )
            (n, e) = (
                instruction.value * self.waypoint.north,
                instruction.value * self.waypoint.east
            )
            self.north += n
            self.east += e


def load(input_path: str) -> List[Instruction]:
    ret_val: List[Instruction] = []
    with open(input_path, 'r') as input_file:
        for line in input_file:
            m = Instruction.PATTERN.match(line)
            if m:
                inst = m.group(Instruction.GRP_NAME_INSTRUCTION)
                val = float(m.group(Instruction.GRP_NAME_VALUE))
                ret_val.append(Instruction(kind=inst, value=val))
            else:
                print("WARN: invalid line '%s'" % line)
    return ret_val


def main() -> None:
    ship = Ship()
    instructions = load("./input.txt")
    ship.sail(instructions)
    print("Ship sailed to %d" % round(ship.get_manhattan_dist()))
    waypoint_ship = WaypointDrivenShip()
    waypoint_ship.sail(instructions)
    print("Waypoint-driven ship sailed to %d" % round(waypoint_ship.get_manhattan_dist()))


if __name__ == "__main__":
    main()
