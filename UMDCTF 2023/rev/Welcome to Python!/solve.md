
┌──(kali㉿kali)-[~/Desktop/pyinstxtractor]
└─$ python3 pyinstxtractor.py chal                                                                                 
[+] Processing chal
[+] Pyinstaller version: 2.1+
[+] Python version: 3.10
[+] Length of package: 6544209 bytes
[+] Found 35 files in CArchive
[+] Beginning extraction...please standby
[+] Possible entry point: pyiboot01_bootstrap.pyc
[+] Possible entry point: pyi_rth_inspect.pyc
[+] Possible entry point: chal.pyc
[!] Warning: This script is running in a different Python version than the one used to build the executable.
[!] Please run this script in Python 3.10 to prevent extraction errors during unmarshalling
[!] Skipping pyz extraction
[+] Successfully extracted pyinstaller archive: chal

You can now use a python decompiler on the pyc files within the extracted directory




pyc to py:

git clone https://github.com/zrax/pycdc
cd pycdc
cmake .
make
make check



FLAG LEN: 38

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


print('==========================================')
print('Professional flag checker service (v 97.2)')
print('==========================================')
flag = input('Show me the flag: ')
lf = len(flag)
ls = len(source)
l = lf if lf < ls else ls
for i in range(seed, seed + l):
    w = wandom(i)
    c = (ord(flag[i - seed]) ^ evil_bit_hack(wandom(wandom(w))) & evil_bit_hack(w)) + 1
    if source[i - seed] != c:
        print("Uh oh! We don't think your flag is correct... :(")
        exit_(1)
if lf == ls:
    print('Your flag is correct!')
    exit(1)
None('Some of your flag is correct...')
