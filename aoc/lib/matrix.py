from typing import TypeVar, Generic, Generator, Callable
from dataclasses import dataclass

Point = tuple[int, int]

T = TypeVar("T")

ConversionFunc = Callable[[str], T]


class Matrix(Generic[T]):
    def __init__(self, m: list[list[T]], delimiter: str = "") -> None:
        self.m = m
        self.delimiter = delimiter

    def __iter__(self) -> Generator[list[T]]:
        for row in self.m:
            yield row

    def __str__(self) -> str:
        s = ""
        for row in self:
            for cell in row:
                s += str(cell) + self.delimiter
            s += "\n"
        return s[:-1]  # remove last new line

    def __repr__(self) -> str:
        return str(self)

    def get(self, p: Point) -> T:
        x, y = p
        return self.m[y][x]

    def copy(self) -> "Matrix[T]":
        return Matrix(
            [row.copy() for row in self],
            delimiter=self.delimiter,
        )

    def set(self, p: Point, val: T) -> None:
        x, y = p
        self.m[y][x] = val

    def size(self) -> Point:
        return len(self.m[0]), len(self.m)

    def get_column(self, x: int) -> list[T]:
        return [row[x] for row in self]

    def iterate(self) -> Generator[tuple[Point, T]]:
        for y, row in enumerate(self):
            for x, cell in enumerate(row):
                yield (x, y), cell

    def find(self, val: T) -> Point | None:
        for p, t in self.iterate():
            if t == val:
                return p
        return None

    def contains_point(self, p: Point) -> bool:
        x, y = p
        return 0 <= x < len(self.m[0]) and 0 <= y < len(self.m)

    def neighbors(self, p: Point) -> list[T]:
        return [
            self.get(neighbor)
            for neighbor in neighbor_points(p)
            if self.contains_point(neighbor)
        ]

    def neighbors_diagonal(self, p: Point) -> list[T]:
        return [
            self.get(neigbor)
            for neigbor in neighbor_points_diagonal(p)
            if self.contains_point(neigbor)
        ]

    @classmethod
    def parse_matrix(
        cls,
        text: str,
        conversion: ConversionFunc,
        delimiter: str = "",
    ) -> "Matrix[T]":
        splitter = lambda x: x.split(delimiter)
        if delimiter == "" or delimiter is None:
            splitter = lambda x: list(x)

        return Matrix[T](
            [
                [conversion(cell) for cell in splitter(row)]
                for row in text.strip().splitlines()
            ],
            delimiter=delimiter,
        )

    @classmethod
    def empty_matrix(cls, width: int, height: int, init: T) -> "Matrix[T]":
        m = [[init for _ in range(width)] for _ in range(height)]
        return Matrix(m)


def neighbor_points(p: Point) -> list[Point]:
    x, y = p
    return [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]


def neighbor_points_diagonal(p: Point) -> list[Point]:
    # all 8 neighbors: up, down, left, right and diagonals
    x, y = p
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


@dataclass
class Limits:
    min: Point
    max: Point

    def inside(self, p: Point) -> bool:
        x, y = p
        return self.min[0] <= x < self.max[0] and self.min[1] <= y < self.max[1]
