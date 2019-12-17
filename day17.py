#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 17 module."""

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


def adjacent(pos):
    x, y = pos
    for point in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        yield point


def neighbors(grid, pos):
    for x, y in adjacent(pos):
        try:
            if grid[y][x] == '#':
                yield (x, y)
        except IndexError:
            continue


def make_grid(puzzle_input):
    q = Queue()
    gen = run_intcode(list(puzzle_input), q)
    grid = []
    while True:
        try:
            c = next(gen)
            grid.append(chr(c))
        except StopIteration:
            break
    return list(''.join(grid).split('\n'))


def find_intersections(grid):
    intersections = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '#' and len(list(neighbors(grid, (x, y)))) == 4:
                intersections.add((x, y))
    return intersections


DIRECTIONS = '^>v<'


def get_deltas(dir_):
    x_delta = y_delta = 0
    if dir_ == 0:
        y_delta = -1
    elif dir_ == 1:
        x_delta = 1
    elif dir_ == 2:
        y_delta = 1
    else:
        x_delta = -1
    return x_delta, y_delta


def is_valid(grid, pos):
    x, y = pos
    try:
        if grid[y][x] == '#':
            return True
    except IndexError:
        pass
    return False


def get_route(grid):
    dir_ = None
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c in DIRECTIONS:
                dir_ = DIRECTIONS.index(c)
                break
        if dir_ is not None:
            break
    route = []
    visited = set()
    move_dist = 0
    while True:
        visited.add((x, y))
        x_delta, y_delta = get_deltas(dir_)
        if is_valid(grid, (x + x_delta, y + y_delta)):
            x += x_delta
            y += y_delta
            move_dist += 1
            continue

        # need to turn
        if move_dist:
            route.append(str(move_dist))
            move_dist = 0
        dir_ = (dir_ - 1) % 4
        x_delta, y_delta = get_deltas(dir_)
        if is_valid(grid, (x + x_delta, y + y_delta)):
            route.append('L')
            continue
        dir_ = (dir_ + 2) % 4
        x_delta, y_delta = get_deltas(dir_)
        if is_valid(grid, (x + x_delta, y + y_delta)):
            route.append('R')
            continue
        break
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '#' and (x, y) not in visited:
                raise ValueError(f'did not visit ({x}, {y})')
    return route


def run_movement(puzzle_input, main, a, b, c):
    q = Queue()
    prog = list(puzzle_input)
    prog[0] = 2
    for i, x in enumerate('{}\n'.format(','.join(main))):
        q.put(ord(x))
    for f in a, b, c:
        for i, x in enumerate('{}\n'.format(','.join(f))):
            q.put(ord(x))
    q.put(ord('n'))
    q.put(ord('\n'))
    msg = []
    gen = run_intcode(prog, q)
    out = 0
    while True:
        try:
            c = next(gen)
            if c > 127:
                out = c
            else:
                msg.append(chr(c))
        except StopIteration:
            break
    print(''.join(msg))
    return out


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    grid = make_grid(puzzle_input)
    print('\n'.join(grid))
    p1 = sum([x * y for x, y in find_intersections(grid)])
    route = get_route(grid)
    route_s = ''.join(route)
    a = ['L', '12', 'L', '10', 'R', '8', 'L', '12']
    a_s = ''.join(a)
    b = ['R', '8', 'R', '10', 'R', '12']
    b_s = ''.join(b)
    c = ['L', '10', 'R', '12', 'R', '8']
    c_s = ''.join(c)
    i = 0
    moves = []
    while i < len(route_s):
        if route_s[i:].startswith(a_s):
            moves.append('A')
            i += len(a_s)
        elif route_s[i:].startswith(b_s):
            moves.append('B')
            i += len(b_s)
        elif route_s[i:].startswith(c_s):
            moves.append('C')
            i += len(c_s)
        else:
            raise ValueError('cannot make movement routine')
    p2 = run_movement(puzzle_input, moves, a, b, c)
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
