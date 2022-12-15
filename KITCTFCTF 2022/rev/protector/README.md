protector (rev): KCTF{fl4g_h1d35_1n_pl41n_51gh7_1f_y0u_g37_r1d_0f_7h3_g4rb4g3}

So, i read decompiled and disassembled code in ghidra and understand that this executable decode itself while running. So we need to debug this peace of sh... elf file

While debugging i found this:
<pre>
   0x0000000000401000:	mov    r12d,0x600000
   0x0000000000401006:	movabs r13,0x7b34b4c5a505890
   0x0000000000401010:	xor    QWORD PTR [r12],r13
   0x0000000000401014:	add    r12,0x8
   0x0000000000401018:	xor    QWORD PTR [r12],r13
   0x000000000040101c:	add    r12,0x8
   0x0000000000401020:	xor    QWORD PTR [r12],r13
   0x0000000000401024:	add    r12,0x8
   0x0000000000401028:	xor    QWORD PTR [r12],r13
   0x000000000040102c:	sub    r12,0x18
   0x0000000000401030:	jmp    r12
</pre>
From this we can understand that code are encoded in elf body, end to decode it we need to xor it with r13
After self decoding program do jmp $r12 (jump to decoded chunk of code)

Then program changing $r13 register by some XORs with previous decoded values 

   0x0000000000401033:	mov    r14,r13
   0x0000000000401036:	xor    r14,QWORD PTR [r12]
   0x000000000040103a:	add    r12,0x8
   0x000000000040103e:	xor    r14,QWORD PTR [r12]
   0x0000000000401042:	add    r12,0x8
   0x0000000000401046:	xor    r14,QWORD PTR [r12]
   0x000000000040104a:	add    r12,0x8
   0x000000000040104e:	xor    r14,QWORD PTR [r12]
   0x0000000000401052:	sub    r12,0x18
   0x0000000000401056:	xor    QWORD PTR [r12],r13
   0x000000000040105a:	add    r12,0x8
   0x000000000040105e:	xor    QWORD PTR [r12],r13
   0x0000000000401062:	add    r12,0x8
   0x0000000000401066:	xor    QWORD PTR [r12],r13
   0x000000000040106a:	add    r12,0x8
   0x000000000040106e:	xor    QWORD PTR [r12],r13
   0x0000000000401072:	add    r12,0x8
   0x0000000000401076:	mov    r13,r14
   0x0000000000401079:	jmp    0x401010

And loop repeats in order to decode next code chunk...

So, after hours of experiment i wrote this code:

```
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
```
Usage:
```
$ python3 parse.py > asm.lst
```

It's going to take a long time

After the script is finished we get asm.lst file. So, lets examine it. 
There are a lot of dead weight code, you have to be patient

At address 0x25d160 and beyond i found:
```
0x25d160
   0:   80 3f 5a                cmp    BYTE PTR [rdi], 0x5a
   3:   9f                      lahf   
   4:   90                      nop
   5:   90                      nop
   6:   90                      nop
   7:   90                      nop

   0:   80 3f b0                cmp    BYTE PTR [rdi], 0xb0
   3:   9f                      lahf   
   4:   90                      nop
   5:   90                      nop
   6:   90                      nop
   7:   90                      nop

...
```
So, we have 61 cmp instruction. It's not hard to figure out that it is a encoded flag
But we need to know how it was encoded

I search all instructions with "rdi" register and find that:
```
   0:   80 37 ec                xor    BYTE PTR [rdi], 0xec
   0:   80 07 03                add    BYTE PTR [rdi], 0x3
   0:   80 2f 6c                sub    BYTE PTR [rdi], 0x6c
   0:   48 ff c7                inc    rdi
   0:   80 37 ac                xor    BYTE PTR [rdi], 0xac
   0:   80 07 b2                add    BYTE PTR [rdi], 0xb2
   0:   80 2f 2b                sub    BYTE PTR [rdi], 0x2b
   0:   48 ff c7                inc    rdi
   0:   80 37 16                xor    BYTE PTR [rdi], 0x16
   0:   80 07 bb                add    BYTE PTR [rdi], 0xbb
   0:   80 2f 7f                sub    BYTE PTR [rdi], 0x7f
   0:   48 ff c7                inc    rdi
   0:   80 37 54                xor    BYTE PTR [rdi], 0x54
   0:   80 07 b9                add    BYTE PTR [rdi], 0xb9
   0:   80 2f 16                sub    BYTE PTR [rdi], 0x16

  ...
```
After many hours with the debugger i understand that bytes are encoded with (xor, add, sub), but not only one time. Each byte encoded 4 times after every 256 blocks of (xor, add, sub)

So, i write all bytes in cmp instruction to file "cmp":
```
x5a
0xb0
0x75
0x9d
0x23
0x39
0x7a
0xcb
...
```

Also all (xor, add, sub) blocks values in bytes.lst:
```
0xec
0x3
0x6c
0xac
0xb2
0x2b
0x16
...
```

And wrote this script with reversed encode function:
```
with open('cmp', 'r') as f:
    enc = f.read().split('\n')

with open('bytes.lst', 'r') as f:
    text = f.read().split('\n')

result = list() # split to (xor, add, sub) blocks
i = 0
while i < len(text):
    result.append(text[i:i+3])
    i += 3

flag = "" # decode loop
for i, w in enumerate(enc):
    tmp = result[1024 + i]
    res = (int(w, 16) + int(tmp[2], 16) - int(tmp[1], 16)) ^ int(tmp[0], 16)
    tmp = result[768 + i]
    res = (res + int(tmp[2], 16) - int(tmp[1], 16)) ^ int(tmp[0], 16)
    tmp = result[512 + i]
    res = (res + int(tmp[2], 16) - int(tmp[1], 16)) ^ int(tmp[0], 16)
    tmp = result[256 + i]
    res = (res + int(tmp[2], 16) - int(tmp[1], 16)) ^ int(tmp[0], 16)
    tmp = result[i]
    res = (res + int(tmp[2], 16) - int(tmp[1], 16)) ^ int(tmp[0], 16)
    res = res % 256 # VERY IMPORTANT % (to normalize negative values of bytes)
    flag += chr(res)
print(flag)
```

And:
```
ubuntu@ubuntu:~/Desktop/protector$ python3 flag.py
KCTF{fl4g_h1d35_1n_pl41n_51gh7_1f_y0u_g37_r1d_0f_7h3_g4rb4g3}
```
