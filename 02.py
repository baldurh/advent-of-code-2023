import operator
import sys
from collections import defaultdict

from tools import (
    compose,
    each_c,
    fork,
    getitem,
    identity,
    map_c,
    pipe,
    reduce_c,
    split,
    spread,
    str_split,
)

RULES = {"red": 12, "green": 13, "blue": 14}


def parse_game(input: str):
    return pipe(
        input,
        str_split(": "),
        spread(
            split(
                compose(
                    str_split(" "),
                    getitem(1),
                    int,
                ),
                compose(
                    str_split("; "),
                    map_c(
                        compose(
                            str_split(", "),
                            map_c(
                                compose(
                                    str_split(" "),
                                    spread(split(int, identity)),
                                    tuple,
                                )
                            ),
                            list,
                        )
                    ),
                    list,
                ),
            ),
        ),
        tuple,
    )


def check_rules(draw: tuple[int, str]):
    return RULES[draw[1]] >= draw[0]


def run_game_1(game: tuple[int, list[list[tuple[int, str]]]]):
    return pipe(
        game,
        spread(
            split(
                identity,
                compose(
                    map_c(
                        reduce_c(lambda acc, x: bool.__and__(acc, check_rules(x)), True)
                    ),
                    list,
                    reduce_c(bool.__and__, True),
                ),
            )
        ),
        spread(lambda id, possible: id if possible else 0),
    )


def store_highest():
    highest = defaultdict(lambda: 0)

    def check_highest(draw: list[tuple[int, str]]):
        for num, color in draw:
            if num > highest[color]:
                highest[color] = num

    return check_highest, highest


def run_game_2(game: tuple[int, list[list[tuple[int, str]]]]):
    check_highest, highest = store_highest()

    pipe(
        game,
        spread(
            split(
                identity,
                each_c(
                    check_highest,
                ),
            )
        ),
    )
    return list(highest.values())


def part_1(games: list[tuple[int, list[list[tuple[int, str]]]]]):
    return pipe(
        games,
        map_c(run_game_1),
        sum,
    )


def part_2(games: list[tuple[int, list[list[tuple[int, str]]]]]):
    return pipe(
        games,
        map_c(run_game_2),
        compose(
            map_c(reduce_c(operator.mul)),
            reduce_c(operator.add),
        ),
    )


pipe(
    sys.stdin.read().splitlines(),
    map_c(parse_game),
    list,
    fork(
        part_1,
        part_2,
    ),
    spread(print),
)
