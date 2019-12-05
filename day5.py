#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 2 module."""


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


def run_intcode(program, input_val=1):
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
                program[a] = input_val
            elif opcode == 4:
                params = get_params(program, [a], param_modes)
                output = params[0]
                print(output)
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
    p1 = run_intcode(list(puzzle_input))
    p2 = run_intcode(list(puzzle_input), input_val=5)
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
