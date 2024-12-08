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
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum


test_input = """\
HERE"""


def main():
    #test_input = read_input("aoc/CHANGE/input.txt")
    matrix = create_matrix(5, 5)
    print_matrix(matrix)


if __name__ == "__main__":
    main()
