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
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

def row_is_safe(row: list[int]) -> bool:
    increasing = all_increasing(row)
    decreasing = all_decreasing(row)
    if not increasing and not decreasing:
        return False


    last = row[0]
    for cell in row[1:]:
        diff = abs(last - cell)
        if diff == 0:
            return False
        if diff > 3:
            return False
        last = cell
    return True

def all_increasing(row: list[int]) -> bool:
    last = row[0]
    for cell in row[1:]:
        if last >= cell:
            return False
        last = cell
    return True

def all_decreasing(row: list[int]) -> bool:
    last = row[0]
    for cell in row[1:]:
        if last <= cell:
            return False
        last = cell
    return True

def dampen(row: list[int]):
    if row_is_safe(row):
        return True

    for i in range(len(row)):
        dampened_row = row[:i] + row[i+1:]
        if row_is_safe(dampened_row):
            return True
    
    return False


def main():
    matrix = parse_matrix(test_input, " ", conversion=int)
    matrix = read_matrix("./aoc/02/input.txt", " ", conversion=int)

    print_matrix(matrix)


    safe = 0
    for i, row in enumerate(matrix):
        if dampen(row):
            safe += 1

    print(safe)


if __name__ == "__main__":
    main()
