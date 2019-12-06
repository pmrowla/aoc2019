#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 6 module."""


def chain_orbits(orbits, k):
    chain = []
    while True:
        v = orbits[k]
        chain.append(v)
        if v == 'COM':
            break
        k = v
    return chain


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    orbits = {}
    for v, k in puzzle_input:
        orbits[k] = v
    chains = {k: chain_orbits(orbits, k) for k in orbits}
    p1 = sum([len(chain) for chain in chains.values()])
    you = set(chains['YOU'])
    san = set(chains['SAN'])
    p2 = len(you.difference(san)) + len(san.difference(you))
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
        puzzle_input = [line.strip().split(')') for line in fileinput.input(args.infile) if line.strip()]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print(f'Part one: {p1}')
        print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
