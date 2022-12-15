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
