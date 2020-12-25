from typing import List


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

    def evaluate_new_state(self) -> bool:
        if self.state == Seat.OCCUPIED_SEAT and self.neighbor_cnt >= 4 and self.count_occupied_neighbors() >= 4:
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

    def _iteration(self) -> int:
        changed_seats: List[Seat] = []
        for seat in self.seats:
            if seat.evaluate_new_state():
                changed_seats.append(seat)
        for seat in changed_seats:
            seat.activate_new_state()
        return len(changed_seats)

    def run(self) -> int:
        iterations = 0
        while self._iteration() > 0 and iterations < Lobby.MAX_ITERATIONS:
            iterations += 1
        if iterations >= Lobby.MAX_ITERATIONS:
            raise RuntimeError("Didn't converge in %d iterations" % iterations)
        return iterations

    def count_occupied(self) -> int:
        return sum([(1 if seat.state == Seat.OCCUPIED_SEAT else 0) for seat in self.seats])


def load(input_path: str) -> Lobby:
    plan: List[List[Seat]] = []
    with open(input_path, 'r') as input_file:
        for raw_line in input_file:
            plan.append([])
            line = raw_line.strip()
            for s in line:
                plan[-1].append(Seat(s))

    seats = _interlink_seats(plan)
    return Lobby(plan=plan, seats=seats)


def _interlink_seats(plan):
    seats: List[Seat] = []
    _interlink_inner_seats(plan, seats)
    _interlink_top_row_seats(plan, seats)
    _interlink_bottom_row_seats(plan, seats)
    _interlink_side_seats(plan, seats)
    return seats


def _interlink_side_seats(plan, seats):
    # sides
    for row_idx in range(1, len(plan) - 1):
        seat = plan[row_idx][0]
        if seat.state != Seat.EMPTY_SPACE:
            seats.append(seat)
            neighbors: List[Seat] = []
            for (i, j) in [(row_idx - 1, 0), (row_idx - 1, 1),
                           (row_idx, 1),
                           (row_idx + 1, 0), (row_idx + 1, 1)]:
                _link_neighboring_seat(plan[i][j], neighbors)
            seat.set_neighbors(neighbors)
        seat = plan[row_idx][-1]
        if seat.state != Seat.EMPTY_SPACE:
            seats.append(seat)
            neighbors: List[Seat] = []
            for (i, j) in [(row_idx - 1, -1), (row_idx - 1, -2),
                           (row_idx, -2),
                           (row_idx + 1, -1), (row_idx + 1, -2)]:
                _link_neighboring_seat(plan[i][j], neighbors)
            seat.set_neighbors(neighbors)


def _interlink_bottom_row_seats(plan, seats):
    # bottom row
    for col_idx in range(len(plan[-1])):
        seat = plan[-1][col_idx]
        if seat.state != Seat.EMPTY_SPACE:
            seats.append(seat)
            neighbors: List[Seat] = []
            # left
            if col_idx > 0:
                _link_neighboring_seat(plan[-2][col_idx - 1], neighbors)
                _link_neighboring_seat(plan[-1][col_idx - 1], neighbors)
            # right
            if col_idx < (len(plan[-1]) - 1):
                _link_neighboring_seat(plan[-1][col_idx + 1], neighbors)
                _link_neighboring_seat(plan[-2][col_idx + 1], neighbors)
            _link_neighboring_seat(plan[-2][col_idx], neighbors)
            seat.set_neighbors(neighbors)


def _interlink_top_row_seats(plan, seats):
    # top row
    for col_idx in range(len(plan[0])):
        seat = plan[0][col_idx]
        if seat.state != Seat.EMPTY_SPACE:
            seats.append(seat)
            neighbors: List[Seat] = []
            # left
            if col_idx > 0:
                neighbor = plan[0][col_idx - 1]
                if neighbor.state != Seat.EMPTY_SPACE:
                    neighbors.append(neighbor)
                neighbor = plan[1][col_idx - 1]
                if neighbor.state != Seat.EMPTY_SPACE:
                    neighbors.append(neighbor)
            # right
            if col_idx < (len(plan[0]) - 1):
                _link_neighboring_seat(plan[0][col_idx + 1], neighbors)
                _link_neighboring_seat(plan[1][col_idx + 1], neighbors)
            # directly below
            _link_neighboring_seat(plan[1][col_idx], neighbors)
            seat.set_neighbors(neighbors)


def _interlink_inner_seats(plan, seats):
    for row_idx in range(1, len(plan) - 1):
        row = plan[row_idx]
        for col_idx in range(1, len(row) - 1):
            seat = row[col_idx]
            if seat.state != Seat.EMPTY_SPACE:
                seats.append(seat)
                neighbors: List[Seat] = []
                for (i, j) in [(row_idx - 1, col_idx - 1), (row_idx - 1, col_idx), (row_idx - 1, col_idx + 1),
                               (row_idx, col_idx - 1), (row_idx, col_idx + 1),
                               (row_idx + 1, col_idx - 1), (row_idx + 1, col_idx), (row_idx + 1, col_idx + 1)]:
                    _link_neighboring_seat(plan[i][j], neighbors)
                seat.set_neighbors(neighbors)


def _link_neighboring_seat(neighbor, neighbors):
    if neighbor.state != Seat.EMPTY_SPACE:
        neighbors.append(neighbor)


def main() -> None:
    lobby = load("./input.txt")
    iterations = lobby.run()
    print("Occupied after converging (%d iterations): %d" % (iterations, lobby.count_occupied()))


if __name__ == "__main__":
    main()
