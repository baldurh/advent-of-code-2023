from dataclasses import dataclass
from sys import stdin

from tools import (
    compose,
    fork,
    map_c,
    pipe,
    reduce,
    spread,
    str_split,
)


@dataclass
class Mapper:
    maps: list[tuple[int, range]]

    def map_value(self, val: int):
        for to_start, from_range in self.maps:
            if val in from_range:
                return to_start + val - from_range[0]
        return val


def create_range(numbers=list[int]) -> tuple[int, range]:
    count = numbers[-1]
    to_range_start = numbers[0]
    from_range_start = numbers[1]
    return (to_range_start, range(from_range_start, from_range_start + count))


def create_mapper(numbers: list[list[int]]):
    return Mapper(list(map(create_range, numbers)))


def parse_map(map_str: str):
    maps_str = map_str.splitlines()[1:]
    mappers = pipe(
        maps_str,
        map_c(compose(str_split(" "), map_c(int), list)),
        create_mapper,
    )
    return mappers


def parse_almanac(almanac_str: str):
    parts = almanac_str.split("\n\n")
    seeds = list(map(int, parts.pop(0).split(": ")[1].split(" ")))
    mappers = list(map(parse_map, parts))
    return (seeds, mappers)


def part_1(almanac: tuple[list[int], list[Mapper]]):
    seeds, mappers = almanac
    return pipe(
        seeds,
        map_c(
            lambda seed: reduce(
                lambda acc, mapper: mapper.map_value(acc), mappers, seed
            )
        ),
        min,
    )


def to_pairs(val: list[int]) -> list[tuple[int, int]]:
    return list(zip(val, val[1:]))[::2]


def part_2(almanac: tuple[list[int], list[Mapper]]):
    seeds, mappers = almanac
    seed_ranges = [range(start, start + count) for (start, count) in to_pairs(seeds)]
    return pipe(
        seed_ranges,
        map_c(
            compose(
                map_c(
                    lambda seed: reduce(
                        lambda acc, mapper: mapper.map_value(acc), mappers, seed
                    )
                ),
                min,
            )
        ),
        min,
    )


pipe(stdin.read(), parse_almanac, fork(part_1, part_2), spread(print))
