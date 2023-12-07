from sys import stdin

from tools import compose, curry_1, filter_c, map_c


def scores(line: str):
    count = count_winning(line)
    if count == 0:
        return 0
    return pow(2, count - 1)


def count_winning(line):
    line = line.split(":")[1]
    winning, ticket = parse(line)
    return sum(1 for n in ticket if n in winning)


def parse(line) -> list[list[int]]:
    split_str = curry_1(lambda sep, s: s.split(sep))
    return list(
        map(
            compose(str.strip, split_str(" "), filter_c(bool), map_c(int), list),
            line.split("|"),
        )
    )


lines = [r.strip() for r in stdin]


def part1(lines):
    print(sum(scores(r.strip()) for r in lines))


def part2(lines):
    counts = [1 for _ in range(len(lines))]
    wins = list(map(count_winning, lines))
    for i, count in enumerate(wins):
        for n in range(i + 1, i + count + 1):
            counts[n] += counts[i]

    print(sum(counts))


part1(lines)
part2(lines)
