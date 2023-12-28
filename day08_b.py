#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from __future__ import annotations

from day08_a import MapGraph, loadMapGraph

import itertools
import sys
from typing import List

class Echelon:
    @staticmethod
    def begin(m: MapGraph) -> List[MapGraph.Iter]:
        return [MapGraph.Iter(m, n) for n in m.nodes if n.endswith('A')]

    def __init__(self, m: MapGraph):
        self.m = m
        self.iters: List[MapGraph.Iter] = Echelon.begin(m)
        print(f"Echelon width {len(self.iters)}")

    def done(self) -> bool:
        return all(i.current.endswith('Z') for i in self.iters)

    def advance(self, direction:int):
        # print(f"===== echelon {'LR'[direction]} =====")
        for i in self.iters:
            i.advance(direction)


def main(source):
    lines = source.readlines()
    directions = ['LR'.index(d) for d in lines[0].strip()]

    graph = loadMapGraph(lines[2:])

    nodes = Echelon(graph)
    for step, direction in enumerate(itertools.cycle(directions)):
        if nodes.done():
            print(f"{step}")
            return
        nodes.advance(direction)
        if (step % 100000) == 0:
            print(f"{step=}")


if __name__ == "__main__":
    with open(sys.argv[1], "r") as source:
        main(source)
