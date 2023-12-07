from sys import stdin
from typing import TypeAlias

from tools import (
    compose,
    fork,
    map_c,
    pipe,
    reduce,
    spread,
    str_split,
)

SeedValueMapper: TypeAlias = tuple[int, range]
SeedRange: TypeAlias = tuple[int, int]
Almanac: TypeAlias = tuple[list[int], list[list[SeedValueMapper]]]


def map_value(val: int, mappers: list[SeedValueMapper]):
    for to_start, from_range in mappers:
        if val in from_range:
            return to_start + val - from_range.start
    return val


def map_ranges(vals: list[SeedRange], mappers: list[SeedValueMapper]):
    vals = split_ranges(vals, [x[1] for x in mappers])
    new_vals = []
    for start, stop in vals:
        new_start = map_value(start, mappers)
        new_stop = map_value(stop, mappers)

        new_vals.append((new_start, new_stop))

    return new_vals


def split_ranges(vals: list[SeedRange], ranges: list[range]) -> list[SeedRange]:
    new_vals = []
    for start, stop in vals:
        for r in ranges:
            if start in r and stop in r:
                new_vals.append((start, stop))
                break
            if start in r:
                new_vals.append((start, r.stop - 1))
                new_vals.append((r.stop, stop))
                break
            if stop in r:
                new_vals.append((r.start, stop))
                new_vals.append((start, r.start - 1))
                break
        else:
            new_vals.append((start, stop))
    return new_vals


def create_seed_value_mapper(numbers=tuple[int, int, int]) -> SeedValueMapper:
    count = numbers[2]
    to_range_start = numbers[0]
    from_range_start = numbers[1]
    return (to_range_start, range(from_range_start, from_range_start + count))


def parse_map(map_str: str) -> list[SeedValueMapper]:
    maps_str = map_str.splitlines()[1:]
    mappers = pipe(
        maps_str,
        map_c(
            compose(
                str_split(" "),
                map_c(int),
                tuple,
                create_seed_value_mapper,
            )
        ),
        list,
    )
    return mappers


def parse_almanac(almanac_str: str) -> Almanac:
    parts = almanac_str.split("\n\n")
    seeds = list(map(int, parts.pop(0).split(": ")[1].split(" ")))
    mappers = list(map(parse_map, parts))
    return (seeds, mappers)


def to_pairs(val: list[int]) -> list[tuple[int, int]]:
    return list(zip(val, val[1:]))[::2]


def part_1(almanac: Almanac):
    seeds, mappers = almanac
    return pipe(
        seeds,
        map_c(
            # Pass each seed through all the mappers in sequence
            lambda seed: reduce(map_value, mappers, seed)
        ),
        min,
    )


def part_2(almanac: Almanac):
    seeds, mappers = almanac
    seed_ranges = [(start, start + count - 1) for (start, count) in to_pairs(seeds)]

    return pipe(
        seed_ranges,
        # Pass each seed range through all the mappers in sequence
        lambda seed_range: reduce(
            map_ranges,
            mappers,
            seed_range,
        ),
        min,
        min,
    )


pipe(
    stdin.read(),
    parse_almanac,
    fork(part_1, part_2),
    spread(print),
)
