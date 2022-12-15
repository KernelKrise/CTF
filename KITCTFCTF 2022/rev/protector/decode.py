from pwn import *


context.arch = "amd64"
starti = 0x972f850179a6d9d8  # to find offset (this is instruction on address 0x600000 in ELF)
r13 = 0x7b34b4c5a505890
with open('protector', 'rb') as f:
    data = f.read()

offset = data.find(p64(starti)) # find instruction "starti" address

for j in range(100000):
    print(f"ADDR: {hex(offset)}")
    
    lst = list()
    for i in range(4):
        lst.append(u64(data[offset + i * 8: offset + i * 8 + 8])) # XOR decode

    for i in range(4):
        lst[i] = lst[i] ^ r13 

    print(disasm(p64(lst[0]))) # useful instructions only in first chunk of code

    r14 = r13
    for i in range(4):
        r14 = r14 ^ lst[i]
        
    r13 = r14
    offset += 0x20
