import binascii

with open('./in.c', 'r') as f:
    original = f.read()
# write system('cat flag.txt') to in.c and add comment // DUMMY
i = 0
while True:
    new_code = original.replace('DUMMY', str(i))
    if hex(binascii.crc32(new_code.encode('utf8'))) == '0x38df65f2':
        break
    if i % 100000 == 0:
        print(i, end=' ')
    i += 1

with open('./get_flag.c', 'w') as f:
    f.write(new_code)
print('SUCCESS!!!')
