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
from collections import defaultdict

test_input = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

@dataclass
class Rule:
    a: int
    b: int

def parse_rule(row: str) -> Rule:
    a, b = row.split("|")
    return Rule(int(a), int(b))

@dataclass
class Update:
    pages: list[int]

def parse_update(row: str) -> Update:
    pages = row.split(",")
    return Update([int(p) for p in pages])

def parse(text: str) -> tuple[list[Rule], list[Update]]:
    updates = []
    rules = []

    rules_done = False
    for row in text.splitlines():
        if not row:
            rules_done = True
            continue

        if rules_done:
            updates.append(parse_update(row))
        else:
            rules.append(parse_rule(row))

    return rules, updates

@dataclass
class Rulebook:
    rules: list[Rule]
    is_before_mapper: dict[int, set[int]]
    is_after_mapper: dict[int, set[int]]

    def is_before(self, a: int, b: int) -> bool:
        return b in self.is_before_mapper[a]
    
    def is_after(self, a: int, b:int) -> bool:
        return a in self.is_before_mapper[b]
    
    def find_first(self, update: list[int]) -> tuple[int, list[int]]:
        for i in range(len(update)):
            rotated = [update[i]] + update[:i] + update[i+1:]

            ok = True
            for after_page in rotated[1:]:
                if not self.is_before(update[i], after_page):
                    ok = False
                    break

            if ok:
                return rotated[0], rotated[1:]
            
        raise RuntimeError("wtf")

    @classmethod
    def from_rules(cls, rules: list[Rule]) -> 'Rulebook':
        is_before_mapper = defaultdict(set)
        is_after_mapper = defaultdict(set)
        for rule in rules:
            is_before_mapper[rule.a].add(rule.b)
            is_after_mapper[rule.b].add(rule.a)

        return Rulebook(rules=rules, 
                        is_before_mapper=is_before_mapper, 
                        is_after_mapper=is_after_mapper)


def update_is_correct(update: list[int], rulebook: Rulebook) -> bool:
    for i, page in enumerate(update):
        for after_page in update[i+1:]:
            if not rulebook.is_before(page, after_page):
                print("here1")
                return False
        for before_page in update[:i]:
            if not rulebook.is_after(page, before_page):
                print("here2")
                return False
            
    return True

def correct(update: Update, rulebook: Rulebook) -> Update:
    new = []
    pages = update.pages.copy()
    while pages:
        next_page, pages = rulebook.find_first(pages)
        new.append(next_page)

    return Update(new)


def main():
    test_input = read_input("aoc/05/input.txt")
    rules, updates = parse(test_input)
    rulebook = Rulebook.from_rules(rules)

    total = 0
    corrected_total = 0
    for update in updates:
        if update_is_correct(update.pages, rulebook):
            print(update, "is correct")
            middle = update.pages[len(update.pages)//2]
            print("middle is", middle)
            total += middle
        else:
            print(update, "was incorrect")
            corrected = correct(update, rulebook)
            print(correct, "is now corrected")
            middle = corrected.pages[len(corrected.pages)//2]
            print("middle is", middle)
            corrected_total += middle
    print("total", total)
    print("corrected_total", corrected_total)


if __name__ == "__main__":
    main()
