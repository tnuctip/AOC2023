#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from trie_01 import Trie, Searcher

import sys

from typing import Any, Dict, List, Optional, Tuple


class Classifier:
    def __init__(self, svmap: Dict[str, int]):
        self.svmap = svmap
        self.trie = Trie()
        for key, value in svmap.items():
            self.trie.add(key, value)

    def find_first(self, source: str) -> Optional[Tuple[str, int]]:
        s = Searcher(self.trie)
        for c in source:
            s.advance(c)
            okv = s.value()
            if okv is not None:
                return okv

        return None

    def find_all(self, source: str) -> List[int]:
        digits: List[int] = []

        s = Searcher(self.trie)
        for c in source:
            s.advance(c)
            okv = s.value()
            if okv is not None:
                digits.append(okv[1])

        return digits


DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}
isdigit = Classifier(DIGITS)


def recoverCalibration(line: str) -> int:
    """
    >>> recoverCalibration("1abc2")
    12
    >>> recoverCalibration("treb7uchet")
    77
    """
    digits = isdigit.find_all(line)
    return (10 * digits[0]) + digits[-1]


def sumCalibrations(source) -> int:
    return sum(recoverCalibration(line.strip()) for line in source)


def main():
    for filename in sys.argv[1:]:
        print(f"{filename=}")
        with open(filename, "r") as source:
            result = sumCalibrations(source)
            print(f"{result=}")


if __name__ == "__main__":
    main()
