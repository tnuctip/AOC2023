#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from collections import defaultdict
from collections.abc import Iterable
import functools
import math
import operator
import re
import sys
from typing import Dict, List, Optional, Set, Tuple

def speed(hold:int) -> int:
    return hold

def distance(hold:int, total:int) -> int:
    """
    >>> distance(0, 7)
    0
    >>> distance(3, 7)
    12
    >>> distance(4, 7)
    12
    """
    return speed(hold) * (total - hold)

def naivesolver(time:int, winner:int) -> int:
    """
    >>> naivesolver(7, 9)
    4
    >>> naivesolver(7, 10)
    2
    """
    winners = filter(lambda d:d > winner, (distance(hold,time) for hold in range(0,time+1)))
    return len(list(winners))

## or we could use the quadratic method:
## y = Bx - x^2
## with B = total ...
##
## so for a given previously-winning distance D, we want the roots of
## y = Bx - x^2 - D
##
## (see day06-quadratic.svg to visualize the intercepts)
##
def quadsolver(time:int, winner:int) -> int:
    """
    >>> quadsolver(7, 9)
    4
    >>> quadsolver(7, 10)
    2
    """
    a = -1
    b = time
    c = -winner
 
    discriminant = b**2 - (4 * a * c)
    assert discriminant >= 0

    if discriminant == 0:
        # only a single solution
        return 1

    sq = math.sqrt(discriminant)
    roots = ((-b + sq)/(2*a), (-b -sq)/(2*a))
    return math.ceil(max(roots)) - math.ceil(min(roots)+0.0001)

def solve(times: List[int], distances: List[int]) -> int:
    results: List[int] = [naivesolver(time, distance) for time, distance in zip(times, distances)]
    return functools.reduce(operator.mul, results)

def main():
    with open(sys.argv[1], "r") as source:
        timestr = source.readline().split()
        assert timestr[0] == 'Time:'

        distancestr = source.readline().split()
        assert distancestr[0] == 'Distance:'

        times: List[int] = [int(s) for s in timestr[1:]]
        distances: List[int] = [int(s) for s in distancestr[1:]]

        result = solve(times, distances)
        print(f"{result}")


if __name__ == "__main__":
    main()
