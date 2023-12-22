#!/bin/env python3
# vi:ai:sw=4 ts=4 et

import sys

def recover_calibration(line:str) -> int:
    """
    >>> recover_calibration("1abc2")
    12
    >>> recover_calibration("treb7uchet")
    77
    """
    digits=list(map(int, filter(str.isdigit, line)))
    return (10 * digits[0]) + digits[-1]

def sum_calibrations(source) -> int:
    return sum(recover_calibration(line.strip()) for line in source)

def main():
    for filename in sys.argv[1:]:
        print(f"{filename=}")
        with open(filename, 'r') as source:
            result = sum_calibrations(source)
            print(f"{result=}")

if __name__ == '__main__':
    main()
