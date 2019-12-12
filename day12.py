#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 12 module."""

import re
from itertools import combinations
from math import gcd


POS_RE = re.compile(r'(?:<\s*x=(?P<x>-?\d+),\s*y=(?P<y>-?\d+),\s*z=(?P<z>-?\d+))')


def _lcm(a, b):
    return abs(a * b) // gcd(a, b)


def lcm(*args):
    if not args:
        raise ValueError
    n = args[0]
    for i in args[1:]:
        n = _lcm(n, i)
    return n


class Moon:

    def __init__(self, pos, v=(0, 0, 0)):
        self.pos = tuple(pos)
        self.v = v

    def __str__(self):
        return f'pos={self.pos}, v={self.v}'

    def __hash__(self):
        return hash(self.pos + self.v)

    @property
    def pot(self):
        return sum([abs(n) for n in self.pos])

    @property
    def kin(self):
        return sum([abs(n) for n in self.v])

    @property
    def energy(self):
        return self.pot * self.kin


def apply_gravity(moons):
    rel = []
    for i, j in combinations(range(len(moons)), 2):
        a = moons[i]
        b = moons[j]
        av = []
        bv = []
        k = 0
        for i, delta in enumerate([bn - an for an, bn in zip(a.pos, b.pos)]):
            if delta > 0:
                av.append(a.v[i] + 1)
                bv.append(b.v[i] - 1)
                k = 1
            elif delta < 0:
                av.append(a.v[i] - 1)
                bv.append(b.v[i] + 1)
                rel.append((i, j, -1))
                k = -1
            else:
                av.append(a.v[i])
                bv.append(b.v[i])
        rel.append((i, j, k, a.v, b.v))
        a.v = tuple(av)
        b.v = tuple(bv)
    return rel


def apply_velocity(moons):
    for m in moons:
        new_pos = []
        for i in range(len(m.pos)):
            new_pos.append(m.pos[i] + m.v[i])
        m.pos = tuple(new_pos)


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    moons = []
    initial = []
    for line in puzzle_input:
        m = POS_RE.match(line)
        if m:
            d = m.groupdict()
            pos = [int(d[k]) for k in 'xyz']
            moons.append(Moon(pos))
            initial.append(Moon(pos))
    step = 0
    initial_x = [(m.pos[0], m.v[0]) for m in moons]
    initial_y = [(m.pos[1], m.v[1]) for m in moons]
    initial_z = [(m.pos[2], m.v[2]) for m in moons]
    x_period = None
    y_period = None
    z_period = None
    while p1 is None or p2 is None:
        apply_gravity(moons)
        apply_velocity(moons)
        step += 1
        if step == 1000:
            p1 = sum([m.energy for m in moons])
        x = [(m.pos[0], m.v[0]) for m in moons]
        if x == initial_x and x_period is None:
            x_period = step
        y = [(m.pos[1], m.v[1]) for m in moons]
        if y == initial_y and y_period is None:
            y_period = step
        z = [(m.pos[2], m.v[2]) for m in moons]
        if z == initial_z and z_period is None:
            z_period = step
        if x_period and y_period and z_period:
            p2 = lcm(x_period, y_period, z_period)
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
