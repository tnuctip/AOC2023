#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
import functools
import sys
from typing import Dict, List


@functools.total_ordering
class Hand:
    TYPES = [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]
    TYPE_NAMES = [
        "Five of a kind",
        "Four of a kind",
        "Full house",
        "Three of a kind",
        "Two pair",
        "One pair",
        "High card",
    ]

    CARD_SCORES = "AKQT98765432J"

    @staticmethod
    def keyJokersWild(counts: Dict[str, int]) -> List[int]:
        """
        >>> Hand.keyJokersWild({'J':5})
        [5]
        >>> Hand.keyJokersWild({'A':4, 'J':1})
        [5]
        >>> Hand.keyJokersWild({'A':2, 'K':2, 'J':1})
        [3, 2]
        >>> Hand.keyJokersWild({'A':1, 'K':1, 'Q':1, 'J':1, '9':1})
        [2, 1, 1, 1]
        """
        # replace the wildcards
        njokers: int = 0
        if "J" in counts:
            njokers = counts["J"]
            del counts["J"]
            # degenerate case
            if njokers == 5:
                return [5]

        # key without jokers
        key = list(reversed(sorted(counts.values())))

        # use the wildcards where they help the most
        key[0] += njokers
        return key

    @staticmethod
    def getType(cards: str) -> int:
        """Categorize the type of a hand.

        >>> Hand.getType('AAAAA')
        0
        >>> Hand.TYPE_NAMES[Hand.getType('AAAAA')]
        'Five of a kind'
        >>> Hand.TYPE_NAMES[Hand.getType('AAA3A')]
        'Four of a kind'
        >>> Hand.TYPE_NAMES[Hand.getType('AAA33')]
        'Full house'
        >>> Hand.TYPE_NAMES[Hand.getType('AAA34')]
        'Three of a kind'
        >>> Hand.TYPE_NAMES[Hand.getType('AA434')]
        'Two pair'
        >>> Hand.TYPE_NAMES[Hand.getType('AA234')]
        'One pair'
        >>> Hand.TYPE_NAMES[Hand.getType('AK234')]
        'High card'
        >>> Hand.TYPE_NAMES[Hand.getType('AJ234')]
        'One pair'
        """
        assert len(cards) == 5
        counts: Dict[str, int] = defaultdict(int)
        for card in cards:
            counts[card] += 1

        key = Hand.keyJokersWild(counts)
        return Hand.TYPES.index(key)

    def __init__(self, cards: str, bid: int = 0):
        self.cards: str = cards
        self.type: int = Hand.getType(cards)
        self.bid = bid

    def __eq__(self, other) -> bool:
        """Only identical hands compare equal

        >>> Hand('AAAAA') == Hand('AAAAA')
        True
        >>> Hand('AAAAK') == Hand('KKKKA')
        False
        """
        if not isinstance(other, Hand):
            return NotImplemented

        return self.cards == other.cards

    def __lt__(self, other: Hand) -> bool:
        """Only identical hands compare equal

        >>> Hand('AAAAA') < Hand('AAAAA')
        False
        >>> Hand('AAAAK') < Hand('KKKKA')
        False
        >>> Hand('KKKKA') < Hand('AAAAK')
        True
        >>> Hand('33332') < Hand('2AAAA')
        False
        >>> Hand('77788') < Hand('77888')
        True
        """
        if self.cards == other.cards:
            return False
        if self.type > other.type:
            return True
        if self.type < other.type:
            return False
        # self.type == other.type
        # compare card ranks
        sscore = [Hand.CARD_SCORES.index(c) for c in self.cards]
        oscore = [Hand.CARD_SCORES.index(c) for c in other.cards]
        for s, o in zip(sscore, oscore):
            if s > o:
                return True
            if s < o:
                return False
        return False


def loadHands(source: Iterable[str]) -> List[Hand]:
    result: List[Hand] = []
    for line in source:
        cards, bid = line.split()
        result.append(Hand(cards, int(bid)))
    return result


def main():
    with open(sys.argv[1], "r") as source:
        hands = loadHands(source)

        ordered = enumerate(sorted(hands))
        scored = [h.bid * (1 + e) for e, h in ordered]

        print(f"{sum(scored)}")


if __name__ == "__main__":
    main()
