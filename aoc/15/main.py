from aoc.lib.matrix import (
    Matrix,
    Point,
)
from aoc.lib import read_input
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
import enum


test_input = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


class Move(enum.StrEnum):
    Left = "<"
    Down = "v"
    Right = ">"
    Up = "^"

    def __repr__(self) -> str:
        return self.value

    def next_point(self, p: Point) -> Point:
        x, y = p
        match self:
            case Move.Left:
                return x - 1, y
            case Move.Right:
                return x + 1, y
            case Move.Up:
                return x, y - 1
            case Move.Down:
                return x, y + 1


def print_map(m: Matrix[str], bot: Point) -> None:
    for p, cell in m.iterate():
        if p[0] == 0:
            if p[1] != 0:
                print()

        if p == bot:
            print("\033[1m@\033[0m", end="")
        else:
            print(cell, end="")

    print()
    print()


def parse(text: str) -> tuple[Matrix[str], list[Move]]:
    m, moves = text.split("\n\n")
    return Matrix.parse_matrix(m, str, ""), [Move(s) for s in moves.replace("\n", "")]


Box = tuple[Point, Point]


def has_space_to_move(m: Matrix[str], box: Box, move: Move) -> tuple[bool, list[Box]]:
    if move not in [Move.Down, Move.Up]:
        raise RuntimeError("just wrong")

    boxes = []
    for box_p in box:
        has_space = False
        behind_p = move.next_point(box_p)
        behind = m.get(behind_p)
        while behind != "#":
            if behind == ".":
                has_space = True
                break

            if behind == "[":
                new_box = (behind_p, (behind_p[0] + 1, behind_p[1]))
            elif behind == "]":
                new_box = ((behind_p[0] - 1, behind_p[1]), behind_p)
            else:
                raise RuntimeError("my bad")

            has_space, new_boxes = has_space_to_move(m, new_box, move)
            if not has_space:
                return False, []
            boxes.append(new_box)
            boxes += new_boxes
            break

        if not has_space:
            return False, []

    return True, boxes


def step(m: Matrix[str], bot: Point, move: Move) -> tuple[Matrix[str], Point]:
    new_p = move.next_point(bot)
    new_tile = m.get(new_p)
    if new_tile == ".":
        # empty
        return m, new_p
    if new_tile == "#":
        # can't move
        return m, bot
    if new_tile == "O":
        # is empty before wall
        has_space = False
        behind_p = move.next_point(new_p)
        behind = m.get(behind_p)
        while behind != "#":
            if behind == ".":
                has_space = True
                break
            behind_p = move.next_point(behind_p)
            behind = m.get(behind_p)

        if not has_space:
            # no move
            return m, bot

        m.set(behind_p, "O")
        m.set(new_p, ".")

        return m, new_p

    if move in "<>" and new_tile in "[]":
        # is empty before wall
        has_space = False
        behind_p = move.next_point(new_p)
        behind = m.get(behind_p)
        while behind != "#":
            if behind == ".":
                has_space = True
                break
            behind_p = move.next_point(behind_p)
            behind = m.get(behind_p)

        if not has_space:
            # no move
            return m, bot

        # move all boxes
        last_point = behind_p
        if bot[0] > last_point[0]:
            # bot is right of point
            step_amount = 1
        else:
            step_amount = -1

        while last_point != bot:
            print(last_point, bot)
            previous_point = (last_point[0] + step_amount, last_point[1])
            m.set(last_point, m.get(previous_point))
            m.set(previous_point, ".")
            last_point = previous_point

        return m, new_p

    if move in "v^" and new_tile in "[]":
        if new_tile == "[":
            new_box = (new_p, (new_p[0] + 1, new_p[1]))
        elif new_tile == "]":
            new_box = ((new_p[0] - 1, new_p[1]), new_p)

        has_space, boxes = has_space_to_move(m, new_box, move)
        if not has_space:
            return m, bot

        boxes.append(new_box)
        for box in boxes:
            for point in box:
                m.set(point, ".")
        for box in boxes:
            m.set(move.next_point(box[0]), "[")
            m.set(move.next_point(box[1]), "]")

        return m, new_p

    print(
        move,
        new_tile,
        move in "v^",
    )
    raise RuntimeError("what")


def checksum(m: Matrix[str]) -> int:
    total = 0
    for (x, y), val in m.iterate():
        if val == "[":
            total += y * 100 + x
    return total


def widen(m: Matrix[str]) -> "Matrix[str]":
    new_rows = []
    new_row = []
    for row in m:
        for cell in row:
            if cell == "#":
                new_row += ["#", "#"]
            if cell == ".":
                new_row += [".", "."]
            if cell == "O":
                new_row += ["[", "]"]
        new_rows.append(new_row)
        new_row = []

    return Matrix(
        m=new_rows,
        delimiter=m.delimiter,
    )


def main():
    test_input = read_input("aoc/15/input.txt")

    m, moves = parse(test_input)
    bot = m.find("@")
    m.set(bot, ".")
    print("initial state:")
    print_map(m, bot)
    m = widen(m)
    bot = (bot[0] * 2, bot[1])
    print_map(m, bot)

    for move in moves:
        #print("move:", move)
        m, bot = step(m, bot, move)
        #print_map(m, bot)
    print("checksum", checksum(m))


if __name__ == "__main__":
    main()
