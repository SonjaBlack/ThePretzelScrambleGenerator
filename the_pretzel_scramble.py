# Quick and dirty scramble generator for AndOneOriginal's bead puzzle.

# Copyright Sonja Black, 2025, and released under the Creative Commons
# Zero 1.0 Universal license
# https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt

from sys import stdout
from random import *

scramble_len = 20 # how many turn/slide pairs are in the scramble

# there are only two meaningful turns, clockwise and counterclockwise,
# Which we'll call R and L # since cw and ccw start with the same letter.
def getTurn():
    if random() > 0.5:
        return "R"
    else:
        return "L"

# Slides are cycles of the moving bead track by some number of beads
# clockwise and counterclockwise. # We'll use positive and negative
# integers in the range +/- 9, excluding zero. Clockwise is positive,
# relative to the bottom of the track.
def getSlide():
    posneg = random()
    amount = randint(1,9)
    if posneg > 0.5:
        return f"+{amount}"
    else:
        return f"-{amount}"

if __name__ == "__main__":
    sequence = []

    for i in range(scramble_len):
        sequence.append(getTurn())
        sequence.append(getSlide())

    for s in range(len(sequence)):
        stdout.write(sequence[s] + " ")
        if s % 8 == 7:
            stdout.write("\n")
