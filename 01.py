import sys

from tools import compose, map_c, pipe

DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def clean(input: str) -> str:
    idx = 0
    while idx < len(input):
        for i, digit in enumerate(DIGITS):
            if input[idx:].startswith(digit):
                yield str(i + 1)
                break
            if input[idx].isnumeric():
                yield input[idx]
                break
        idx += 1


pipe(
    sys.stdin.read().splitlines(),
    map_c(
        compose(
            clean,
            list,
            lambda x: x[0] + x[-1],
            int,
        )
    ),
    sum,
    print,
)
