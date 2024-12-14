from aoc.lib import (
    Matrix,
    create_matrix,
    print_matrix,
    parse_matrix,
    neighbor_indexes_diagonal,
    neighbor_coordinate_pairs,
    neighbors,
    read_matrix,
    neighbors_diagonal,
    read_input,
    matrix_get,
    Point,
)
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum


test_input = """\
0123
1234
8765
9876"""

test_input = """\
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""

test_input = """\
..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""

test_input = """\
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01"""

test_input = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

test_input = """\
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9...."""

Path = list[Point]


@dataclass
class Node:
    point: Point
    value: int
    neighbors: list["Node"] = field(default_factory=list)

    def __repr__(self):
        return f"{self.value}"


Map = list[list[Node]]


def parse_nodes(m: Map) -> Map:
    graph: list[list[Node]] = [[None for cell in row] for row in m]
    for y, row in enumerate(m):
        for x, cell in enumerate(row):
            p = (x, y)
            value = int(cell) if cell != "." else "."
            graph[y][x] = Node(p, value)

    for row in graph:
        for node in row:
            if node.value == ".":
                continue
            ns = neighbors(graph, node.point[0], node.point[1])
            for neighbor in ns:
                if neighbor.value == ".":
                    continue
                if neighbor.value - node.value == 1:
                    node.neighbors.append(neighbor)

    return graph


def trailheads(m: Map) -> list[Node]:
    points = []
    for row in m:
        for node in row:
            if node.value == 0:
                points.append(node)

    return points


def bfs(trailhead: Node) -> int:
    q = [trailhead]
    visited = set(trailhead.point)

    nines = 0

    while q:
        node = q.pop(0)
        if node.value == 9:
            nines += 1

        for neighbor in node.neighbors:
            if neighbor.point in visited:
                continue
            visited.add(neighbor.point)
            q.append(neighbor)

    return nines


def find(trailhead: Node) -> list[Path]:
    return find_all_paths([], [], trailhead)


def find_all_paths(paths: list[Path], path: Path, n: Node) -> list[Path]:
    path = path + [n]
    paths = []

    queue = n.neighbors.copy()
    while queue:
        node = queue.pop()
        if node in path:
            continue

        if node.value == 9:
            paths += [path + [node]]
            continue

        found = find_all_paths(paths, path, node)
        if not found:
            continue
        paths += found

    return paths


def main():
    test_input = read_input("aoc/10/input.txt")
    m = parse_matrix(test_input, delimiter="")
    graph = parse_nodes(m)
    print_matrix(graph)

    total = 0
    for head in trailheads(graph):
        total += len(find(head))

    print(total)


if __name__ == "__main__":
    main()
