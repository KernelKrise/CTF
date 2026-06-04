# baby-bof

There is `lighthttpd` server which on each request executes `CGI` binary `index.cgi`.
Target program is `CGI` binary which checks HTTP `Authorization` buffer.

There is stack-based buffer overflow vulnerability in `decode_base64()` function. 
It takes input buffer `basic_auth` with base64-encoded data and decodes it into `decoded` buffer.
The problem is `decode_base64` does not check size of output buffer. So, large input buffer (as HTTP `Authorization` header) will be written to small
`decoded` buffer causing overwflow.
```c
char decoded[0x100];
...
decode_base64(basic_auth, decoded);
```

But, `index.cgi` compiled with `canary` enabled, so we can not just overwrite return address.

But, there are some `try/catch` constructions we can abuse to do so.

The main idea of such method of exploitation described here: [https://github.com/chop-project/chop](https://github.com/chop-project/chop)

As I understand, when function fails on `throw`, exception handling algorithm starts:
1. Check if current return address in `try` block
2. If no -> check return address of caller function and so on
3. If yes -> check what `catch` block catches
4. If `catch` block catches needed exception - execute it
5. If no -> check return address of caller function and so on

The idea is to `hijack` return address of current function, so it will point
to another `try` block with `suitable` exception filter in other function `WITHOUT` `canary`.
> Yes, some function does not have `canary`. Compiler will not add it if there is no work with buffers in function.

So, how we can find pointer to suitables `try/catch`? 
Unfortunately, start and end of it are not present in disassembled code. This information located in specific sections:
`.eh_frame`, `.gcc_except_table` and very unfriendly to understand.

But, there is tool named [edhdump](https://github.com/chop-project/chop/tree/main/tools/ehdump) which can do it for us.

We will use it to dump `try` block's `start` and `end` addresses and `lp` - start of the `catch` block. 
Filter by `ar_disp==0`, so catch block will catch all exceptions without type matching.

Use the following command:

```shell
ehdump ./index.cgi | head -n -1 | jq '.[].lsda.cses[] | select(any(.actions[]?; .ar_disp==0)) | {start,end,lp}'
```

Output:

```json
{
  "start": "0x4025a7",
  "end": "0x4025ac",
  "lp": "0x402632"
}
{
  "start": "0x4036c7",
  "end": "0x4036cc",
  "lp": "0x403758"
}
{
  "start": "0x4037a1",
  "end": "0x4037a6",
  "lp": "0x4037a6"
}
{
  "start": "0x4037c8",
  "end": "0x4037ca",
  "lp": "0x4037cf"
}
{
  "start": "0x4012b4",
  "end": "0x4012b9",
  "lp": "0x40124d"
}
{
  "start": "0x404b96",
  "end": "0x404b9b",
  "lp": "0x404bd3"
}
{
  "start": "0x407d0b",
  "end": "0x407d10",
  "lp": "0x407d7c"
}
{
  "start": "0x40a415",
  "end": "0x40a4c5",
  "lp": "0x40a4ef"
}
```

So, we obtained candidates for `CHOP` exploitation.

Yes, we can statically analyze them to check if there is canary in each function and if there are no code that can crash, but
I am lazy, so i just tried all of them.

And I found out that this two `try/catch` block:
```json
{
  "start": "0x407d0b",
  "end": "0x407d10",
  "lp": "0x407d7c"
}
{
  "start": "0x40a415",
  "end": "0x40a4c5",
  "lp": "0x40a4ef"
}
```
gives us `RIP` control because of return address corruption.

So, now we just need to do ROP to read the flag.

Tricky part is that we are behind HTTP server, so probably no `/bin/sh` shell for us. So, we need to read the flag.

There are all gdagets we need to control `RAX`, `RDI`, `RSI`, `RDX` and do `SYSCALL`.
Also, I found gadget `mov qword ptr [rdi], rax ; ret` which gives us `arbitrary write` primitive.

`ROP` chain will be:
1. Arbwrite `/flag.txt` to writable memory.
2. Open `/flag.txt` using `SYS_open` syscall.
3. Read flag data with `SYS_read` syscall.
4. Write flag data to `stdout` using `SYS_write` syscall.

`solve.py` output:
```
$ ./solve.py REMOTE
[*] '/home/user/ctf/dist-baby_bof/index.cgi'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
[*] Loaded 127 cached gadgets for 'index.cgi'
[*] FLAG: grey{5tuck_<REDACTED>_3b6ab6b4}
```
