#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 20 module."""

import itertools
from heapq import heappush, heappop
from string import ascii_uppercase


class PrioQueue(object):

    REMOVED = (-1, -1, -1)

    def __init__(self):
        self.q = []
        self.entries = {}
        self._count = itertools.count()

    def add(self, item, prio=0):
        """Add or update priority q entry."""
        if item in self.entries:
            self.remove(item)
        count = next(self._count)
        entry = (prio, count, item)
        self.entries[item] = entry
        heappush(self.q, entry)

    def remove(self, item):
        entry = self.entries.pop(item)
        entry[-1] = self.REMOVED

    def pop(self):
        while self.q:
            prio, count, item = heappop(self.q)
            if item is not self.REMOVED:
                del self.entries[item]
                return item
        raise KeyError('pop from empty queue')

    def empty(self):
        return len(self.q) == 0


def adjacent(pos):
    x, y, z = pos
    for point in [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z)]:
        yield point


def neighbors(grid, portal_map, pos, recursive=False):
    for point in adjacent(pos):
        x, y, z = point
        if y < 0 or x < 0 or y >= len(grid) or x >= len(grid[0]):
            continue
        c = grid[y][x]
        if c == '.':
            yield point
    x, y, z = pos
    if (x, y) in portal_map:
        (x, y), change = portal_map[(x, y)]
        if recursive:
            z += change
        if z >= 0:
            yield (x, y, z)


def dijkstra(grid, portal_map, src, dst=None, recursive=False):
    dist = {}
    prev = {}
    q = PrioQueue()

    max_dist = len(grid) * len(grid[0])
    if recursive:
        max_levels = len(portal_map) / 2
        max_dist *= max_levels

    visited = set()
    q.add(src, max_dist)
    dist[src] = 0

    while not q.empty():
        pos = q.pop()
        if dst is not None and pos == dst:
            break
        visited.add(pos)
        x, y, z = pos
        for point in neighbors(grid, portal_map, pos, recursive):
            if point in visited:
                continue
            px, py, pz = point
            alt = dist[pos] + 1
            if point not in dist or alt < dist[point]:
                dist[point] = alt
                prev[point] = pos
                q.add(point, alt)

    return dist, prev


def get_portals(grid):
    portals = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c in ascii_uppercase:
                portal = pos = None
                if x < len(row) - 1 and row[x + 1] in ascii_uppercase:
                    portal = f'{c}{row[x + 1]}'
                    for px, py in [(x - 1, y), (x + 2, y)]:
                        if px >= 0 and px < len(row) and grid[py][px] == '.':
                            pos = px, py
                            break
                elif y < len(grid) - 1 and grid[y + 1][x] in ascii_uppercase:
                    portal = f'{c}{grid[y + 1][x]}'
                    for px, py in [(x, y - 1), (x, y + 2)]:
                        if py >= 0 and py < len(grid) and grid[py][px] == '.':
                            pos = px, py
                            break
                if portal is not None and pos is not None:
                    if portal not in portals:
                        portals[portal] = []
                    px, py = pos
                    if px == 2 or px == (len(row) - 3) or py == 2 or py == (len(grid) - 3):
                        portals[portal].insert(0, pos)
                    else:
                        portals[portal].append(pos)
    portal_map = {}
    for k, v in portals.items():
        if len(v) == 2:
            a, b = v
            portal_map[a] = (b, -1)
            portal_map[b] = (a, 1)
    return portals, portal_map


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    grid = list(puzzle_input)
    portals, portal_map = get_portals(grid)
    start = portals['AA'][0] + (0,)
    end = portals['ZZ'][0] + (0,)
    dist, prev = dijkstra(grid, portal_map, start, end)
    if prev.get(end) is not None:
        p1 = dist[end]
    dist, prev = dijkstra(grid, portal_map, start, end, True)
    if prev.get(end) is not None:
        p2 = dist[end]
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
        puzzle_input = [line.rstrip('\n') for line in fileinput.input(args.infile) if line.rstrip('\n')]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print(f'Part one: {p1}')
        print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
