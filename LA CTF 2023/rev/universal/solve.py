# Firstly just decompile .class file with recaf or bytecode viewer or smthng else
# In this file, our input compares as: (var3[34] ^ var3[23] * 7 ^ ~var3[36] + 13) & 255) == 182 && ((var3[37] ^ ...
# So, we need to brute force it
# But firstly replace first bytes with "lactf{" and "}" at the end
# Use:
# for i in raw_flag.split('&&'):
#     if i.count('var') == 1:
#         print(i)

# to find compare with only one unknown byte and brute it, and repeat this operation until you get the flag

from pprint import pprint

raw_flag = "((var3[34] ^ var3[23] * 7 ^ ~var3[36] + 13) & 255) == 182 && ((var3[37] ^ var3[10] * 7 ^ ~var3[21] + 13) & 255) == 223 && ((var3[24] ^ var3[23] * 7 ^ ~var3[19] + 13) & 255) == 205 && ((var3[25] ^ var3[13] * 7 ^ ~var3[23] + 13) & 255) == 144 && ((var3[6] ^ var3[27] * 7 ^ ~var3[25] + 13) & 255) == 138 && ((var3[4] ^ var3[32] * 7 ^ ~var3[22] + 13) & 255) == 227 && ((var3[25] ^ var3[19] * 7 ^ ~var3[1] + 13) & 255) == 107 && ((var3[22] ^ var3[7] * 7 ^ ~var3[29] + 13) & 255) == 85 && ((var3[15] ^ var3[10] * 7 ^ ~var3[20] + 13) & 255) == 188 && ((var3[29] ^ var3[16] * 7 ^ ~var3[12] + 13) & 255) == 88 && ((var3[35] ^ var3[4] * 7 ^ ~var3[33] + 13) & 255) == 84 && ((var3[36] ^ var3[2] * 7 ^ ~var3[4] + 13) & 255) == 103 && ((var3[26] ^ var3[3] * 7 ^ ~var3[1] + 13) & 255) == 216 && ((var3[12] ^ var3[6] * 7 ^ ~var3[18] + 13) & 255) == 165 && ((var3[12] ^ var3[28] * 7 ^ ~var3[36] + 13) & 255) == 151 && ((var3[20] ^ var3[0] * 7 ^ ~var3[21] + 13) & 255) == 101 && ((var3[27] ^ var3[36] * 7 ^ ~var3[14] + 13) & 255) == 248 && ((var3[35] ^ var3[2] * 7 ^ ~var3[19] + 13) & 255) == 44 && ((var3[13] ^ var3[11] * 7 ^ ~var3[33] + 13) & 255) == 242 && ((var3[33] ^ var3[11] * 7 ^ ~var3[3] + 13) & 255) == 235 && ((var3[31] ^ var3[37] * 7 ^ ~var3[29] + 13) & 255) == 248 && ((var3[1] ^ var3[33] * 7 ^ ~var3[31] + 13) & 255) == 33 && ((var3[34] ^ var3[22] * 7 ^ ~var3[35] + 13) & 255) == 84 && ((var3[36] ^ var3[16] * 7 ^ ~var3[4] + 13) & 255) == 75 && ((var3[8] ^ var3[3] * 7 ^ ~var3[10] + 13) & 255) == 214 && ((var3[20] ^ var3[5] * 7 ^ ~var3[12] + 13) & 255) == 193 && ((var3[28] ^ var3[34] * 7 ^ ~var3[16] + 13) & 255) == 210 && ((var3[3] ^ var3[35] * 7 ^ ~var3[9] + 13) & 255) == 205 && ((var3[27] ^ var3[22] * 7 ^ ~var3[2] + 13) & 255) == 46 && ((var3[27] ^ var3[18] * 7 ^ ~var3[9] + 13) & 255) == 54 && ((var3[3] ^ var3[29] * 7 ^ ~var3[22] + 13) & 255) == 32 && ((var3[24] ^ var3[4] * 7 ^ ~var3[13] + 13) & 255) == 99 && ((var3[22] ^ var3[16] * 7 ^ ~var3[13] + 13) & 255) == 108 && ((var3[12] ^ var3[8] * 7 ^ ~var3[30] + 13) & 255) == 117 && ((var3[25] ^ var3[27] * 7 ^ ~var3[35] + 13) & 255) == 146 && ((var3[16] ^ var3[10] * 7 ^ ~var3[14] + 13) & 255) == 250 && ((var3[21] ^ var3[25] * 7 ^ ~var3[12] + 13) & 255) == 195 && ((var3[26] ^ var3[10] * 7 ^ ~var3[30] + 13) & 255) == 203 && ((var3[20] ^ var3[2] * 7 ^ ~var3[1] + 13) & 255) == 47 && ((var3[34] ^ var3[12] * 7 ^ ~var3[27] + 13) & 255) == 121 && ((var3[19] ^ var3[34] * 7 ^ ~var3[20] + 13) & 255) == 246 && ((var3[25] ^ var3[22] * 7 ^ ~var3[14] + 13) & 255) == 61 && ((var3[19] ^ var3[28] * 7 ^ ~var3[37] + 13) & 255) == 189 && ((var3[24] ^ var3[9] * 7 ^ ~var3[17] + 13) & 255) == 185)"

