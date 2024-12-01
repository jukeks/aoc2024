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


def parse_matrix(text: str) -> Matrix:
    return [[cell for cell in row] for row in text.strip().splitlines()]


def read_matrix(filename: str) -> Matrix:
    with open(filename) as f:
        return parse_matrix(f.read())


def read_input(filename: str):
    with open(filename) as f:
        return f.read()


from typing import TypeVar

T = TypeVar("T")


def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [item for sublist in list_of_lists for item in sublist]
