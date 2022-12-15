Payload in loader is encoded (it located in exe file)
So, we cant decompile or disassemble it

We need to debug it:

I find "call rdi" in main(FUN_001017ab).
I follow it and find comparing len of our input and <b>0x20</b>, so flag is 32 bytes long.

Next i find a loop that xor our input with <b>0x69</b>

Next i found that our xored input compares (cmp) with <b>b'\024XXX\031\034\004\033]\036\066\033Y\017\066Z\004\002\n]\033\n6\020\\]Z\022/=*\"'</b>

So this is xored flag:
<pre>
for i in fl:
    ...:     print(chr(i ^ 0x69), end='')
    ...: 
    ...: 
</pre>
OUTPUT: 
}111pumr4w_r0f_3mkc4rc_y543{FTCK

flag is reversed:
<pre>
In [12]: flag = "}111pumr4w_r0f_3mkc4rc_y543{FTCK"

In [13]: flag[::-1]
Out[13]: 'KCTF{345y_cr4ckm3_f0r_w4rmup111}'
</pre>
