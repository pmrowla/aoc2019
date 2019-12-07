#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 7 module."""

from itertools import cycle, permutations
from queue import Queue


def get_params(program, input_params, modes):
    params = []
    for i, param in enumerate(input_params):
        if i >= len(modes):
            mode = 0
        else:
            mode = modes[i]
        if mode == 0:
            params.append(program[param])
        elif mode == 1:
            params.append(param)
        else:
            raise ValueError(f'unexpected mode {mode}')
    return params


def run_intcode(program, input_q):
    pc = 0
    output = None
    while pc < len(program):
        opcode = program[pc] % 100
        param_modes = [int(c) for c in str(program[pc] // 100)]
        param_modes.reverse()
        if opcode == 99:
            break
        if opcode in (1, 2, 7, 8,):
            a, b, c = program[pc+1 : pc+4]
            params = get_params(program, [a, b], param_modes)
            if opcode == 1:
                program[c] = params[0] + params[1]
            elif opcode == 2:
                program[c] = params[0] * params[1]
            elif opcode == 7:
                if params[0] < params[1]:
                    program[c] = 1
                else:
                    program[c] = 0
            elif opcode == 8:
                if params[0] == params[1]:
                    program[c] = 1
                else:
                    program[c] = 0
            pc += 4
        elif opcode in (3, 4):
            a = program[pc+1]
            if opcode == 3:
                if input_q.empty():
                    raise ValueError('input instruction w/empty input queue')
                program[a] = input_q.get()
            elif opcode == 4:
                params = get_params(program, [a], param_modes)
                output = params[0]
                yield output
            pc += 2
        elif opcode in (5, 6):
            a, b = program[pc+1 : pc+3]
            params = get_params(program, [a, b], param_modes)
            if (opcode == 5 and params[0] != 0) or (opcode == 6 and params[0] == 0):
                pc = params[1]
            else:
                pc += 3
        else:
            raise ValueError(f'unexpected opcode {opcode}')
    return output


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    output_signals = []
    for perm in permutations(range(5)):
        output = 0
        for i in perm:
            q = Queue()
            q.put(i)
            q.put(output)
            output = next(run_intcode(list(puzzle_input), q))
        output_signals.append((perm, output))
    p1 = sorted(output_signals, key=lambda x: x[1])[-1]

    output_signals = []
    for perm in permutations(range(5, 10)):
        amps = []
        for i in perm:
            q = Queue()
            q.put(i)
            amps.append((run_intcode(list(puzzle_input), q), q))

        output = 0
        for gen, q in cycle(amps):
            try:
                q.put(output)
                output = next(gen)
            except StopIteration:
                break
        output_signals.append((perm, output))
    p2 = sorted(output_signals, key=lambda x: x[1])[-1]
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
