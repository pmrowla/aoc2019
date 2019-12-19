#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 19 module."""

from collections import defaultdict
from queue import Queue


def get_params(mem, input_params, modes, base):
    params = []
    for i, param in enumerate(input_params):
        if i >= len(modes):
            mode = 0
        else:
            mode = modes[i]
        if mode == 0:
            params.append(mem[param])
        elif mode == 1:
            params.append(param)
        elif mode == 2:
            params.append(mem[param+base])
        else:
            raise ValueError(f'unexpected mode {mode}')
    return params


def run_intcode(program, input_q):
    pc = 0
    output = None
    relative_base = 0
    mem = defaultdict(int)
    for i, data in enumerate(program):
        mem[i] = data
    while pc in mem:
        opcode = mem[pc] % 100
        param_modes = [int(c) for c in str(mem[pc] // 100)]
        param_modes.reverse()
        if opcode == 99:
            break
        if opcode in (1, 2, 7, 8,):
            a, b, c = (mem[pc+1], mem[pc+2], mem[pc+3])
            params = get_params(mem, [a, b], param_modes, relative_base)
            if len(param_modes) >= 3 and param_modes[2] == 2:
                c += relative_base
            if opcode == 1:
                mem[c] = params[0] + params[1]
            elif opcode == 2:
                mem[c] = params[0] * params[1]
            elif opcode == 7:
                if params[0] < params[1]:
                    mem[c] = 1
                else:
                    mem[c] = 0
            elif opcode == 8:
                if params[0] == params[1]:
                    mem[c] = 1
                else:
                    mem[c] = 0
            pc += 4
        elif opcode in (3, 4, 9):
            a = mem[pc+1]
            if opcode == 3:
                if input_q.empty():
                    raise ValueError('input instruction w/empty input queue')
                if param_modes and param_modes[0] == 2:
                    a += relative_base
                mem[a] = input_q.get()
            else:
                params = get_params(mem, [a], param_modes, relative_base)
                if opcode == 4:
                    output = params[0]
                    yield output
                elif opcode == 9:
                    relative_base += params[0]
            pc += 2
        elif opcode in (5, 6):
            a, b = (mem[pc+1], mem[pc+2])
            params = get_params(mem, [a, b], param_modes, relative_base)
            if (opcode == 5 and params[0] != 0) or (opcode == 6 and params[0] == 0):
                pc = params[1]
            else:
                pc += 3
        else:
            raise ValueError(f'unexpected opcode {opcode}')
    return output


pos_cache = {}


def check_pos(puzzle_input, pos):
    if pos in pos_cache:
        return pos_cache[pos]
    x, y = pos
    q = Queue()
    gen = run_intcode(list(puzzle_input), q)
    q.put(x)
    q.put(y)
    pos_cache[pos] = next(gen)
    return pos_cache[pos]


def make_grid(puzzle_input):
    grid = []
    for y in range(50):
        row = []
        for x in range(50):
            row.append(check_pos(puzzle_input, (x, y)))
        grid.append(row)
    return grid


def print_grid(grid):
    for row in grid:
        out = []
        for n in row:
            if n:
                out.append('#')
            else:
                out.append('.')
        print(''.join(out))


def find_square(puzzle_input, size=100):
    y = -1 + size
    x_start = 0
    while True:
        y += 1
        for x in range(x_start, y + 1):
            n = check_pos(puzzle_input, (x, y))
            if n:
                x_start = x
                break
        else:
            continue
        if not check_pos(puzzle_input, (x_start + size - 1, y)):
            continue
        width = 10
        while check_pos(puzzle_input, (x_start + width, y)):
            width += 1
        for x in range(x_start, x_start + width - size + 1):
            if not check_pos(puzzle_input, (x, y + size - 1)):
                continue
            return x, y


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    grid = make_grid(puzzle_input)
    print_grid(grid)
    p1 = sum([n for row in grid for n in row])
    x, y = find_square(puzzle_input)
    print(f'({x}, {y})')
    p2 = x * 10000 + y
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
