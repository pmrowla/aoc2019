#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 24 module."""

from collections import deque


def adjacent(pos, size=5):
    x, y = pos
    for px, py in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if px < 0 or py < 0 or px >= size or py >= size:
            continue
        yield px, py


def step(grid):
    next_grid = []
    for y, row in enumerate(grid):
        next_row = []
        for x, c in enumerate(row):
            count = 0
            for px, py in adjacent((x, y)):
                if grid[py][px] == '#':
                    count += 1
            if c == '#':
                if count == 1:
                    next_row.append('#')
                else:
                    next_row.append('.')
            else:
                if count in (1, 2):
                    next_row.append('#')
                else:
                    next_row.append('.')
        next_grid.append(tuple(next_row))
    return tuple(next_grid)


def biodiversity(grid):
    x = 0
    rating = 0
    for row in grid:
        for c in row:
            if c == '#':
                rating += pow(2, x)
            x += 1
    return rating


def adjacent_recursive(pos, step, size=5):
    x, y, z = pos
    for px, py in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if px >= 0 and py >= 0 and px < size and py < size:
            if not (px == 2 and py == 2):
                yield px, py, z

    z_max = 2 * step + 1
    if y == 0:
        pz = z + 1
        if pz <= z_max:
            yield 2, 1, pz
    elif y == size - 1:
        pz = z + 1
        if pz <= z_max:
            yield 2, 3, pz
    if x == 0:
        pz = z + 1
        if pz <= z_max:
            yield 1, 2, pz
    elif x == size - 1:
        pz = z + 1
        if pz <= z_max:
            yield 3, 2, pz

    if (x, y) == (2, 1):
        pz = z - 1
        if pz >= 0:
            for px in range(size):
                yield px, 0, pz
    elif (x, y) == (1, 2):
        pz = z - 1
        if pz >= 0:
            for py in range(size):
                yield 0, py, pz
    elif (x, y) == (3, 2):
        pz = z - 1
        if pz >= 0:
            for py in range(size):
                yield size - 1, py, pz
    elif (x, y) == (2, 3):
        pz = z - 1
        if pz >= 0:
            for px in range(size):
                yield px, size - 1, pz


def empty_grid():
    return [
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '?', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
    ]


def step_recursive(recursive_grid, step):
    next_recursive_grid = deque()
    recursive_grid.appendleft(empty_grid())
    recursive_grid.append(empty_grid())

    for z, grid in enumerate(recursive_grid):
        next_grid = []
        for y, row in enumerate(grid):
            next_row = []
            for x, c in enumerate(row):
                if (x, y) == (2, 2):
                    next_row.append('?')
                    continue
                count = 0
                for px, py, pz in adjacent_recursive((x, y, z), step):
                    if recursive_grid[pz][py][px] == '#':
                        count += 1
                if c == '#':
                    if count == 1:
                        next_row.append('#')
                    else:
                        next_row.append('.')
                else:
                    if count in (1, 2):
                        next_row.append('#')
                    else:
                        next_row.append('.')
            next_grid.append(next_row)
        next_recursive_grid.append(next_grid)
    return next_recursive_grid


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    init_grid = []
    for row in puzzle_input:
        init_grid.append(tuple([c for c in row]))

    grid = tuple(init_grid)
    seen = set()
    while grid not in seen:
        seen.add(grid)
        grid = step(grid)
    p1 = biodiversity(grid)

    recursive_grid = deque([init_grid])
    for i in range(200):
        recursive_grid = step_recursive(recursive_grid, i)
    p2 = sum([c == '#' for grid in recursive_grid for row in grid for c in row])
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
