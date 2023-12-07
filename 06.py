from math import ceil, prod
from sys import stdin

from tools import compose, fork, map_c, pipe, re_split, re_sub, spread


def travel(speed: int, time: int):
    return speed * time


def find_highest_under(time: int, record: int):
    curr_speed = time // 2
    highest_under = 0
    while True:
        distance = travel(curr_speed, time - curr_speed)
        if distance == record:
            return curr_speed
        if curr_speed > highest_under and distance <= record:
            highest_under = curr_speed
            curr_speed += 1
            if travel(curr_speed, time - curr_speed) > record:
                return curr_speed - 1
            continue
        if distance > record:
            curr_speed = curr_speed // 2
        elif distance <= record:
            if highest_under == curr_speed:
                break
            curr_speed = ceil(curr_speed * 1.5)
        else:
            break
    return highest_under


def test(race: tuple[int, int]) -> int:
    time, record = race

    start = find_highest_under(time, record)
    end = time - start
    return end - start - 1


def part_1(input: str):
    return pipe(
        # parse
        input,
        str.splitlines,
        map_c(compose(re_split(r"\s+"), lambda x: x[1:], map_c(int))),
        spread(zip),
        list,
        # test
        map_c(test),
        prod,
    )


def part_2(input: str):
    return pipe(
        # parse
        input,
        str.splitlines,
        map_c(compose(re_sub(r"\s+", ""), re_split(":"), lambda x: x[1:], map_c(int))),
        spread(zip),
        list,
        # test
        map_c(test),
        prod,
    )


pipe(
    stdin.read(),
    fork(part_1, part_2),
    spread(print),
)
