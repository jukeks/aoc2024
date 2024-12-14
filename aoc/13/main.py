from aoc.lib.matrix import (
    Matrix, Point,
)
from aoc.lib import read_input
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
import itertools


test_input = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

@dataclass
class Machine:
    a: Point
    b: Point
    target: Point

    @classmethod
    def from_txt(cls, txt: str) -> 'list[Machine]':
        def split_button(s: str) -> Point:
            x, y = s.split(", ")
            x = x.replace("X", "")
            y = y.replace("Y", "")
            return int(x), int(y)
        
        def split_target(s: str) -> Point:
            x, y = s.split(", ")
            x = x.replace("X=", "")
            y = y.replace("Y=", "")
            return int(x), int(y)

        machines = []
        for batch in itertools.batched(txt.splitlines(), 4):
            _, a = batch[0].split(":")
            _, b = batch[1].split(":")
            _, t = batch[2].split(":")

            machines.append(
                Machine(
                    a=split_button(a),
                    b=split_button(b),
                    target=split_target(t)
                )
            )
        return machines

    

    def limits(self) -> int:
        ax, ay = self.a
        bx, by = self.b
        tx, ty = self.target
        return 100

        return max(
            tx//ax,
            ty//ay,
            tx//bx,
            ty//by,
        )

def minimize(m: Machine) -> int:
    limit = m.limits()

    default = 10000000000000
    smallest = default
    for a_count in range(limit):
        for b_count in range(limit):

            x = a_count*m.a[0] + b_count*m.b[0]
            y = a_count*m.a[1] + b_count*m.b[1]

            #print("trying", a_count, b_count, x, y)

            if m.target == (x, y):
                cost = 3 * a_count + b_count
                if cost < smallest:
                    smallest = cost
    if smallest == default:
        return None
    return smallest

def solve(m: Machine) -> int:
    ax, ay = m.a
    bx, by = m.b
    X, Y = m.target
    X += 10000000000000
    Y += 10000000000000

    B = (ay * X - ax * Y) // (bx * ay - by * ax)
    A = (X - bx * B) // ax

    if A * ax + B * bx != X or A * ay + B * by != Y:
        return None
    
    return 3*A + B


def main():
    test_input = read_input("aoc/13/input.txt")
    machines = Machine.from_txt(test_input)
    total = 0
    for machine in machines:
        print(machine)
        #cost1 = minimize(machine)
        cost2 = solve(machine)
        #print(cost1, cost2)
        if cost2:
            total += cost2
    print(total)


if __name__ == "__main__":
    main()
