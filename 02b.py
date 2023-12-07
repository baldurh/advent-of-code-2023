from collections import defaultdict
from math import prod
from sys import stdin


def run_game(game: str):
    colors = defaultdict(lambda: [])
    rounds = game.strip().split(": ")[1]

    for draw in rounds.split("; "):
        for cubes in draw.split(", "):
            count, color = cubes.split(" ")
            colors[color].append(int(count))
    return prod([max(color) for color in colors.values()])


print(sum([run_game(game) for game in stdin]))