flag_len = 38
flag = list([ord(i) for i in "lactf{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}"])

# replacing lactf{}
raw_flag = raw_flag.replace('var3[0]', '108').replace('var3[1]', '97').replace('var3[2]', '99').replace('var3[3]', '116').replace('var3[4]', '102').replace('var3[5]', '123').replace('var3[37]', '125')

# var3[36]
idx = 36
for i in range(256):
    if ((i ^ 99 * 7 ^ ~102 + 13) & 255) == 103:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 26
for i in range(256):
    if ((i ^ 116 * 7 ^ ~97 + 13) & 255) == 216:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 16
for i in range(256):
    if ((116 ^ i * 7 ^ ~102 + 13) & 255) == 75:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 20
for i in range(256):
    if ((i ^ 99 * 7 ^ ~97 + 13) & 255) == 47:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 21
for i in range(256):
    if ((49 ^ 108 * 7 ^ ~i + 13) & 255) == 101:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 10
for i in range(256):
    if ((125 ^ i * 7 ^ ~108 + 13) & 255) == 223:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 15
for i in range(256):
    if ((i ^ 110 * 7 ^ ~49 + 13) & 255) == 188:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 8
for i in range(256):
    if ((i ^ 116 * 7 ^ ~110 + 13) & 255) == 214:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 12
for i in range(256):
    if ((49 ^ 123 * 7 ^ ~i + 13) & 255) == 193:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 29
for i in range(256):
    if ((i ^ 95 * 7 ^ ~95 + 13) & 255) == 88:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 28
for i in range(256):
    if ((95 ^ i * 7 ^ ~116 + 13) & 255) == 151:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 31
for i in range(256):
    if ((i ^ 125 * 7 ^ ~108 + 13) & 255) == 248:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 33
for i in range(256):
    if ((97 ^ i * 7 ^ ~51 + 13) & 255) == 33:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 35
for i in range(256):
    if ((i ^ 102 * 7 ^ ~95 + 13) & 255) == 84:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 19
for i in range(256):
    if ((51 ^ 99 * 7 ^ ~i + 13) & 255) == 44:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 25
for i in range(256):
    if ((i ^ 98 * 7 ^ ~97 + 13) & 255) == 107:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 11
for i in range(256):
    if ((95 ^ i * 7 ^ ~116 + 13) & 255) == 235:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 13
for i in range(256):
    if ((i ^ 116 * 7 ^ ~95 + 13) & 255) == 242:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 23
for i in range(256):
    if ((110 ^ 115 * 7 ^ ~i + 13) & 255) == 144:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 34
for i in range(256):
    if ((i ^ 49 * 7 ^ ~116 + 13) & 255) == 182:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 24
for i in range(256):
    if ((i ^ 49 * 7 ^ ~98 + 13) & 255) == 205:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 22
for i in range(256):
    if ((121 ^ i * 7 ^ ~51 + 13) & 255) == 84:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 32
for i in range(256):
    if ((102 ^ i * 7 ^ ~108 + 13) & 255) == 227:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 7
for i in range(256):
    if ((108 ^ i * 7 ^ ~108 + 13) & 255) == 85:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 9
for i in range(256):
    if ((116 ^ 51 * 7 ^ ~i + 13) & 255) == 205:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 27
for i in range(256):
    if ((i ^ 108 * 7 ^ ~99 + 13) & 255) == 46:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 6
for i in range(256):
    if ((i ^ 115 * 7 ^ ~110 + 13) & 255) == 138:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 18
for i in range(256):
    if ((95 ^ 49 * 7 ^ ~i + 13) & 255) == 165:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 14
for i in range(256):
    if ((115 ^ 116 * 7 ^ ~i + 13) & 255) == 248:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 30
for i in range(256):
    if ((95 ^ 100 * 7 ^ ~i + 13) & 255) == 117:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

idx = 17
for i in range(256):
    if ((48 ^ 48 * 7 ^ ~i + 13) & 255) == 185:
        print(f'var3[{idx}] = {i}')
        flag[idx] = i
        raw_flag = raw_flag.replace(f'var3[{idx}]', f'{i}')
        break

print("".join([chr(i) for i in flag]))
#find the strings with one unknown char
for i in raw_flag.split('&&'):
    if i.count('var') == 1:
        print(i)
