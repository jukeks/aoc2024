from aoc.lib.matrix import (
    Matrix,
)
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum


test_input = """\
814 1183689 0 1 766231 4091 93836 46"""


def step(stone: int, occurances: int, stones: dict[int, int]) -> None:
    if stone == 0:
        stones[1] += occurances
        return

    s = str(stone)
    if len(s) % 2 == 0:
        half = len(s) // 2
        a, b = int(s[:half]), int(s[half:])
        stones[a] += occurances
        stones[b] += occurances
        return

    stones[stone*2024] += occurances


def print_stones(stones: list[int]) -> None:
    print(" ".join([str(s) for s in stones]))


def main():
    stones = [int(s) for s in test_input.split(" ")]
    print_stones(stones)

    old = {stone: 1 for stone in stones}
    for i in range(1000):
        new = defaultdict(int)
        for stone, occurances in old.items():
            step(stone, occurances, new)

        old = new
        total = 0
        for _stone, occurances in new.items():
            total += occurances
        print("round", i, total, len(new))

if __name__ == "__main__":
    main()
