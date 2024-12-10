from aoc.lib.matrix import (
    Matrix,
)
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum


test_input = """\
HERE"""


def main():
    #test_input = read_input("aoc/CHANGE/input.txt")
    matrix = Matrix.empty_matrix(5, 5, 0)
    print(matrix)


if __name__ == "__main__":
    main()
