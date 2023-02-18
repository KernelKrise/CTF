def func(f, i):
    if i<5:
        out = ord(f) ^ 0x76 ^ 0xAD
        var1 = (out & 0xAA) >> 1
        var2 = 2 * out & 0xAA
        return var1 | var2 
    elif i>=5 and i<10:
        out = ord(f) ^ 0x76 ^ 0xBE
        var1 = (out & 0xCC) >> 2
        var2 = 4 * out & 0xCC
        return var1 | var2
    else:
        out = ord(f) ^ 0x76 ^ 0xEF
        var1 = (out & 0xF0) >> 4
        var2 = 16 * out & 0xF0
        return var1 | var2


with open('./result', 'r') as f:
    enc = f.read()

flag = ""
for n in range(15):
    for i in range(255):
        sym = func(chr(i), n)
        if chr(sym) == enc[n]:
            flag += chr(i)

print(f'ictf{{{flag}}}')
