#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from enum import IntFlag
import itertools
import sys
from typing import Dict, List, Optional, Set, Tuple


class Dir(IntFlag):
    EMPTY = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


opposite: Dict[Dir, Dir] = {
    Dir.NORTH: Dir.SOUTH,
    Dir.SOUTH: Dir.NORTH,
    Dir.EAST: Dir.WEST,
    Dir.WEST: Dir.EAST,
    Dir.EMPTY: Dir.EMPTY,
}

xdelta: Dict[Dir, int] = {
    Dir.NORTH: 0,
    Dir.SOUTH: 0,
    Dir.EAST: +1,
    Dir.WEST: -1,
}

ydelta: Dict[Dir, int] = {
    Dir.NORTH: -1,
    Dir.SOUTH: +1,
    Dir.EAST: 0,
    Dir.WEST: 0,
}


def movePos(pos: Tuple[int, int], direction: Dir) -> Tuple[int, int]:
    return (pos[0] + xdelta[direction], pos[1] + ydelta[direction])


def exitDir(moving: Dir, pipe: Dir) -> Dir:
    """eg. if we move Eastwards into a pipe connecting West-to-North, we go North ...

           ^
           |
        -> J

    >>> exitDir(Dir.EAST, Dir.WEST|Dir.NORTH)
    <Dir.NORTH: 1>
    >>> exitDir(Dir.EAST, Dir.WEST|Dir.EAST)
    <Dir.EAST: 2>
    >>> exitDir(Dir.WEST, Dir.WEST|Dir.EAST)
    <Dir.WEST: 8>
    >>> exitDir(Dir.WEST, Dir.EAST|Dir.SOUTH)
    <Dir.SOUTH: 4>
    """
    enteringFrom: Dir = opposite[moving]
    assert (pipe & enteringFrom) != Dir.EMPTY
    return pipe & ~enteringFrom


def exitDirections(pipe: Dir) -> List[Dir]:
    """eg. if we start from a pipe connecting West-to-North, we can leave either Westwards or Northwards ...

    >>> exitDirections(Dir.WEST|Dir.NORTH)
    [<Dir.NORTH: 1>, <Dir.WEST: 8>]
    >>> exitDirections(Dir.WEST|Dir.EAST)
    [<Dir.EAST: 2>, <Dir.WEST: 8>]
    """
    exits: List[Dir] = []
    for d in [Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST]:
        if pipe & d:
            exits.append(d)
    return exits


class PipeGraph:
    """
    TILE characters are (forming a square):
        F-7
        | |
        L-J
    """

    TILE: Dict[str, Dir] = {
        "F": Dir.SOUTH | Dir.EAST,
        "-": Dir.EAST | Dir.WEST,
        "7": Dir.WEST | Dir.SOUTH,
        "|": Dir.NORTH | Dir.SOUTH,
        "L": Dir.NORTH | Dir.EAST,
        "J": Dir.WEST | Dir.NORTH,
        ".": Dir.EMPTY,
    }

    CHAR: Dict[Dir, str] = dict((d, k) for k, d in TILE.items())

    def convertTiles(self, lines: List[str]):
        start: Optional[Tuple[int, int]] = None
        rows: List[List[Dir]] = []
        for line in lines:
            line = line.strip()
            row: List[Dir] = []
            for c in line:
                if c == "S":
                    if start:
                        raise RuntimeError(
                            f"start detected at {start=} and ({len(row)}, {len(rows)})"
                        )
                    start = (len(row), len(rows))
                    row.append(Dir.EMPTY)  # figure this out later
                elif c in PipeGraph.TILE:
                    row.append(PipeGraph.TILE[c])
                else:
                    raise RuntimeError(
                        f"character {c} not recognized at ({len(row)}, {len(rows)})"
                    )
            rows.append(row)
        assert start is not None
        self.start: Tuple[int, int] = start
        self.tiles: List[List[Dir]] = rows

    def resolveStartConnectivity(self):
        startx, starty = self.start
        entrances: int = 0
        height: int = len(self.tiles)
        width: int = len(self.tiles[0])
        inferred: Dir = Dir.EMPTY
        if startx > 0 and self.tiles[starty][startx - 1] & Dir.EAST:
            inferred |= Dir.WEST
            entrances += 1
        if startx < width - 1 and self.tiles[starty][startx + 1] & Dir.WEST:
            inferred |= Dir.EAST
            entrances += 1
        if starty > 0 and self.tiles[starty - 1][startx] & Dir.SOUTH:
            inferred |= Dir.NORTH
            entrances += 1
        if starty < height - 1 and self.tiles[starty + 1][startx] & Dir.NORTH:
            inferred |= Dir.SOUTH
            entrances += 1

        assert entrances == 2
        self.tiles[starty][startx] = inferred

    def __init__(self, lines: List[str]):
        self.convertTiles(lines)
        self.resolveStartConnectivity()

    def __str__(self) -> str:
        return "\n".join("".join(PipeGraph.CHAR[d] for d in row) for row in self.tiles)

    def begin(self) -> Dir:
        startx, starty = self.start
        return self.tiles[starty][startx]

    def __getitem__(self, key: Tuple[int, int]) -> Dir:
        x, y = key
        return self.tiles[y][x]


def findFarthest(graph: PipeGraph):
    steps: int = 0
    seen: Set[Tuple[int, int]] = set()
    cursor: List[Tuple[int, int]] = [graph.start, graph.start]
    direction: List[Dir] = exitDirections(graph.begin())
    assert len(direction) == 2

    def nextstep(moving: Dir, pos: Tuple[int, int]) -> Tuple[Dir, Tuple[int, int]]:
        tile = graph[pos]
        newPos = movePos(pos, moving)
        newDir = exitDir(moving, graph[newPos])
        return (newDir, newPos)

    for step in itertools.count(0):
        seen.add(cursor[0])
        seen.add(cursor[1])

        for i in range(2):
            newDir, newPos = nextstep(direction[i], cursor[i])
            direction[i] = newDir
            cursor[i] = newPos

        if cursor[0] in seen or cursor[1] in seen:
            return step


def main(source):
    lines = source.readlines()
    graph = PipeGraph(lines)

    maxdist = findFarthest(graph)
    print(f"{maxdist}")


if __name__ == "__main__":
    with open(sys.argv[1], "r") as source:
        main(source)
