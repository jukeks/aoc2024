from aoc.lib import (
    create_matrix,
    print_matrix,
    parse_matrix,
    Matrix,
    Any,
    filter_out_empty_cells,
    to_int_matrix,
    get_column,
    read_matrix,
)
from collections import defaultdict

test_input = to_int_matrix(
    filter_out_empty_cells(
        parse_matrix(
            """3   4
4   3
2   5
1   3
3   9
3   3
"""
        )
    )
)

real_input = to_int_matrix(
    filter_out_empty_cells(
        read_matrix("./aoc/01/1.input", "   ")))


def main():
    arr1 = sorted(get_column(real_input, 0))
    arr2 = sorted(get_column(real_input, 1))

    occurances1 = defaultdict(int)
    for i in arr1:
        occurances1[i] += 1
    occurances2 = defaultdict(int)
    for i in arr2:
        occurances2[i] += 1

    print(arr1)
    print(arr2)

    similarities = 0
    for i in arr1:
        similarities += occurances2[i] * i

    print(similarities)


if __name__ == "__main__":
    main()
