from aoc.lib.matrix import (
    Matrix,
    Point,
    Limits,
)
from aoc.lib import read_input
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum


test_input = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


@dataclass
class Robot:
    p: Point
    v: Point

    @classmethod
    def from_text(cls, txt: str) -> list["Robot"]:
        robots = []
        for line in txt.splitlines():
            p_raw, v_raw = line.split(" ")
            px, py = p_raw.replace("p=", "").split(",")
            vx, vy = v_raw.replace("v=", "").split(",")
            robots.append(
                Robot(
                    p=(int(px), int(py)),
                    v=(int(vx), int(vy)),
                )
            )
        return robots

    def step(self, size: Point, count: int = 1) -> "None":
        px, py = self.p
        vx, vy = self.v
        w, h = size

        px = (px + vx * count) % w
        py = (py + vy * count) % h

        self.p = (px, py)


def str_map(robots: list[Robot], size: Point):
    w, h = size
    rm = defaultdict(int)
    for r in robots:
        rm[r.p] += 1
    s = ""
    for y in range(h):
        for x in range(w):
            s += str(rm.get((x, y), " "))
        s += "\n"
    return s[:-1]


def print_map(i: int, robots: list[Robot], size: Point):
    print("iteration:", i)
    print(str_map(robots, size))


def safety_factor(robots: list[Robot], size: Point) -> int:
    w, h = size

    horizontal_cutoff = h // 2
    vertical_cutoff = w // 2

    quadrants = defaultdict(int)

    for r in robots:
        x = -1
        y = -1
        if r.p[0] < vertical_cutoff:
            x = 0
        if r.p[0] > vertical_cutoff:
            x = 1
        if r.p[1] < horizontal_cutoff:
            y = 0
        if r.p[1] > horizontal_cutoff:
            y = 1
        if x == -1 or y == -1:
            continue
        quadrants[(x, y)] += 1

    print(quadrants)
    acc = 1
    for q in quadrants.values():
        acc *= q
    return acc


def horizontal_score(robots: list[Robot], size: Point) -> int:
    middle = size[0] / 2

    acc = 0
    for r in robots:
        from_middle = middle - abs(r.p[0] - middle)
        acc += from_middle
    return acc


def main():
    test_input = read_input("aoc/14/input.txt")
    robots = Robot.from_text(test_input)
    size = (101, 103)
    print_map(0, robots, size)
    print()

    for i in range(10000):
        for r in robots:
            r.step(size)
        score = horizontal_score(robots, size)
        s = str_map(robots, size)
        if "1    111111111111111111111    1" in s:
            print_map(i, robots, size)
            break
    print("safety", safety_factor(robots, size))


if __name__ == "__main__":
    main()
