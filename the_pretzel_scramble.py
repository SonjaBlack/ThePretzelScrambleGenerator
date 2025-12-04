# Quick and dirty scramble generator for the sliding bead puzzle
# "The Pretzel" from &11 Game Company.

# Copyright Sonja Black, 2025, and released under the Creative Commons
# Zero 1.0 Universal license
# https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt

from sys import stdout
from random import *

scramble_len = 1 # how many turn/slide pairs are in the scramble

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
    amount = randint(1,4)
    if posneg > 0.5:
        return f"+{amount}"
    else:
        return f"-{amount}"

# given a scramble sequence, simulate it to generate a bead configuration
def getScrambleImage(sequence):
    # Initialize arrays. We have four arrays for the bottom parts of the circle
    # (two 6s and two 3s) and one large array of length 27 for the movable track.
    # The swapping portions of the track are defined simply as indexes within it.
    # 'w' and 'b' represent white and blue beads.
    ll6 = ['w' for i in range(0,6)]
    ll3 = ['w' for i in range(0,3)]
    lr6 = ['w' for i in range(0,6)]
    lr3 = ['w' for i in range(0,3)]
    track = ['b' for i in range(0,27)]
    lbuffer = [] # long and short buffers to assist with the swaps.
    sbuffer = []
    # since clockwise slides are positive numbers, we'll count beads in that direction
    # too, with the 0th bead being the first one to the left of the split line between
    # the upper and lower sections of the puzzle, adjacent to the larger section. Thus
    # bead #26 is the one immediately adjacent and to the right of bead #0.
    index1 = 21 # the large section is beads 21..26, so the end index has to be 27
    index2 = 27
    index3 = 9  # the small section is beads 9..11
    index4 = 12

    def turn(dir): # helper
        def swapRight(): # helper's helper
            nonlocal ll6, ll3, lr6, lr3, track, lbuffer, sbuffer
            # Swapping right means:
            # 1, copy the large and small sections from the track into the buffers
            lbuffer = track[index1:index2]
            sbuffer = track[index3:index4]
            # 2, copy ll6 and ll3 into the track
            for i in range(0,6):
                track[index1+i] = ll6[i]
            for i in range(0,3):
                track[index3+i] = ll3[i]
            # 3, copy lr6 and lr3 int ll6 and ll3
            ll6 = [lr6[i] for i in range(0,6)]
            ll3 = [lr3[i] for i in range(0,3)]
            # 4, copy the buffers into lr6 and lr3 
            lr6 = [lbuffer[i] for i in range(0,6)]
            lr3 = [sbuffer[i] for i in range(0,3)]            
        # Assume we were supposed to swap right:
        swapRight()
        # And if that was wrong, just swapRight again. Two wrongs make a left!
        if dir == 'L':
            swapRight()

    def slide(amt): # helper
        amount = int(amt)
        nonlocal track
        if amount > 0: # positive, clockwise slide. Beads from the end go to the beginning
            track = track[-amount:] + track[:27-amount]
        else:          # negative, counterclockwise. Beads from the beginning go to the end
            track = track[-amount:] + track[:-amount] 

    def showBeads():
        nonlocal ll6, ll3, lr6, lr3, track, lbuffer, sbuffer
        print(''.join(track[:9]) + "|" + ''.join(track[9:12]) + "|" + ''.join(track[12:21]) + "|" + ''.join(track[21:]))
        print(''.join(ll3) + "|" + ''.join(ll6) + "     " + ''.join(lr6) + "|" + ''.join(lr3))

    # Iterate through the scramble. Recall, scramble_len is how many chunks there are,
    # so sequence[] is actually twice that long
    for i in range(0,scramble_len):
        turn(sequence[2*i])
        slide(sequence[2*i+1])
    showBeads()

if __name__ == "__main__":
    sequence = []

    for i in range(scramble_len):
        sequence.append(getTurn())
        sequence.append(getSlide())

    for s in range(len(sequence)):
        stdout.write(str(sequence[s]) + " ")
        if s % 8 == 7:
            stdout.write("\n")
    print()
    getScrambleImage(sequence)
