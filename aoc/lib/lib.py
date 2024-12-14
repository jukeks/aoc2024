from typing import TypeVar

T = TypeVar("T")


def read_input(filename: str):
    with open(filename) as f:
        return f.read()


def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [item for sublist in list_of_lists for item in sublist]
