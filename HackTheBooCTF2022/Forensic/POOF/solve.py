# decrypt .pdf:
import pyaes
from pwn import *

with open('candy_dungeon.pdf.boo', 'rb') as f:
    ciphertext = f.read() + b'\xaa'*15

key = b'vN0nb7ZshjAWiCzv'
iv = b'ffTC776Wt59Qawe1'
aes = pyaes.AESModeOfOperationCFB(key, iv=iv)
result = b''

c = 0
while c < len(ciphertext):
    result += aes.decrypt(ciphertext[c:c+16])
    c += 16

result = result[:-15]
with open('decrypted.pdf', 'wb') as f:
    f.write(result)
