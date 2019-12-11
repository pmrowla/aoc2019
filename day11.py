#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 11 module."""

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


def paint(puzzle_input, starting_panel=0):
    grid = {(0, 0): starting_panel}
    x = y = 0
    cur_dir = 0
    painted = set()
    q = Queue()
    gen = run_intcode(list(puzzle_input), q)
    while True:
        try:
            cur_panel = grid.get((x, y), 0)
            q.put(cur_panel)
            color = next(gen)
            grid[(x, y)] = color
            painted.add((x, y))
            turn = next(gen)
            if turn == 0:
                cur_dir = (cur_dir - 1) % 4
            else:
                cur_dir = (cur_dir + 1) % 4
            if cur_dir == 0:
                y += 1
            elif cur_dir == 1:
                x += 1
            elif cur_dir == 2:
                y -= 1
            else:
                x -= 1
        except StopIteration:
            break
    return painted, grid


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    painted, _ = paint(puzzle_input)
    p1 = len(painted)
    painted, grid = paint(puzzle_input, 1)
    min_x = max_x = None
    min_y = max_y = None
    for x, y in painted:
        if min_x is None:
            min_x = max_x = x
            min_y = max_y = y
        else:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
    out = ['']
    for y in range(max_y, min_y - 1, -1):
        line = []
        for x in range(min_x, max_x + 1):
            color = grid.get((x, y), 0)
            if color == 0:
                line.append(' ')
            else:
                line.append('#')
        out.append(''.join(line))
    p2 = '\n'.join(out)
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
