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
import re

test_input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

pattern = r"mul\((\d+)\,(\d+)\)"
enable_pattern = r"do\(\)"
disable_pattern = r"don\'t\(\)"

RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC = '\033[0m'

def red(s: str) -> str:
    return RED + s + NC

def green(s: str) -> str:
    return GREEN + s + NC

def preprocess(s: str) -> str:
    matches = list(re.finditer(pattern, s))
    start = 0
    output = ""
    for m in matches:
        part = s[start:m.start()]
        
        outpart = ""
        while part:
            match = re.search(enable_pattern, part)
            if not match:
                outpart += part
                break
            outpart += part[:match.start()] + green(part[match.start():match.end()])
            part = part[match.end():]

        part = outpart
        outpart = ""
        while part:
            match = re.search(disable_pattern, part)
            if not match:
                outpart += part
                break
            outpart += part[:match.start()] + red(part[match.start():match.end()])
            part = part[match.end():]
        output += outpart + "\n"


        
        start = m.start()
    return output


def main():
    test_input = read_input("./aoc/03/input.txt")
    nice_input = preprocess(test_input)

    enabled = True
    total = 0
    for match in re.finditer(f"({pattern})|({enable_pattern})|({disable_pattern})", test_input):
        print(match)
        if match.group(0) == "do()":
            enabled = True
        elif match.group(0) == "don't()":
            enabled = False
        else:
            if enabled:
                a = match.group(2)
                b = match.group(3)
                print("doing", match.group())
                total += int(a) * int(b)
            else:
                print("skipping", match.group())
    print("total", total)

if __name__ == "__main__":
    main()
