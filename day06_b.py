#!/bin/env python3
# vi:ai:sw=4 ts=4 et

from day06_a import naivesolver, quadsolver

import sys

def main():
    with open(sys.argv[1], "r") as source:
        timestrs = source.readline().split()
        assert timestrs[0] == 'Time:'

        distancestrs = source.readline().split()
        assert distancestrs[0] == 'Distance:'

        timestr: str = ''.join(timestrs[1:])
        distancestr: str = ''.join(distancestrs[1:])

        time: int = int(timestr)
        distance: int = int(distancestr)

        result = quadsolver(time, distance)
        print(f"{result}")


if __name__ == "__main__":
    main()
