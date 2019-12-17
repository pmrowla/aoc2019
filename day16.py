#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 16 module."""

from itertools import cycle

import numpy as np

from tqdm import tqdm


def pattern(index):
    out = []
    for n in [0, 1, 0, -1]:
        out.extend([n] * (index + 1))
    out.append(out.pop(0))
    out = out[index:] + out[:index]
    return cycle(out)


def phase(input_signal, start=0):
    output_signal = np.empty(len(input_signal), dtype=int)
    for i in range(start, len(input_signal) // 2 + 1):
        signal = input_signal[i:]
        output_signal[i] = abs(sum([a * b for a, b in zip(signal, pattern(i)) if b])) % 10
    last = 0
    stop = len(input_signal) // 2
    if (start - 1) > stop:
        stop = start - 1
    for i in range(len(input_signal) - 1, stop, -1):
        last = (input_signal[i] + last) % 10
        output_signal[i] = last
    return output_signal


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    signal = np.array([int(n) for n in puzzle_input])
    for i in tqdm(range(100)):
        signal = phase(signal)
    p1 = ''.join([str(n) for n in signal[:8]])

    offset = int(puzzle_input[:7])
    signal = np.array([int(n) for n in puzzle_input] * 10000)
    if offset <= len(signal) / 2:
        raise ValueError('unexpected offset')
    for i in tqdm(range(100)):
        signal = phase(signal, start=offset)
    p2 = ''.join([str(n) for n in signal[offset : offset+8]])
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
        for line in fileinput.input(args.infile):
            puzzle_input = line.strip()
            if not puzzle_input:
                continue
            p1, p2 = process(puzzle_input, verbose=args.verbose)
            print(f'Part one: {p1}')
            print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
