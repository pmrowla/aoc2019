#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 14 module."""

import math
from collections import defaultdict


def parse_reactions(puzzle_input):
    reactions = {}
    for line in puzzle_input:
        inputs = []
        in_s, out_s = line.split('=>')
        out_count, out_name = out_s.strip().split()
        out_count = int(out_count)
        for in_ in in_s.strip().split(','):
            count, name = in_.strip().split()
            inputs.append((int(count), name))
        reactions[out_name] = (out_count, inputs)
    return reactions


def produce(name, quantity, reactions, total_produced, excess):
    if excess[name] >= quantity:
        excess[name] -= quantity
        return
    elif excess[name]:
        quantity -= excess[name]
        excess[name] = 0

    if name == 'ORE':
        num_produced = quantity
    else:
        output_qty, inputs = reactions[name]
        multiplier = math.ceil(quantity / output_qty)
        for in_qty, in_name in inputs:
            produce(in_name, in_qty * multiplier, reactions, total_produced, excess)
        num_produced = output_qty * multiplier
    total_produced[name] += num_produced
    if num_produced > quantity:
        excess[name] += num_produced - quantity


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    reactions = parse_reactions(puzzle_input)
    total_produced = defaultdict(int)
    excess = defaultdict(int)
    produce('FUEL', 1, reactions, total_produced, excess)
    p1 = total_produced['ORE']

    available_ore = 10 ** 12
    lb = 0
    ub = 0
    fuel = 2
    while True:
        total_produced = defaultdict(int)
        excess = defaultdict(int)
        produce('FUEL', fuel, reactions, total_produced, excess)
        if total_produced['ORE'] < available_ore:
            fuel **= 2
        else:
            ub = fuel
            break
    while True:
        fuel = (ub + lb) // 2
        excess = defaultdict(int)
        total_produced = defaultdict(int)
        produce('FUEL', fuel, reactions, total_produced, excess)
        if total_produced['ORE'] <= available_ore:
            lb = fuel
        else:
            ub = fuel
        if ub - lb <= 1:
            p2 = lb
            break
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
