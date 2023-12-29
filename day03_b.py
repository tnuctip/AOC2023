#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from day03_a import matchpos

from collections.abc import Iterable
import re
import sys
from typing import List, Tuple


def boxOverlaps(
    point: Tuple[int, int], topleft: Tuple[int, int], botright: Tuple[int, int]
) -> bool:
    """
    >>> boxOverlaps((0,0), (0,0), (3,3))
    True
    >>> boxOverlaps((0,0), (1,0), (3,3))
    False
    >>> boxOverlaps((1,1), (0,0), (3,3))
    True
    >>> boxOverlaps((3,3), (0,0), (3,2))
    False
    """
    left, top = topleft
    right, bot = botright
    pxx, pyy = point

    if top <= pyy and pyy <= bot:
        if left <= pxx and pxx <= right:
            return True
    return False


def gearRatios(source: Iterable[str]) -> int:
    numpat = re.compile(r"\d+")
    sympat = re.compile("[^ .0-9]")

    numbers: List[Tuple[int, int, int, int]] = []
    symbols: List[Tuple[int, int]] = []

    for lineno, line in enumerate(source):
        line = line.strip()
        for start, end, sym in matchpos(line, sympat):
            if sym == "*":
                symbols.append((start, lineno))
                # print(f"gear at {start},{lineno}")

        for start, end, numstr in matchpos(line, numpat):
            numbers.append((start, end, lineno, int(numstr)))
            # print(f"number {numstr} at ({start}-{end}),{lineno}")

    # now find all the symbols adjacent to exactly two numbers
    gears: List[int] = []

    for sxx, syy in symbols:
        found: List[int] = []
        for nxbegin, nxend, nyy, num in numbers:
            if boxOverlaps((sxx, syy), (nxbegin - 1, nyy - 1), (nxend, nyy + 1)):
                found.append(num)

        if len(found) == 2:
            # print(f"found exactly two numbers adjacent to {sxx},{syy}: {found}")
            gears.append(found[0] * found[1])

    return sum(gears)


def main():
    with open(sys.argv[1], "r") as source:
        result = gearRatios(source)
        print(f"{result}")


if __name__ == "__main__":
    main()
