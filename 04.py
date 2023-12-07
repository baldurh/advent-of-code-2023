import sys
from functools import lru_cache

from tools import compose, fork, map_c, pipe, re_split, spread, str_split


def calculate_card(line):
    numbers = line.split(": ")[1]
    winning_numbers, my_numbers = pipe(
        numbers,
        str_split(" | "),
        map_c(
            compose(
                str.strip,
                re_split(r"\s+"),
                map_c(int),
                set,
            )
        ),
    )
    return len(winning_numbers & my_numbers)


part_1 = compose(
    map_c(
        lambda x: pow(2, x - 1) if x else 0,
    ),
    sum,
)


def part_2(results):
    @lru_cache
    def result(head, tail):
        tail = eval(tail)
        if head == 0:
            return 1
        return 1 + sum([result(tail[x], str(tail[x + 1 :])) for x in range(head)])

    return sum([result(x[1], str(results[x[0] :])) for x in enumerate(results, 1)])


pipe(
    sys.stdin.read().splitlines(),
    map_c(calculate_card),
    list,
    fork(
        part_1,
        part_2,
    ),
    spread(print),
)
