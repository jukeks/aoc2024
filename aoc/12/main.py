from aoc.lib.matrix import (
    Matrix,
    Point,
    neighbor_points,
)
from aoc.lib import (
    read_input,
)
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
import itertools


test_input = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def collect(m: Matrix) -> dict[str, list[Point]]:
    c = defaultdict(list)
    for y, row in enumerate(m):
        for x, cell in enumerate(row):
            c[cell].append((x, y))
    return c


def sort_crop_to_plots(m: Matrix[str], crop: str, points: list[Point]) -> list[list[Point]]:
    pointSet = set(points)
    plots = []

    while pointSet:
        root = pointSet.pop()
        visited = set([root])
        q = [root]
        while q:
            n = q.pop()
            for np in neighbor_points(n):
                if not m.is_inside(np):
                    continue
                if m.get(np) != crop:
                    continue

                if np not in visited:
                    visited.add(np)
                    q.append(np)
        
        for p in visited:
            pointSet.discard(p)
        plots.append(list(visited))

    return plots

class Dir(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def __repr__(self):
        return self.name


def calculate(m: Matrix, crop: str, plot: list[Point]) -> int:
    area = len(plot)
    perimeter = 0

    fence = set()

    for p in plot:
        neighbors = neighbor_points(p)
        for np, dir in zip(neighbors, [Dir.RIGHT, Dir.LEFT, Dir.UP, Dir.DOWN]):
            if not m.is_inside(np):
                perimeter += 1
                fence.add((p, dir))
                continue
            n = m.get(np)
            if n != crop:
                perimeter += 1
                fence.add((p, dir))
                continue


    sides = sort_fence_to_sides(fence)

    print(crop, area, perimeter, len(fence), len(sides))

    return area * len(sides)

def sort_fence_to_sides(fence: set[Point]) -> list[list[Point]]:
    fencePoints = set(fence)
    fence = fence.copy()
    sides = []

    while fencePoints:
        root = fencePoints.pop()
        visited = set([root])
        q = [root]
        while q:
            (x, y), dir = q.pop()
            
            neigbor_point_candidates = []
            if dir in [Dir.UP, Dir.DOWN]:
                # horizontal
                neigbor_point_candidates = [((x-1, y), dir), ((x+1, y), dir)]
            else:
                # vertical
                neigbor_point_candidates = [((x, y-1), dir), ((x, y+1), dir)]

            for np in neigbor_point_candidates:
                if np not in fence:
                    continue

                if np not in visited:
                    visited.add(np)
                    q.append(np)
        
        for p in visited:
            fencePoints.discard(p)
        sides.append(list(visited))

    return sides

def main():
    test_input = read_input("aoc/12/input.txt")
    m: Matrix[str] = Matrix.parse_matrix(test_input, str, "")
    c = collect(m)
    total = 0
    for crop, points in c.items():
        plots = sort_crop_to_plots(m, crop, points)
        for plot in plots:
            t = calculate(m, crop, plot)
            total += t

    print(total)



if __name__ == "__main__":
    main()
