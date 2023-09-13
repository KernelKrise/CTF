We can call only whitelisted syscalls

From whitelist syscalls we have openat(), read(), so we can read the flag. But we need to output it somehow. I decided to make error-based brute force:

If we gues the byte of the flag correctly, we will call read() syscall and program will not crash, else crash:

On 10th byte of flag we need to change shellcode:
```
        payload += asm('add r12, 8')
        payload += asm('add r12, 2')
```
Because asm('add r12, 10') will give us '\n' bye and shellcode will not be read to the end
