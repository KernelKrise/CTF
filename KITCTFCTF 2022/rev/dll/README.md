Payload in loader is encoded (it located in exe file)
Si, we cant decompile or disassemble it
We need to debug it:
I find "call rdi" in main(FUN_001017ab)
I follow it and find comparing len of our input and 0x20, so flag is 0x20 bytes long
Next i find a loop that xor our input with 0x69
Next i found that our xored input cmp with b'\024XXX\031\034\004\033]\036\066\033Y\017\066Z\004\002\n]\033\n6\020\\]Z\022/=*\"'
So this is xored flag:
for i in fl:
    ...:     print(chr(i ^ 0x69), end='')
    ...: 
    ...: 
}111pumr4w_r0f_3mkc4rc_y543{FTCK

flag is reversed:
In [12]: flag = "}111pumr4w_r0f_3mkc4rc_y543{FTCK"

In [13]: flag[::-1]
Out[13]: 'KCTF{345y_cr4ckm3_f0r_w4rmup111}'
