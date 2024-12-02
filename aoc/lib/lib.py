from typing import Any

Matrix = list[list[Any]]


def create_matrix(width: int, height: int, init: Any = None) -> Matrix:
    return [[init for _ in range(width)] for _ in range(height)]


def neighbor_indexes(x: int, y: int) -> list[tuple[int, int]]:
    return [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]


def neighbor_indexes_diagonal(x: int, y: int) -> list[tuple[int, int]]:
    # all 8 neighbors, up, down, left, right and diagonals
    return [
        (x - 1, y - 1),
        (x + 0, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x + 0, y + 1),
        (x + 1, y + 1),
    ]


def neighbors(matrix: Matrix, x: int, y: int) -> list[int]:
    return [
        matrix[j][i]
        for i, j in neighbor_indexes(x, y)
        if 0 <= j < len(matrix) and 0 <= i < len(matrix[0])
    ]


def neighbors_diagonal(matrix: Matrix, x: int, y: int) -> list[int]:
    return [
        matrix[j][i]
        for i, j in neighbor_indexes_diagonal(x, y)
        if 0 <= j < len(matrix) and 0 <= i < len(matrix[0])
    ]


def print_matrix(matrix: Matrix):
    for row in matrix:
        for cell in row:
            print(cell, end="")
        print()


def parse_matrix(text: str, delimiter: str = " ") -> Matrix:
    return [[cell for cell in row.split(delimiter)] for row in text.strip().splitlines()]


def read_matrix(filename: str, delimiter: str = " ") -> Matrix:
    with open(filename) as f:
        return parse_matrix(f.read(), delimiter)


def filter_out_empty_cells(m: Matrix) -> Matrix:
    new_m = list()
    for row in m:
        new_row = list()
        for cell in row:
            if cell.strip() != "":
                new_row.append(cell)
        new_m.append(new_row)
    return new_m


def to_int_matrix(m: Matrix) -> Matrix:
    new_m = list()
    for row in m:
        new_row = [int(cell) for cell in row]
        new_m.append(new_row)
    return new_m


def read_input(filename: str):
    with open(filename) as f:
        return f.read()

def get_column(m: Matrix, i: int) -> list[any]:
    col = list()
    for r in m:
        col.append(r[i])
    return col

from typing import TypeVar

T = TypeVar("T")


def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [item for sublist in list_of_lists for item in sublist]
