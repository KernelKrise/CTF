# We have a program without functions, variables, etc...
# Idk how to reverse this algorithm, but i can brute force flag byte by byte
# To do this, I rewrote the algorithm on python. I substitute the values of the flag bytes for each iteration

from pwn import *

with open('switcheroo', 'rb') as f:
    DATA = f.read()
BASE_ADDR = 0x40203c - 0x400000


def ltob(number, i=0):
    return (number & (0xff << (i * 8))) >> (i * 8)


def rol (val, r_bits, max_bits):
    return (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))


def find_byte(r10):
    val = 0x21
    while val < 0x7e:
        addr = BASE_ADDR + val*8
        r8 = u64(DATA[addr:addr+8])
        r8 = rol(r8, 0x8, 64)
        r13 = ltob(r8)
        r14 = 0
        while True:
            if r14 >= r13:
                break
            r8 = rol(r8, 0x8, 64)
            if ltob(r8) == ltob(r10):
                return chr(val)
            else:
                r14 += 1
        val += 1

    print('ERROR!')
    return 'X'

flag = ""
for w in range(0x3f):
    flag += find_byte(w)

print(flag)
