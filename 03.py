import re
import sys
from math import prod


def iter_adjacent(adj_to, x):
    # Create a range from +/- 1 clamped to the boundaries of adj_to list
    yield from range(max(x - 1, 0), min(len(adj_to), x + 2))


def check_environment_for_gear(map, x, y):
    found = []
    for adj_x in iter_adjacent(map, x):
        for m in re.finditer(r"(\d+)", map[adj_x]):
            # Check if number is in y-range
            if y in range(m.start() - 1, m.end() + 1):
                found.append(int(m.group()))
    if len(found) == 2:
        return prod(found)
    return None


def check_environment_for_num(map, x, y):
    for adj_x in iter_adjacent(map, x):
        for adj_y in iter_adjacent(map[0], y):
            # Check if value is a symbol
            if map[adj_x][adj_y] != "." and not map[adj_x][adj_y].isnumeric():
                return True


parts = sys.stdin.read().splitlines()
numbers = []
gears = []

for input in enumerate(parts):
    x, line = input

    # Find all numbers in line
    for m in re.finditer(r"(\d+)", line):
        for y in range(*m.span()):
            # Check if a symbol is adjacent
            if check_environment_for_num(parts, x, y):
                numbers.append(int(m.group()))
                break

    # Find all gears in line
    for m in re.finditer(r"\*", line):
        # Check if two numbers are adjacent
        if ratio := check_environment_for_gear(parts, x, m.start()):
            gears.append(ratio)


print(sum(numbers))
print(sum(gears))
