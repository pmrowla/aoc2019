#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 15 module."""

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


def get_direction(pos, dst):
    if dst[0] == pos[0] and dst[1] == pos[1] + 1:
        return 1
    elif dst[0] == pos[0] and dst[1] == pos[1] - 1:
        return 2
    elif dst[0] == pos[0] - 1 and dst[1] == pos[1]:
        return 3
    elif dst[0] == pos[0] + 1 and dst[1] == pos[1]:
        return 4
    raise ValueError('pos/dst must be adjacent points')


def print_grid(grid):
    xs, ys = zip(*grid.keys())
    rows = []
    for y in range(min(ys), max(ys) + 1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            row.append(grid.get((x, y), '#'))
        rows.append(''.join(row))
    print('\n'.join(rows))


def adjacent(pos):
    x, y = pos
    for point in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        yield point


def neighbors(grid, pos):
    for point in adjacent(pos):
        if grid[point] != '#':
            yield point


def map_adjacent(grid, pos, gen, q):
    for point in adjacent(pos):
        if point not in grid:
            q.put(get_direction(pos, point))
            status = next(gen)
            if status == 0:
                grid[point] = '#'
            elif status <= 2:
                if status == 1:
                    grid[point] = '.'
                else:
                    grid[point] = 'O'
                map_adjacent(grid, point, gen, q)
                q.put(get_direction(point, pos))
                next(gen)
            else:
                raise ValueError('unexpected droid status')


def make_grid(puzzle_input):
    grid = {(0, 0): 'D'}
    x = y = 0
    q = Queue()
    gen = run_intcode(list(puzzle_input), q)
    map_adjacent(grid, (x, y), gen, q)
    return grid


def dijkstra(grid, src, dst=None):
    dist = {k: len(grid) for k, v in grid.items() if v != '#'}
    prev = {k: None for k, v in grid.items() if v != '#'}
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


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    grid = make_grid(puzzle_input)
    dst = None
    for k, v in grid.items():
        if v == 'O':
            dst = k
            break
    dist, _ = dijkstra(grid, (0, 0), dst)
    p1 = dist[dst]
    dist, _ = dijkstra(grid, dst)
    p2 = sorted(dist.values())[-1]
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
