#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from day05_a import loadMapPath, walkPath

from collections import defaultdict
from collections.abc import Generator, Iterable
import itertools
import re
import sys
from typing import Dict, List, Set, Tuple


def seedLocations(source: List[str]) -> Iterable[int]:
    seedline = source[0].split()
    assert seedline[0] == "seeds:"
    seedraws = [int(s) for s in seedline[1:]]
    seedPairs = zip(seedraws[0::2], seedraws[1::2])
    seeds = itertools.chain.from_iterable(range(s[0], s[0]+s[1]) for s in seedPairs)

    ## build the graph
    path = loadMapPath("seed", "location", source[1:])

    locations = (walkPath(seed, path) for seed in seeds)
    return locations


def main():
    with open(sys.argv[1], "r") as source:
        result = min(seedLocations(source.readlines()))
        print(f"{result}")


if __name__ == "__main__":
    main()
