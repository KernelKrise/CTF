# Decompile elf in ghidra, find main and see, that user input compares (cmp al, BYTE PTR [rbx+rsi*1]) with some value that is returned by the custom function on each iteration
# So, we need to use gdb gef to retrieve this value on each iteration

flag_len = 47 # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

main = "0x555555555070"
cmp_break = "0x55555555510b"

flag = \
[
    0x6c,
    0x61,
    0x63,
    0x74,
    0x66,
    0x7b,
    0x6d,
    0x34,
    0x79,
    0x62,
    0x33,
    0x5f,
    0x74,
    0x68,
    0x33,
    0x72,
    0x33,
    0x5f,
    0x31,
    0x73,
    0x5f,
    0x73,
    0x30,
    0x6d,
    0x33,
    0x5f,
    0x6d,
    0x33,
    0x72,
    0x31,
    0x74,
    0x5f,
    0x74,
    0x30,
    0x5f,
    0x75,
    0x73,
    0x31,
    0x6e,
    0x67,
    0x5f,
    0x34,
    0x5f,
    0x64,
    0x62,
    0x7d
]

print("".join([chr(i) for i in flag]))

#gef> define fn
# set $eflags |= (1 << 6)
# c
# end

# use fn to iterate and retrieve value of $al register
