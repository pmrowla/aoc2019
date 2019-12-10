#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 10 module."""

import math


def detect_update(grid, a, b):
    ax, ay = a
    if a == b:
        grid[ay][ax] = '.'
        return
    bx, by = b
    y_delta = by - ay
    x_delta = bx - ax
    if y_delta == 0:
        if x_delta > 0:
            x_delta = 1
        else:
            x_delta = -1
    elif x_delta == 0:
        if y_delta > 0:
            y_delta = 1
        else:
            y_delta = -1
    else:
        d = math.gcd(abs(y_delta), abs(x_delta))
        y_delta //= d
        x_delta //= d
    y = by + y_delta
    x = bx + x_delta
    while y >= 0 and y < len(grid) and x >= 0 and x < len(grid[0]):
        if grid[y][x] == '#':
            grid[y][x] = '.'
        x += x_delta
        y += y_delta


def detectable(grid, pos):
    """Return detectable asteroids from pos."""
    grid = [list(row) for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '#':
                detect_update(grid, pos, (x, y))
    return grid


def dist(p, q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def vaporized(grid, pos):
    """Return list vaporized positions in order."""
    pos_angles = []
    px, py = pos
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) == pos:
                continue
            if grid[y][x] == '#':
                x_delta = x - px
                y_delta = py - y
                angle = math.atan2(x_delta, y_delta)
                angle = (360 + math.degrees(angle)) % 360
                pos_angles.append(((x, y), angle, dist(pos, (x, y))))
    # sort by angle then distance
    pos_angles.sort(key=lambda x: (x[1], x[2]))
    output = []
    i = 0
    prev_angle = None
    while i < len(pos_angles):
        pos, angle, _ = pos_angles[i]
        if angle == prev_angle:
            i += 1
            if i == len(pos_angles):
                i = 0
        else:
            del pos_angles[i]
            prev_angle = angle
            output.append(pos)
    return output


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    detect_counts = []
    grid = [list(row) for row in puzzle_input]
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '#':
                d = detectable(grid, (x, y))
                count = sum([c == '#' for row in d for c in row])
                detect_counts.append(((x, y), count))
    p1 = sorted(detect_counts, key=lambda x: x[1])[-1]
    pos, _ = p1
    pos = vaporized(grid, pos)[199]
    p2 = pos[0] * 100 + pos[1]
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
        puzzle_input = [line.strip() for line in fileinput.input(args.infile) if line.strip()]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print(f'Part one: {p1}')
        print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
