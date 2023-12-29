#!/bin/env python3
# vi:ai:sw=4 ts=4 et
from __future__ import annotations

from day05_a import loadMapPath, XtoYMap

from collections.abc import Iterable
import sys
from typing import List, Optional


class Interval:
    """Half-open interval [begin, end)"""

    def __init__(self, begin: int, end: int):
        assert begin <= end
        self.begin = begin
        self.end = end

    def width(self) -> int:
        """
        >>> Interval(1, 3).width()
        2
        """
        return self.end - self.begin

    def __str__(self):
        return f"({self.begin}, {self.end}]"

    def isdisjoint(self, other: Interval) -> bool:
        """
        >>> Interval(1, 1).isdisjoint(Interval(1, 1))
        True
        >>> Interval(1, 3).isdisjoint(Interval(3, 5))
        True
        >>> Interval(1, 4).isdisjoint(Interval(3, 5))
        False
        """
        if self.width() == 0 or other.width() == 0:
            return True

        if self.end <= other.begin:
            return True
        if self.begin >= other.end:
            return True

        return False

        """
        >>> Interval(2, 3).isdisjoint(Interval(1, 4))
        True
        >>> Interval(1, 3).isdisjoint(Interval(1, 5))
        True
        >>> Interval(1, 3).isdisjoint(Interval(3, 5))
        False
        """

    def issubset(self, other: Interval) -> bool:
        if self.begin >= other.begin and self.end <= other.end:
            return True
        return False

    def intersection(self, other: Interval) -> Optional[Interval]:
        if other.issubset(self):
            return other

        if self.isdisjoint(other):
            return None

        maxmin = max(self.begin, other.begin)
        minmax = min(self.end, other.end)
        return Interval(maxmin, minmax)

    def difference(self, other: Interval) -> List[Interval]:
        overlap = other.intersection(self)
        if overlap is None:
            return [self]
        other = overlap

        results: List[Interval] = []
        if self.begin < other.begin:
            results.append(Interval(self.begin, other.begin))
        if other.end < self.end:
            results.append(Interval(other.end, self.end))

        return results


def transformIntervals(source: List[Interval], xtoy: XtoYMap) -> List[Interval]:
    mapranges = [(Interval(s, s + w), d) for d, s, w in xtoy.ranges]

    curgen = source
    nextgen: List[Interval] = []
    for s in curgen:
        for srange, dest in mapranges:
            overlap = s.intersection(srange)
            if overlap is None:
                continue

            offset = dest - srange.begin
            nextgen.append(Interval(overlap.begin + offset, overlap.end + offset))

            residue = s.difference(overlap)
            if len(residue) >= 1:
                s = residue[0]
                if len(residue) == 2:
                    curgen.append(residue[1])
            else:
                continue

    return nextgen


def seedLocations(source: List[str]) -> Iterable[int]:
    seedline = source[0].split()
    assert seedline[0] == "seeds:"
    seedraws = [int(s) for s in seedline[1:]]
    seedPairs = zip(seedraws[0::2], seedraws[1::2])
    seeds = [Interval(s[0], s[0] + s[1]) for s in seedPairs]

    # build the graph
    path = loadMapPath("seed", "location", source[1:])

    locations = seeds
    for step in path:
        locations = transformIntervals(locations, step)

    return (i.begin for i in locations)


def main():
    with open(sys.argv[1], "r") as source:
        result = min(seedLocations(source.readlines()))
        print(f"{result}")


if __name__ == "__main__":
    main()
