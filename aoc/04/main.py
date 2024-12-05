from aoc.lib import (
    Matrix,
    create_matrix,
    print_matrix,
    parse_matrix,
    read_matrix,
    read_input,
)
from dataclasses import dataclass

test_input = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def candidate_indexes(x: int, y: int) -> list[list[tuple[int, int]]]:
    horizontal = [(x + i, y) for i in range(4)]
    vertical = [(x, y + j) for j in range(4)]
    diagonal = [(x + i, y + i) for i in range(4)]
    other_diagonal = [(x - i, y + i) for i in range(4)]

    return [
        horizontal,
        vertical,
        diagonal,
        other_diagonal,
        list(reversed(horizontal)),
        list(reversed(vertical)),
        list(reversed(diagonal)),
        list(reversed(other_diagonal)),
    ]

def candidate_indexes2(x: int, y: int) -> list[list[tuple[int, int]]]:
    diagonal = [(x - 1 + i, y - 1 + i) for i in range(3)]
    other_diagonal = [(x + 1 - i, y - 1 + i) for i in range(3)]
    return [
        diagonal,
        other_diagonal,
    ]

def candidates(m: Matrix, x: int, y: int) -> list[list[tuple]]:
    results = []
    cs = candidate_indexes(x, y)
    for candidate in cs:
        ok = True
        for (i, j) in candidate:
            if i < 0 or j < 0 or i >= len(m[0]) or j >= len(m):
                ok = False
                break
        if not ok:
            continue

        s = "".join([m[j][i] for (i, j) in candidate])
        if s == "XMAS":
            results.append(tuple(candidate))
    return results

def is_xmas(m: Matrix, x: int, y: int) -> bool:
    ok = ["MAS", "SAM"]
    diagonal_indexes, other_diagonal_indexes = candidate_indexes2(x, y)

    diagonal = "".join([m[j][i] for (i, j) in diagonal_indexes])
    other_diagonal = "".join([m[j][i] for (i, j) in other_diagonal_indexes])
    return diagonal in ok and other_diagonal in ok

def main():
    matrix = parse_matrix(test_input, "")
    matrix = read_matrix("./aoc/04/input.txt", "")
    print_matrix(matrix)
    print()

    contains = set()
    results = set()
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            res = candidates(matrix, x, y)
            if res:
                for candidate in res:
                    contains.update(candidate)
                    results.add(candidate)

    print(contains)
    print(results)

    xmasses = 0
    for y in range(1, len(matrix) - 1):
        for x in range(1, len(matrix[0]) - 1):
            if is_xmas(matrix, x, y):
                xmasses +=1

    print("results:", len(results))
    print("xmasses:", xmasses)


if __name__ == "__main__":
    main()
