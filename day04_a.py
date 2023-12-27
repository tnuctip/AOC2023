#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from collections.abc import Iterable
import re
import sys
from typing import Dict, List, Set, Tuple

def matchCard(line: str) -> int:
    name, numbers = line.split(":")
    winstr, actstr = numbers.split("|")

    winning: Set[int] = set((int(i) for i in winstr.split()))
    actual: Set[int] = set((int(i) for i in actstr.split()))

    matched = winning & actual

    return len(matched)

def scoreCard(line: str) -> int:
    nmatched = matchCard(line)

    if nmatched > 0:
        return 2 ** (nmatched - 1)

    return 0


def scoreCards(source: Iterable[str]) -> int:
    scores = (scoreCard(line) for line in source)
    return sum(scores)


def main():
    with open(sys.argv[1], "r") as source:
        result = scoreCards(source)
        print(f"{result}")


if __name__ == "__main__":
    main()
