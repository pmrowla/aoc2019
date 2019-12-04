#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 4 module."""

from tqdm import tqdm


def valid_passwords(low, high):
    valid_p1 = []
    valid_p2 = []
    for i in tqdm(range(low, high + 1)):
        double = False
        repeats = set()
        repeat_count = 0
        max_digit = 0
        prev = None
        for c in str(i):
            if int(c) < max_digit:
                break
            max_digit = max(int(c), max_digit)
            if prev and prev == c:
                repeat_count += 1
                double = True
            else:
                repeats.add(repeat_count)
                repeat_count = 1
            prev = c
        else:
            repeats.add(repeat_count)
            if double:
                valid_p1.append(i)
            if 2 in repeats:
                valid_p2.append(i)
    return valid_p1, valid_p2


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    low, high = puzzle_input
    p1, p2 = valid_passwords(low, high)
    return len(p1), len(p2)


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
        for line in fileinput.input(args.infile):
            line = line.strip()
            if not line:
                continue
            puzzle_input = [int(x) for x in line.split('-')]
            p1, p2 = process(puzzle_input, verbose=args.verbose)
            print(f'Part one: {p1}')
            print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
