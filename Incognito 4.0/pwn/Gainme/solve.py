from pwn import *

p = remote('143.198.219.171', 5003)
#p = process('./Gainme')
#gdb.attach(p, gdbscript='b *main+178')
print(p.recv())
p.sendline(b'ICTF4')
print(p.recv())
p.sendline(p32(0x44736164) + p32(0x57515341) + p32(0x72746a67) + p32(0x73646f6b) + p32(99))
print(p.recv())
p.sendline(p32(0xdeadbeef))
print(p.recv())
p.sendline(p32(0x31))
print(p.recv())
