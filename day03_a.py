#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from collections.abc import Iterable
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

def matchpos(line: str, pattern: re.Pattern) -> Iterable[Tuple[int, int, str]]:
    """Find (start, end, group) for every match in the source string"""
    for m in re.finditer(pattern, line):
        yield (m.start(), m.end(), m.group())

def partnums(source: Iterable[str]):
    """this is eager, ie, we find all numeral sequences and symbols first"""
    # find positions of every symbol and number
    numpat = re.compile('\d+')
    sympat = re.compile('[^ .0-9]')

    numbers: List[Tuple(int, int, int, int)] = []
    symbols: Set[Tuple(int, int)] = set()

    for lineno, line in enumerate(source):
        line = line.strip()
        for start, end, sym in matchpos(line, sympat):
            symbols.add((start, lineno))
            print(f"symbol {sym} at {start},{lineno}")

        for start, end, num in matchpos(line, numpat):
            numbers.append((start, end, lineno, int(num)))
            print(f"number {num} at ({start}-{end}),{lineno}")

    # now extract all the numbers adjacent to a symbol
    partnums: List[int] = []

    for xbegin, xend, yy, num in numbers:
        if (xbegin-1, yy) in symbols or (xend, yy) in symbols:
            # same line -- $123$
            partnums.append(num)
            print(f"{num} is on the same line as a symbol")
        else:
            # adjacent line:
            # $....
            # .123.
            # ....$
            for xx in range(xbegin-1, xend+1):
                if (xx, yy-1) in symbols:
                    print(f"{num} is adjacent to the symbol at {xx},{yy-1}")
                    partnums.append(num)
                    break
                elif (xx, yy+1) in symbols:
                    print(f"{num} is adjacent to the symbol at {xx},{yy+1}")
                    partnums.append(num)
                    break

    return sum(partnums)

def main():
    with open(sys.argv[1], "r") as source:
        result = partnums(source)
        print(f"{result}")

if __name__ == "__main__":
    main()
