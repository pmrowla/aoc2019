#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 13 module."""

from collections import defaultdict


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


def run_intcode(program, input_f=None):
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
                if not input_f:
                    raise ValueError('no input func')
                if param_modes and param_modes[0] == 2:
                    a += relative_base
                # print('read input')
                mem[a] = input_f()
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


def count_blocks(tiles):
    return sum([v == 2 for v in tiles.values()])


def print_tiles(tiles):
    xs, ys = zip(*tiles.keys())
    rows = []
    tile = ' X#-*'
    for y in range(min(ys), max(ys) + 1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            tile_id = tiles[(x, y)]
            row.append(tile[tile_id])
        rows.append(''.join(row))
    print('\n'.join(rows))


def run_game(puzzle_input, play=False):
    tiles = {}
    score = 0
    prog = list(puzzle_input)
    if play:
        prog[0] = 2

    def move():
        for pos, tile_id in tiles.items():
            if tile_id == 3:
                px, _ = pos
            elif tile_id == 4:
                bx, _ = pos
        if bx > px:
            return 1
        if bx < px:
            return -1
        return 0

    gen = run_intcode(prog, input_f=move)
    while True:
        try:
            x = next(gen)
            y = next(gen)
            tile_id = next(gen)
            if x == -1 and y == 0:
                score = tile_id
            else:
                tiles[(x, y)] = tile_id
        except StopIteration:
            break
    return tiles, score


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    tiles, _ = run_game(puzzle_input)
    p1 = count_blocks(tiles)
    _, score = run_game(puzzle_input, play=True)
    p2 = score
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
