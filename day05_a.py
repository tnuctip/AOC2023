#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from collections import defaultdict
from collections.abc import Iterable
import re
import sys
from typing import Dict, List, Optional, Tuple


class XtoYMap:
    def __init__(self, header: str):
        m = re.match("(?P<from>[^-]+)-to-(?P<to>[^ ]+) map:", header)
        assert m is not None
        self.source: str = m.group("from")
        self.dest: str = m.group("to")
        self.ranges: List[Tuple[int, int, int]] = []

    def addRange(self, line: str):
        dstbegin, srcbegin, width = (int(i) for i in line.split(" "))
        self.ranges.append((dstbegin, srcbegin, width))

    def transform(self, value: int) -> int:
        for dstbegin, srcbegin, width in self.ranges:
            if srcbegin <= value and value <= srcbegin + width:
                return dstbegin + (value - srcbegin)
        return value


def parseMaps(source: Iterable[str]) -> List[XtoYMap]:
    maps: List[XtoYMap] = []
    current: Optional[XtoYMap] = None

    for line in source:
        line = line.strip()
        if len(line) == 0:
            continue

        if not current:
            current = XtoYMap(line)
            maps.append(current)
            continue

        current.addRange(line)

    return maps


class MapGraph:
    def __init__(self, maps: List[XtoYMap]):
        self.maplist = maps

        graph: Dict[str, List[XtoYMap]] = defaultdict(list)

        for m in maps:
            graph[m.source].append(m)

        self.graph = graph

    def findPath(self, source: str, destination: str) -> List[XtoYMap]:
        # degenerate case
        if source == destination:
            return []

        options = self.graph[source]
        if len(options) == 0:
            raise RuntimeError(f"no forward step from {source} towards {destination}")

        # only one way forward
        if len(options) == 1:
            return [options[0]] + self.findPath(options[0].dest, destination)

        # this is only OK because we're promised a DAG
        paths: List[List[XtoYMap]] = []
        for step in options:
            try:
                following = self.findPath(step.dest, destination)
                paths.append([step] + following)
            except RuntimeError:
                pass  # one dead end is not a problem

        path = min(paths, key=len)
        return path


def walkPath(value: int, path: List[XtoYMap]) -> int:
    for step in path:
        nextvalue = step.transform(value)
        # print(f"{step.source}:{value} -> {step.dest}:{nextvalue}")
        value = nextvalue
    return value


def loadMapPath(source: str, destination: str, lines: List[str]) -> List[XtoYMap]:
    xys: List[XtoYMap] = []
    xy: Optional[XtoYMap] = None

    for line in lines:
        line = line.strip()
        if len(line):
            if line.endswith(" map:"):
                xy = XtoYMap(line)
                xys.append(xy)
                continue

            assert xy is not None
            xy.addRange(line)

    graph = MapGraph(xys)
    path = graph.findPath(source, destination)
    # print(f"path {[(s.source, s.dest) for s in path]}")
    return path


def seedLocations(source: List[str]) -> Iterable[int]:
    seedline = source[0].split()
    assert seedline[0] == "seeds:"
    seeds = [int(s) for s in seedline[1:]]

    # build the graph
    path = loadMapPath("seed", "location", source[1:])

    locations = [walkPath(seed, path) for seed in seeds]
    return locations


def main():
    with open(sys.argv[1], "r") as source:
        result = min(seedLocations(source.readlines()))
        print(f"{result}")


if __name__ == "__main__":
    main()
