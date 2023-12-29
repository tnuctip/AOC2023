#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from day04_a import matchCard

from collections import defaultdict
from collections.abc import Iterable
import sys
from typing import Dict


def countCards(source: Iterable[str]) -> int:
    # map row number to count, everything starts at 1
    counts: Dict[int, int] = defaultdict(lambda: 1)

    for num, line in enumerate(source):
        mult = counts[num]
        nmatched = matchCard(line)
        for extra in range(num + 1, num + 1 + nmatched):
            counts[extra] += mult

    return sum(counts.values())


def main():
    with open(sys.argv[1], "r") as source:
        result = countCards(source)
        print(f"{result}")


if __name__ == "__main__":
    main()
