#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from __future__ import annotations

from day08_a import MapGraph, loadMapGraph

import itertools
import math
import sys
from typing import List


class Echelon:
    @staticmethod
    def begin(m: MapGraph) -> List[MapGraph.Iter]:
        return [MapGraph.Iter(m, n) for n in m.nodes if n.endswith("A")]

    def __init__(self, m: MapGraph):
        self.m = m
        self.iters: List[MapGraph.Iter] = Echelon.begin(m)
        print(f"Echelon width {len(self.iters)}")

    def done(self) -> bool:
        return all(i.current.endswith("Z") for i in self.iters)

    def advance(self, direction: int):
        # print(f"===== echelon {'LR'[direction]} =====")
        for i in self.iters:
            i.advance(direction)


class LCMEchelon:
    @staticmethod
    def begin(m: MapGraph) -> List[MapGraph.Iter]:
        return [MapGraph.Iter(m, n) for n in m.nodes if n.endswith("A")]

    def __init__(self, m: MapGraph):
        self.m = m
        self.iters: List[MapGraph.Iter] = Echelon.begin(m)
        self.cycles: List[int] = []
        self.steps: int = 0
        print(f"Echelon width {len(self.iters)}")

    def done(self) -> bool:
        return len(self.iters) == 0

    def result(self) -> int:
        return math.lcm(*self.cycles)

    def advance(self, direction: int):
        nextEchelon: List[MapGraph.Iter] = []
        for i in self.iters:
            if i.current.endswith("Z"):
                self.cycles.append(self.steps)
            else:
                i.advance(direction)
                nextEchelon.append(i)
        self.steps += 1
        self.iters = nextEchelon


def main(source):
    lines = source.readlines()
    directions = ["LR".index(d) for d in lines[0].strip()]

    graph = loadMapGraph(lines[2:])

    # naive echelon is (much) too slow.
    # next step: get the cycle length for each iterator independently
    # and then LCM them
    nodes = LCMEchelon(graph)
    for step, direction in enumerate(itertools.cycle(directions)):
        if nodes.done():
            print(f"{nodes.result()}")
            return
        nodes.advance(direction)
        if step and (step % 100000) == 0:
            print(f"{step=}")


if __name__ == "__main__":
    with open(sys.argv[1], "r") as source:
        main(source)
