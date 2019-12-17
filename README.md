# aoc2019
My Advent of Code 2019 solutions

Should work in Python 3.6+, but only tested in 3.7.

General usage should follow:
```
$ python3 day1.py input.txt
```

You can also enter input via stdin, use EOF marker (Ctrl+D) when finished sending input.
When using stdin, your input format should match the AOC txt file input format.
```
$ python3 day1.py -
1
2
3
<Ctrl+D>
```

### Requirements

- numpy
- [tqdm](https://github.com/tqdm/tqdm) - if tqdm is available, certain slow solutions will provide a progress bar on the terminal.

### Notes

- Day 17: pathing split was found by hand and probably only works for my input

To install everything:
```
$ pip install -r requirements.txt
```
