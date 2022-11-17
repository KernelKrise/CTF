xor_lst = [0x57, 0x65, 0x6c, 0x63, 0x6f, 0x6d, 0x65, 0x20, 
0x74, 0x6f, 0x20, 0x53, 0x45, 0x43, 0x43, 0x4f, 0x4e, 0x20, 
0x32, 0x30, 0x32, 0x32, 0x57, 0x65, 0x6c, 0x63, 0x6f, 0x6d, 
0x65, 0x20, 0x74, 0x6f, 0x20, 0x53, 0x45, 0x43]  # with this bytes, our input xored at the start of the function (i found it using gdb gef insude loop in $rax register)

concated = ""  # values that return CONCAT44 function (concated local variables in func)
concated += '591e2320202f2004'[::-1]  # use little-endian format
concated += '2b2d3675357f1a44'[::-1]
concated += '0736506d035a1711'[::-1]
concated += '362b470401093c15'[::-1]
concated += '380a41'[::-1]

lst = list()

i = 0
while i < 36 * 2 - 2:
    lst.append(int("0x" + concated[i:i+2][::-1], 16))
    i += 2

for j in range(len(xor_lst) - 1):
    print(chr(xor_lst[j] ^ lst[j]), end='')
    
