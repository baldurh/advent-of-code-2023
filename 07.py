from __future__ import annotations

from collections.abc import Callable
from itertools import groupby
from sys import stdin
from typing import TypeAlias

from tools import compose, fork, identity, map_c, mapi_c, pipe, split, spread, str_split

Hand: TypeAlias = tuple[str, int]


def replace_jokers(cards: str) -> str:
    # Cards have been translated at this point
    if cards == "00000":
        # Only Jokers, best card is Joker
        best_card = cards[0]
    else:
        # Sort the cards without Jokers
        sorted_cards = sorted(cards.replace("0", ""), reverse=True)
        # Find the card in the best group (group with most cards)
        best_card = sorted(
            [list(x[1]) for x in groupby(sorted_cards)],
            key=lambda x: len(x),
            reverse=True,
        )[0][0]

    return cards.replace("0", best_card)


def type(cards: str) -> int:
    cards = replace_jokers(cards)
    sorted_cards = sorted(cards, reverse=True)
    card_groups = sorted(
        [list(x[1]) for x in groupby(sorted_cards)],
        key=lambda x: len(x),
        reverse=True,
    )
    match len(card_groups), len(card_groups[0]):
        case 5, _:  # 5 groups: High card
            return 0
        case 4, _:  # 4 groups: One pair
            return 1
        case 3, 2:  # 3 groups, largest group is 2: Two pairs
            return 2
        case 3, _:  # 3 groups: Three of a kind
            return 3
        case 2, 3:  # 2 groups, largest group is 3: Full house
            return 4
        case 2, _:  # 2 groups: Four of a kind
            return 5
        case 1, _:  # 1 group: Five of a kind
            return 6
        case _:
            return 0


def translate(mapping: dict[str, str]) -> Callable[[Hand], Hand]:
    # Translate the string to a sortable string
    trans_table = str.maketrans(mapping)

    def inner(hand: Hand) -> Hand:
        cards, bet = hand
        return (cards.translate(trans_table), bet)

    return inner


def score_hand(hand: Hand) -> Hand:
    cards, bet = hand
    return (f"{type(cards)}{cards}", bet)


def hand_winning(rank: int, hand: Hand) -> int:
    _, bet = hand
    return bet * rank


pipe(
    stdin.read().splitlines(),
    map_c(
        compose(
            str_split(" "),
            spread(
                split(
                    identity,
                    int,
                )
            ),
        )
    ),
    list,
    fork(
        # part 1
        map_c(
            translate({"T": "B", "J": "C", "Q": "D", "K": "E", "A": "F"}),
        ),
        # part 2
        map_c(
            translate({"J": "0", "T": "B", "Q": "D", "K": "E", "A": "F"}),
        ),
    ),
    map_c(
        compose(
            map_c(score_hand),
            sorted,
            mapi_c(hand_winning, 1),
            sum,
        )
    ),
    spread(print),
)
