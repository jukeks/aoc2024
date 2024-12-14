from aoc.lib import (
    Matrix,
    create_matrix,
    print_matrix,
    parse_matrix,
    neighbor_indexes_diagonal,
    read_matrix,
    neighbors_diagonal,
    read_input,
)
from dataclasses import dataclass, field
from enum import Enum

test_input = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

GUARD = "^"
OBSTRUCTION = "#"
EMPTY = "."


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __repr__(self):
        if self == Direction.UP:
            return "^"
        if self == Direction.RIGHT:
            return ">"
        if self == Direction.DOWN:
            return "v"
        if self == Direction.LEFT:
            return "<"

    def __str__(self):
        if self == Direction.UP:
            return "^"
        if self == Direction.RIGHT:
            return ">"
        if self == Direction.DOWN:
            return "v"
        if self == Direction.LEFT:
            return "<"


@dataclass
class Map:
    matrix: Matrix


@dataclass
class Guard:
    x: int
    y: int
    facing: Direction
    history: set[tuple[int, int]] = field(default_factory=set)
    visited: set[tuple[int, int, Direction]] = field(default_factory=set)

    def step(self, map: Map) -> bool:
        self.history.add((self.x, self.y))
        self.visited.add((self.x, self.y, self.facing))

        while not self.about_to_leave(map) and self.is_obstacle(map):
            self.facing = Direction((self.facing.value + 1) % 4)

        self.x, self.y = self.next_coordinate()

        return self.about_to_leave(map) or self.is_obstacle(map)

    def has_left(self, m: Map) -> bool:
        return self.out_of_bounds(self.x, self.y, m)

    def has_visited_before(self) -> bool:
        # in a loop
        return (self.x, self.y, self.facing) in self.visited

    def out_of_bounds(self, x: int, y: int, m: Map) -> bool:
        return x < 0 or y < 0 or y > len(m.matrix) - 1 or x > len(m.matrix[0]) - 1

    def next_coordinate(self) -> tuple[int, int]:
        d = self.facing
        x = self.x
        y = self.y
        match d:
            case Direction.UP:
                return (x, y - 1)
            case Direction.RIGHT:
                return (x + 1, y)
            case Direction.DOWN:
                return (x, y + 1)
            case Direction.LEFT:
                return (x - 1, y)

    def is_obstacle(self, m: Map) -> bool:
        x, y = self.next_coordinate()
        return m.matrix[y][x] in (OBSTRUCTION, "O")

    def about_to_leave(self, m: Map) -> bool:
        x, y = self.next_coordinate()
        return self.out_of_bounds(x, y, m)


def parse(text: str) -> tuple[Guard, Map]:
    m = parse_matrix(text, "")
    for j, row in enumerate(m):
        for i, cell in enumerate(row):
            if cell == "^":
                g = Guard(i, j, Direction.UP)
                m = parse_matrix(text, "", lambda x: x if x != "^" else ".")
                return g, Map(m)


def print_state(g: Guard, m: Map) -> None:
    for j, row in enumerate(m.matrix):
        for i, cell in enumerate(row):
            if (i, j) == (g.x, g.y):
                cell = g.facing
            print(cell, end="")
        print()


def print_visited(g: Guard, m: Map) -> None:
    for j, row in enumerate(m.matrix):
        for i, cell in enumerate(row):
            if (i, j) in g.history:
                cell = "X"
            print(cell, end="")
        print()


def main():
    test_input = read_input("aoc/06/input.txt")
    g, m = parse(test_input)
    start_x, start_y = (g.x, g.y)
    print(g)
    print_state(g, m)

    while not g.has_left(m):
        hit_wall = g.step(m)
        if hit_wall:
            print("hit wall")
            print_state(g, m)

    print("left area")
    print()
    print_visited(g, m)
    print("visited:", len(g.history))

    # part 2
    _, template = parse(test_input)
    loops = 0
    for i, j in g.history:
        cell = template.matrix[j][i]
        if cell == OBSTRUCTION or (i, j) == (start_x, start_y):
            continue
        g, m = parse(test_input)
        m.matrix[j][i] = "O"

        while not g.has_left(m):
            g.step(m)
            if g.has_visited_before():
                print("loop found", i, j)
                loops += 1
                break

    print("loops", loops)


if __name__ == "__main__":
    main()
