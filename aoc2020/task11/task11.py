from typing import List, Tuple


LOG_PROGRESS = True


class Seat:

    FREE_SEAT = "L"
    OCCUPIED_SEAT = "#"
    EMPTY_SPACE = "."

    def __init__(self, state: str):
        self.state: str = state
        self.new_state: str = state
        self.neighbors: List[Seat] = []
        self.neighbor_cnt = 0

    def set_neighbors(self, neighbors: List['Seat'] or None = None) -> None:
        self.neighbors = [] if neighbors is None else neighbors
        self.neighbor_cnt = len(self.neighbors)

    def evaluate_new_state(self, threshold: int) -> bool:
        if self.state == Seat.OCCUPIED_SEAT and self.neighbor_cnt >= threshold and self.count_occupied_neighbors() >= threshold:
            self.new_state = Seat.FREE_SEAT
            return True
        if self.state == Seat.FREE_SEAT and self.count_occupied_neighbors() == 0:
            self.new_state = Seat.OCCUPIED_SEAT
            return True
        return False

    def count_occupied_neighbors(self):
        return sum(
            [(1 if neighbor.state == Seat.OCCUPIED_SEAT else 0) for neighbor in self.neighbors]
        )

    def activate_new_state(self) -> None:
        self.state = self.new_state


class Lobby:

    MAX_ITERATIONS = 1000000

    def __init__(self, plan: List[List[Seat]] or None, seats: List[Seat] or None):
        self.plan: List[List[Seat]] = [] if plan is None else plan
        self.seats: List[Seat] = [] if seats is None else seats

    def _iteration(self, threshold: int) -> int:
        changed_seats: List[Seat] = []
        for seat in self.seats:
            if seat.evaluate_new_state(threshold):
                changed_seats.append(seat)
        for seat in changed_seats:
            seat.activate_new_state()
        n = len(changed_seats)
        log(n)
        return n

    def run(self, threshold: int = 4) -> int:
        iterations = 0
        while self._iteration(threshold) > 0 and iterations < Lobby.MAX_ITERATIONS:
            iterations += 1
        if iterations >= Lobby.MAX_ITERATIONS:
            raise RuntimeError("Didn't converge in %d iterations" % iterations)
        return iterations

    def count_occupied(self) -> int:
        return sum([(1 if seat.state == Seat.OCCUPIED_SEAT else 0) for seat in self.seats])

    def __str__(self) -> str:
        return "\n".join(
            ["".join([seat.state for seat in row]) for row in self.plan]
        )


def log(n: int) -> None:
    if LOG_PROGRESS:
        print(n)


def load(input_path: str, radius: int = 1) -> Lobby:
    plan: List[List[Seat]] = []
    with open(input_path, 'r') as input_file:
        for raw_line in input_file:
            plan.append([])
            line = raw_line.strip()
            for s in line:
                plan[-1].append(Seat(s))

    seats = _interlink_neighboring_seats(plan, radius)
    print("Lobby loaded")
    return Lobby(plan=plan, seats=seats)


def _interlink_neighboring_seats(plan, radius: int = 1) -> List[Seat]:
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    seats: List[Seat] = []
    for row_idx in range(len(plan)):
        for col_idx in range(len(plan[row_idx])):
            seat = plan[row_idx][col_idx]
            if seat.state != Seat.EMPTY_SPACE:
                neighbors: List[Seat] = []
                for direction in directions:
                    _find_neighboring_seat_in_direction(
                        start=(row_idx, col_idx),
                        direction=direction,
                        radius=radius,
                        plan=plan,
                        neighbors=neighbors
                    )
                seat.set_neighbors(neighbors)
                seats.append(seat)
    return seats


def _find_neighboring_seat_in_direction(
        start: Tuple[int, int],
        direction: Tuple[int, int],
        radius: int,
        plan: List[List[Seat]],
        neighbors: List[Seat]
) -> None:
    max_row = len(plan)
    max_column = len(plan[0])
    position: Tuple[int, int] = (start[0] + direction[0], start[1] + direction[1])
    r = 1
    while 0 <= position[0] < max_row and 0 <= position[1] < max_column and \
            plan[position[0]][position[1]].state == Seat.EMPTY_SPACE and \
            (radius < 0 or r < radius):
        position = (position[0] + direction[0], position[1] + direction[1])
        r += 1
    if 0 <= position[0] < max_row and 0 <= position[1] < max_column and \
            plan[position[0]][position[1]].state != Seat.EMPTY_SPACE:
        neighbors.append(plan[position[0]][position[1]])


def main() -> None:
    radius = 1
    lobby = load("./input.txt", radius)
    iterations = lobby.run()
    print("Occupied after converging (%d iterations, radius: %d): %d" % (iterations, radius, lobby.count_occupied()))
    radius = -1
    lobby = load("./input.txt", radius)
    iterations = lobby.run(5)
    print("Occupied after converging (%d iterations, radius: %d): %d" % (iterations, radius, lobby.count_occupied()))


if __name__ == "__main__":
    main()
