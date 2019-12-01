#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 1 module."""


def fuel(mass):
    return mass // 3 - 2


def fuel_recursive(mass):
    f = fuel(mass)
    if f <= 0:
        return 0
    return f + fuel_recursive(f)


def process(puzzle_input, verbose=False):
    p1 = sum([fuel(int(x)) for x in puzzle_input])
    p2 = sum([fuel_recursive(int(x)) for x in puzzle_input])
    return p1, p2


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    parser.add_argument('-v', '--verbose', '-d', '--debug',
                        action='store_true', dest='verbose', help='verbose output')
    args = parser.parse_args()
    try:
        puzzle_input = [line.strip() for line in fileinput.input(args.infile)]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print(f'Part one: {p1}')
        print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
