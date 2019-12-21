#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 21 module."""

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
                    raise ValueError('empty input q')
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


def run_springdroid(puzzle_input, script):
    prog = list(puzzle_input)

    q = Queue()
    for line in script:
        for c in line:
            q.put(ord(c))
        q.put(ord('\n'))

    gen = run_intcode(prog, q)
    output = []
    damage = 0
    while True:
        try:
            out = next(gen)
            if out > 127:
                damage = out
            else:
                c = chr(out)
                if c == '\n':
                    print(''.join(output))
                    output = []
                else:
                    output.append(c)
        except StopIteration:
            break
    return damage


def process(puzzle_input, verbose=False):
    p1 = p2 = None

    base_script = [
        'NOT A T',  # T = !A
        'NOT B J',  # J = !B
        'OR T J',   # J = !A || !B
        'NOT C T',  # T = !C
        'OR T J',   # J = !A || !B || !C
        'AND D J',  # J = (!A || !B || !C) && D
    ]
    script = base_script + [
        'WALK',
    ]
    p1 = run_springdroid(puzzle_input, script)

    script = base_script + [
        'NOT I T',  # T = !I
        'NOT T T',  # T = I
        'OR F T',   # T = I || F
        'AND E T',  # T = E && (I || F)
        'OR H T',   # T = H || (E && (I || F))
        'AND T J',  # J = (!A || !B || !C) && D && (H || (E && (I || F)))
        'RUN',
    ]
    p2 = run_springdroid(puzzle_input, script)
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
