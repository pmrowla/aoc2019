#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2019 day 8 module."""

from collections import Counter


def get_layers(pixels, size=(3, 2)):
    width, height = size
    pixels_s = str(pixels)
    if len(pixels_s) % (width * height) != 0:
        raise ValueError('pixel data does not match image size')
    layers = []
    i = 0
    stride = width * height
    while i < len(pixels_s):
        layers.append(pixels_s[i : i+stride])
        i += stride
    return layers


def composite(layers):
    layers.reverse()
    im = [pixel for pixel in layers.pop(0)]
    for layer in layers:
        for i, pixel in enumerate(layer):
            if pixel != '2':
                im[i] = pixel
    for i, pixel in enumerate(im):
        if pixel == '0':
            im[i] = ' '
    return ''.join(im)


def process(puzzle_input, verbose=False):
    p1 = p2 = None
    width, height = (25, 6)
    layers = get_layers(puzzle_input, (width, height))
    counts = [Counter(layer) for layer in layers]
    p1_layer = sorted(counts, key=lambda x: x['0'])[0]
    p1 = p1_layer['1'] * p1_layer['2']
    p2_im = composite(layers)
    p2 = []
    for i in range(height):
        p2.append(p2_im[i*width : (i+1)*width])
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
        for line in fileinput.input(args.infile):
            puzzle_input = line.strip()
            if not puzzle_input:
                continue
            p1, p2 = process(puzzle_input, verbose=args.verbose)
            print(f'Part one: {p1}')
            print(f'Part two:')
            [print(l) for l in p2]
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
