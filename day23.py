#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 23 module."""

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
    waiting = 0
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
                if param_modes and param_modes[0] == 2:
                    a += relative_base
                if input_q.empty():
                    waiting += 1
                    mem[a] = -1
                    if waiting > 1:
                        yield None
                else:
                    waiting = 0
                    mem[a] = input_q.get()
            else:
                params = get_params(mem, [a], param_modes, relative_base)
                if opcode == 4:
                    waiting = 0
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


def run_network(puzzle_input, use_nat=False):
    nics = []
    in_queues = []
    out_queues = []
    for i in range(50):
        q = Queue()
        q.put(i)
        gen = run_intcode(list(puzzle_input), q)
        nics.append(gen)
        in_queues.append(q)
        out_queues.append([])

    nat_packet = (None, None)
    last_y = None

    not_idle = list(range(50))

    while True:
        try:
            while not_idle:
                i = not_idle.pop(0)
                gen = nics[i]
                while True:
                    out = next(gen)
                    if out is None:
                        break
                    out_queues[i].append(out)
                    if len(out_queues[i]) == 3:
                        dst, x, y = out_queues[i]
                        # print(f'{i:02} -> {dst:02} ({x}, {y})')
                        if dst == 255:
                            nat_packet = (x, y)
                            if not use_nat:
                                return nat_packet
                        else:
                            in_queues[dst].put(x)
                            in_queues[dst].put(y)
                            if dst not in not_idle:
                                not_idle.append(dst)
                        out_queues[i].clear()
            if use_nat:
                x, y = nat_packet
                if x is None or y is None:
                    raise RuntimeError('network will idle forever')
                # print(f'IDLE 255 -> 00 {nat_packet}')
                if y == last_y:
                    break
                last_y = y
                in_queues[0].put(x)
                in_queues[0].put(y)
                not_idle = list(range(50))
                nat_packet = (None, None)
        except StopIteration:
            break
    return nat_packet


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    _, p1 = run_network(puzzle_input)
    _, p2 = run_network(puzzle_input, True)
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
