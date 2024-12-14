from aoc.lib import (
    Matrix,
    create_matrix,
    print_matrix,
    parse_matrix,
    neighbor_indexes_diagonal,
    read_matrix,
    neighbors_diagonal,
    read_input,
    point_in_matrix,
    coordinate_in_matrix,
)
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from itertools import permutations

Point = tuple[int, int]

test_input = """\
##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##"""


def point_from(a: Point, b: Point) -> Point:
    ax, ay = a
    bx, by = b
    dx = ax - bx
    dy = ay - by

    return ax + dx, ay + dy


def main():
    test_input = read_input("aoc/08/input.txt")
    matrix = parse_matrix(test_input, "", conversion=lambda x: "." if x == "#" else x)

    antennas = defaultdict(list)
    for j, row in enumerate(matrix):
        for i, cell in enumerate(row):
            if cell == ".":
                continue
            antennas[cell].append((i, j))

    antinodes = set()
    for freq, locations in antennas.items():
        for a, b in permutations(locations, 2):
            antinodes.add(a)
            antinodes.add(b)
            points = set([a, b])
            last_size = -1
            while len(points) != last_size:
                last_size = len(points)
                for new_a, new_b in permutations(points, 2):
                    x, y = point_from(new_a, new_b)
                    if not coordinate_in_matrix(matrix, x, y):
                        continue
                    if matrix[y][x] in ("#", "."):
                        matrix[y][x] = "#"
                    antinodes.add((x, y))
                    points.add((x, y))

    print_matrix(matrix)
    print(len(antinodes))


if __name__ == "__main__":
    main()
