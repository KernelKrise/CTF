# six (popular meme)
# 13371337 (just disasm and see strcmp())
# it's a log cabin!!! (following script)

enc = [ 0x0e, 0xc9, 0x9d, 0xb8, 0x26, 0x83, 0x26, 0x41, 0x74, 0xe9, 0x26, 0xa5, 0x83, 0x94, 0x0e, 0x63, 0x37, 0x37, 0x37, 0x00 ]
ans = ""
for i in enc:
    for j in range(256):
        if (j * 0x11) % 0xfd == i:
            ans += chr(j)
            break
print(ans)
