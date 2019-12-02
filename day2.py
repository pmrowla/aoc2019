#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 2 module."""


from tqdm import tqdm


def run_intcode(program):
    pc = 0
    while pc < len(program):
        opcode = program[pc]
        if opcode == 99:
            break
        elif opcode in (1, 2):
            a, b, c = program[pc+1 : pc+4]
            if opcode == 1:
                program[c] = program[a] + program[b]
            elif opcode == 2:
                program[c] = program[a] * program[b]
        else:
            raise ValueError('unexpected opcode')
        pc += 4
    return program


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    prog = list(puzzle_input)
    prog[1] = 12
    prog[2] = 2
    p1 = run_intcode(prog)[0]
    for i in tqdm(range(100)):
        for j in range(100):
            prog = list(puzzle_input)
            prog[1] = i
            prog[2] = j
            if run_intcode(prog)[0] == 19690720:
                p2 = 100 * i + j
                break
        if p2 is not None:
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
        puzzle_input = [int(x) for x in ''.join(fileinput.input(args.infile)).split(',') if x.strip()]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print(f'Part one: {p1}')
        print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
