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
from dataclasses import dataclass, field
from enum import Enum
import itertools

test_input = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

class Operator(Enum):
    ADD = "+"
    MULTIPLY = "*"
    CONCAT = "||"

@dataclass
class Equation:
    result: int
    operands: list[int]

    def solve(self) -> int:
        solutions = 0
        for p in itertools.product([Operator.ADD, Operator.MULTIPLY, Operator.CONCAT], repeat=len(self.operands)-1):
            operands = self.operands.copy()
            acc = operands.pop(0)
            for operator in p:
                operand = operands.pop(0)
                if operator == Operator.ADD:
                    acc += operand
                if operator == Operator.MULTIPLY:
                    acc *= operand
                if operator == Operator.CONCAT:
                    acc = int(str(acc) + str(operand))
            if acc == self.result:
                print("solution found!")
                solutions += 1
                break

        return solutions


def main():
    test_input = read_input("aoc/07/input.txt")
    eqs = parse(test_input)
    total = 0
    for eq in eqs:
        print(eq)
        if eq.solve():
            total += eq.result
    print(total)

def parse(text: str) -> list[Equation]:
    eqs = []
    for row in text.splitlines():
        result, operands_raw = row.split(": ")
        operands = operands_raw.split(" ")
        eqs.append(Equation(int(result), [int(o) for o in operands]))

    return eqs

if __name__ == "__main__":
    main()
