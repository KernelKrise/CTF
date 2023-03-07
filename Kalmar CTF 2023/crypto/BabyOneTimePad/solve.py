from pwn import *


def xor_chrs(str1, db):
    resp_xored = list()
    for idx, i in enumerate(str1):
        if idx % 2 == 0:
            resp_xored.append(i ^ ord(db[0]))
        else:
            resp_xored.append(i ^ ord(db[1]))
    return bytearray(resp_xored)

permutation = '0,' * 64
for i in range(128):
    permutation += f'{i},'
payload = permutation[:-1].encode()

print(f'Permutation PAYLOAD: ')
print(payload)

passwd_enc = bytes.fromhex(input('ENTER ENC PASSWD: '))
resp = bytes.fromhex(input('ENTER PERMUTATION RESPONSE: '))

for i in range(0x10, 256):
    tmp_key = xor_chrs(resp[:128], hex(i)[2:])
    r = str(xor(resp[128:], tmp_key))[2:-1]
    for j in r:
        if j not in "0123456789abcdef":
            break
    else:
        print(f'VALUE: {hex(i)} -> {r}')
        print(f'KEY: {tmp_key.hex()}')
        print(f'PASSWORD: {str(xor(passwd_enc, tmp_key))[2:-1]}')
        
