#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from day02_a import Game

from collections.abc import Iterable
import sys


def powerGames(source: Iterable[str]) -> Iterable[int]:
    games = (Game(line) for line in source)

    # return (map(operator.mul, game.maxbrg) for game in games)
    return (game.maxbrg[0] * game.maxbrg[1] * game.maxbrg[2] for game in games)


def main():
    with open(sys.argv[1], "r") as source:
        powers = powerGames(source)
        print(f"{sum(powers)}")


if __name__ == "__main__":
    main()
