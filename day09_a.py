#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from typing import List
import itertools
import sys


def nextInSequence(sequence: List[int]) -> int:
    """
    >>> nextInSequence([0,3,6,9,12,15])
    18
    """
    if not any(sequence):
        # all zeroes
        return 0

    if len(sequence) < 2:
        raise RuntimeError(f"can't compute differences in {sequence=}")

    differences = [b - a for a, b in itertools.pairwise(sequence)]
    nextDelta = nextInSequence(differences)
    return sequence[-1] + nextDelta


def solve(line: str) -> int:
    return nextInSequence([int(tok) for tok in line.split()])


def main(source):
    result = sum(solve(line) for line in source)
    print(f"{result}")


if __name__ == "__main__":
    with open(sys.argv[1], "r") as source:
        main(source)
