#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from collections.abc import Iterable
import operator
import re
import sys
from typing import Any, Dict, List, Optional, Tuple


class Game:
    def __init__(self, line: str):
        line = line.strip()
        head, body = line.split(":")
        self.id = int(head.split(" ")[1])
        self.maxbrg = Game.maxima(body)

        # print(f"{line} -> max:{self.maxbrg}")

    @staticmethod
    def search(name: str, sample: str) -> int:
        m = re.search(f"(\d*) {name}", sample)
        if m:
            return int(m.group(1))
        else:
            return 0

    @staticmethod
    def parse(body: str) -> Iterable[Tuple[int, int, int]]:
        for sample in body.split(";"):
            yield (
                Game.search("blue", sample),
                Game.search("red", sample),
                Game.search("green", sample),
            )

    @staticmethod
    def maxima(body: str) -> Tuple[int, int, int]:
        maxblue: int = 0
        maxred: int = 0
        maxgreen: int = 0

        for b, r, g in Game.parse(body):
            maxblue = max(maxblue, b)
            maxred = max(maxred, r)
            maxgreen = max(maxgreen, g)

        return (maxblue, maxred, maxgreen)


def filterGames(
    source: Iterable[str], blue: int, red: int, green: int
) -> Iterable[int]:
    games = (Game(line) for line in source)

    def possible(game: Game) -> bool:
        return all(
            maximum <= needed
            for maximum, needed in zip(game.maxbrg, (blue, red, green))
        )

    return (game.id for game in filter(possible, games))


def solve(blue: int, red: int, green: int):
    with open(sys.argv[1], "r") as source:
        ids = list(filterGames(source, blue, red, green))
        print(f"{ids=}\n{sum(ids)}")


def main():
    solve(blue=14, red=12, green=13)


if __name__ == "__main__":
    main()
