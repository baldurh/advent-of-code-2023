import math
from functools import partial
from itertools import cycle
from sys import stdin

from tools import compose, identity, map_c, pipe, re_sub, split_args, spread, str_split

parse_node = compose(
    str_split(" = "),
    split_args(
        identity,
        compose(
            re_sub(r"(\w+)", r'"\1"'),
            eval,
        ),
    ),
)


parse = compose(
    str_split("\n\n"),
    split_args(
        identity,
        compose(
            str.splitlines,
            map_c(parse_node),
            dict,
        ),
    ),
    tuple,
)


def traverse(map, key):
    instructions, nodes = map
    i = 0
    for dir in cycle(instructions):
        key = nodes[key][0 if dir == "L" else 1]
        i += 1
        if key.endswith("Z"):
            break
    return i


def traverse_keys(map):
    start_keys = [key for key in map[1] if key.endswith("A")]
    return map_c(partial(traverse, map))(start_keys)


pipe(
    stdin.read(),
    parse,
    traverse_keys,
    spread(math.lcm),
    print,
)
