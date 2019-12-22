#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 22 module."""


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def get_ops(puzzle_input):
    ops = []
    for line in puzzle_input:
        x = line.split()
        op = x[0]
        try:
            count = int(x[-1])
        except ValueError:
            count = None
        ops.append((op, count))
    return ops


def deal(deck_size, n, count):
    if count is None:
        return (-1 * n + deck_size - 1) % deck_size
    return (n * count) % deck_size


def deal_inverse(deck_size, a, b, count):
    if count is None:
        # return (-1 * n + deck_size - 1) % deck_size
        return (-a, -b + deck_size - 1)
    # return (n * modinv(count, deck_size) % deck_size)
    inv = modinv(count, deck_size)
    return a * inv, b * inv


def cut(deck_size, n, count):
    return (n - count) % deck_size


def cut_inverse(deck_size, a, b, count):
    # return (n + count) % deck_size
    return a, b + count


def shuffle(puzzle_input, card, deck_size=10007):
    ops = {'deal': deal, 'cut': cut}
    for i, (op, count) in enumerate(get_ops(puzzle_input)):
        card = ops[op](deck_size, card, count)
    return card


def shuffle_inverse(puzzle_input, index, deck_size=10007, iterations=1):
    ops = {'deal': deal_inverse, 'cut': cut_inverse}
    a = 1
    b = 0
    for op, count in reversed(get_ops(puzzle_input)):
        a, b = ops[op](deck_size, a, b, count)
    a %= deck_size
    b %= deck_size
    return (index * pow(a, iterations, deck_size) +
            (pow(a, iterations, deck_size) - 1) * b * modinv(a - 1, deck_size)) % deck_size


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    p1 = shuffle(puzzle_input, 2019)
    p2 = shuffle_inverse(puzzle_input, 2020, 119315717514047, 101741582076661)
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
        puzzle_input = [line.strip() for line in fileinput.input(args.infile) if line.strip()]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print(f'Part one: {p1}')
        print(f'Part two: {p2}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
