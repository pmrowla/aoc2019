#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 18 module."""

from string import ascii_lowercase, ascii_uppercase


def adjacent(pos):
    x, y = pos
    for point in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        yield point


def neighbors(grid, pos):
    for point in adjacent(pos):
        x, y = point
        if y < 0 or x < 0 or y >= len(grid) or x >= len(grid[0]):
            continue
        c = grid[y][x]
        if c != '#':
            yield point


def dijkstra(grid, src, dst=None):
    dist = {}
    prev = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != '#':
                dist[(x, y)] = len(grid) * len(grid[0])
                prev[(x, y)] = None
    unvisited = set(dist.keys())
    dist[src] = 0

    while unvisited:
        pos = sorted(list(unvisited), key=lambda x: dist[x])[0]
        unvisited.remove(pos)
        if dst is not None and pos == dst:
            break
        for point in neighbors(grid, pos):
            alt = dist[pos] + 1
            if alt < dist[point]:
                dist[point] = alt
                prev[point] = pos
    return dist, prev


def parse_grid(grid, p2=False):
    start = None
    keys = {}
    doors = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '@':
                start = (x, y)
            elif c in ascii_lowercase:
                keys[c] = (x, y)
            elif c in ascii_uppercase:
                doors[c] = (x, y)
    return start, keys, doors


def key_distances(grid, start, keys, doors):
    """Return distance start to any keys, and doors that must be passed."""
    dist, prev = dijkstra(grid, start)
    dest_keys = {}
    for k, pos in keys.items():
        if pos == start:
            continue
        p = pos
        if prev[pos] is None:
            continue
        needed_keys = set()
        while p != start:
            p = prev[p]
            if p in doors.values():
                needed_keys.add(grid[p[1]][p[0]].lower())
        dest_keys[k] = (dist[pos], frozenset(needed_keys))
    return dest_keys


def min_route_dist(robot_keys, key_dists):

    known_dists = {}

    def _min_dist(keys, remaining_keys):
        nonlocal key_dists
        nonlocal known_dists
        if (keys, remaining_keys) in known_dists:
            return known_dists[(keys, remaining_keys)]

        min_dist = None
        for k in remaining_keys:
            for robot_key in keys:
                if k not in key_dists[robot_key]:
                    continue
                dist, needed_keys = key_dists[robot_key][k]
                if needed_keys.intersection(remaining_keys):
                    continue
                new_remaining = set(remaining_keys)
                new_remaining.remove(k)
                new_keys = set(keys)
                new_keys.remove(robot_key)
                new_keys.add(k)
                if new_remaining:
                    dist += _min_dist(frozenset(new_keys), frozenset(new_remaining))
                if min_dist is None:
                    min_dist = dist
                else:
                    min_dist = min(dist, min_dist)
        known_dists[(keys, remaining_keys)] = min_dist
        return min_dist

    min_dist = None
    for robot_key in robot_keys:
        for key, (dist, needed_keys) in key_dists[robot_key].items():
            if needed_keys:
                continue
            remaining = set([k for k in key_dists if not k.startswith('@')])
            remaining.remove(key)
            keys = set(robot_keys)
            keys.remove(robot_key)
            keys.add(key)
            dist += _min_dist(frozenset(keys), frozenset(remaining))
            if min_dist is None:
                min_dist = dist
            else:
                min_dist = min(dist, min_dist)

    return min_dist


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    grid = [list(row) for row in puzzle_input]
    start, keys, doors = parse_grid(grid)
    robots = [('@', start)]
    key_dists = {}
    for i, (key, pos) in enumerate(robots):
        key_dists[key] = key_distances(grid, pos, keys, doors)
    for k, pos in keys.items():
        key_dists[k] = key_distances(grid, pos, keys, doors)
    p1 = min_route_dist(['@'], key_dists)

    robots = []
    x, y = start
    for i, pos in enumerate([(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]):
        x, y = pos
        key = f'@{i}'
        grid[y][x] = '@'
        robots.append((key, pos))
    x, y = start
    for pos in [(x, y - 1), (x - 1, y), (x, y), (x + 1, y), (x, y + 1)]:
        x, y = pos
        grid[y][x] = '#'

    key_dists = {}
    for i, (key, pos) in enumerate(robots):
        key_dists[key] = key_distances(grid, pos, keys, doors)
    for k, pos in keys.items():
        key_dists[k] = key_distances(grid, pos, keys, doors)
    p2 = min_route_dist([k for k, pos in robots], key_dists)

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
