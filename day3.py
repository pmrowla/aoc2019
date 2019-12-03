#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 3 module."""


def visit(wire):
    visited = set()
    step = x = y = 0
    steps = {}
    for path in wire:
        direction = path[0]
        distance = int(path[1:])
        for i in range(distance):
            if direction == 'R':
                x += 1
            elif direction == 'L':
                x -= 1
            elif direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            else:
                raise ValueError(f'unexpected direction "{direction}"')
            step += 1
            visited.add((x, y))
            if (x, y) not in steps:
                steps[(x, y)] = step
    if (0, 0) in visited:
        visited.remove((0, 0))
    return visited, steps


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    wires = []
    for line in puzzle_input:
        wires.append(visit([pos.upper() for pos in line.split(',')]))
    intersections = wires[0][0].intersection(wires[1][0])
    manhattan_distances = [abs(pos[0]) + abs(pos[1]) for pos in intersections]
    steps = [wires[0][1][pos] + wires[1][1][pos] for pos in intersections]
    p1 = sorted(manhattan_distances)[0]
    p2 = sorted(steps)[0]
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
        puzzle_input = [line.strip() for line in fileinput.input(args.infile) if line]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print(f'Part one: {p1}')
        print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
