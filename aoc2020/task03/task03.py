from typing import Tuple, List

FREE = "."
OBSTACLE = "#"


class TerrainMap:

    def __init__(self, terrain: List[str]):
        self.terrain = terrain
        self.width = len(terrain[0])
        self.height = len(terrain)

    def evaluate_slope(self, direction: Tuple[int, int], start: Tuple[int, int] = (0, 0)) -> int:
        current = start
        obstacles = 0
        while current[0] < self.height:
            if self.terrain[current[0]][current[1]] == OBSTACLE:
                obstacles += 1
            current = (current[0] + direction[0], (current[1] + direction[1]) % self.width)
        return obstacles


def load(input_path: str) -> TerrainMap:
    terrain: List[str] = []
    with open(input_path, 'r') as input_file:
        for line in input_file:
            terrain.append(line.strip())
    return TerrainMap(terrain)


def main() -> None:
    terrain = load("./input.txt")
    direction = (1, 3)
    obstacles = terrain.evaluate_slope(direction)
    log_encountered_obstacles(direction, obstacles)

    product = obstacles
    direction = (1, 1)
    obstacles = terrain.evaluate_slope(direction)
    log_encountered_obstacles(direction, obstacles)
    product *= obstacles

    direction = (1, 5)
    obstacles = terrain.evaluate_slope(direction)
    log_encountered_obstacles(direction, obstacles)
    product *= obstacles

    direction = (1, 7)
    obstacles = terrain.evaluate_slope(direction)
    log_encountered_obstacles(direction, obstacles)
    product *= obstacles

    direction = (2, 1)
    obstacles = terrain.evaluate_slope(direction)
    log_encountered_obstacles(direction, obstacles)
    product *= obstacles

    print("The product is %d" % product)


def log_encountered_obstacles(direction, obstacles):
    print("Trees encountered [%d, %d]: %d" % (direction[0], direction[1], obstacles))


if __name__ == "__main__":
    main()
