from math import sqrt, sin, cos
from ctypes import c_uint32, c_float
from sys import exit as exit_

source = [ 672662614,
    741343303,
    495239261,
    744259788,
    722021046,
    0xA70AA247,
    1053692,
    0xA8050035,
    0xA982A820,
    624689,
    0xA90D20BC,
    41134,
    295340,
    0xA0028102,
    622681,
    576469,
    671170814,
    0x8041086E,
    765,
    680595550,
    0x80200166,
    698368102,
    2437137,
    0x8042C1EE,
    570966112,
    4612341,
    0x800008D4,
    0xA94D02CE,
    16484,
    2103301,
    136226,
    9438506,
    663820758,
    0x8013523B,
    8405532,
    0xA4000875,
    0x80030A78,
    136768]
seed = 64

def wandom(x):
    return x * x * cos(x) * sin(x) / 1000


def evil_bit_hack(y):
    return int(c_uint32.from_buffer(c_float(y)).value)

def main():
    for i in range(seed, seed + 38):
        for j in range(20, 200):
            w = wandom(i)
            c = (j ^ evil_bit_hack(wandom(wandom(w))) & evil_bit_hack(w)) + 1
            if source[i - seed] != c:
                continue
            else:
                print(chr(j), end='')

main()
