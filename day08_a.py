#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from __future__ import annotations

from collections.abc import Iterable
import functools
import itertools
import re
import sys
from typing import Dict, Tuple


class MapGraph:
    def __init__(self):
        self.nodes: Dict[str, Tuple[str, str]] = {}

    def add(self, line: str):
        m = re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
        assert m is not None
        node = m.group(1)
        left = m.group(2)
        right = m.group(3)
        self.nodes[node] = (left, right)

    class Iter:
        def __init__(self, m: MapGraph, current: str):
            self.m = m
            self.current = current

        def advance(self, direction: int):
            curnode = self.m.nodes[self.current]
            nextnode = curnode[direction]

            # print(f"{self.current} : {direction} {curnode} -> {nextnode}")
            self.current = nextnode

        def __eq__(self, other) -> bool:
            if not isinstance(other, MapGraph.Iter):
                return NotImplemented
            return self.current == other.current

    def begin(self):
        assert "AAA" in self.nodes
        return MapGraph.Iter(self, "AAA")

    @functools.cache
    def end(self):
        assert "ZZZ" in self.nodes
        return MapGraph.Iter(self, "ZZZ")


def loadMapGraph(source: Iterable[str]) -> MapGraph:
    result = MapGraph()

    for line in source:
        result.add(line)

    return result


def main(source):
    lines = source.readlines()
    directions = ["LR".index(d) for d in lines[0].strip()]

    graph = loadMapGraph(lines[2:])

    node = graph.begin()
    for step, direction in enumerate(itertools.cycle(directions)):
        if node == graph.end():
            print(f"{step}")
            return
        node.advance(direction)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as source:
        main(source)
