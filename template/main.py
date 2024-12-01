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
from dataclasses import dataclass

test_input = """\
HERE"""


def main():
    matrix = create_matrix(5, 5)
    print_matrix(matrix)


if __name__ == "__main__":
    main()
