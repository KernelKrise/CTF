We have admin function with buffer overflow, but we neeed to pass not zero param to it
In buy book function we have store with books, we want to buy "address of puts()", but we need money:
After buying or not buying a book, we can leave a tip ($10), so we can get negative amount of money!
```
======================================
|Cash balance: $5|
1) The Catcher in the ROP - $300
2) The Great Hacksby - $425
3) The Address of puts() - $99999999
======================================
What do you want to read? >> 2
You don't have enough cash!

Thanks for you're buisness, would you like to leave a tip? (y/N) >> y

Yay! Thank you!

1) Write a book
2) Buy a book
3) Write a special book (ADMINS ONLY) (0)
4) Check out
 >> 2
Want to buy an adventure on paperback?
Here's what we have in stock
======================================
|Cash balance: $4294967291|
1) The Catcher in the ROP - $300
2) The Great Hacksby - $425
3) The Address of puts() - $99999999
======================================
What do you want to read? >> 3
In the realm of bits and bytes, the audacious CTF player searched and searched, seeking something useful for their intellectual shenanigans. At long last, they had finally found it. For in the distance, in all it's glory 0x7f366d42eb00 rested in slumber, it's image telling a story. The End.
```

Write book function is also vulnerable, we can overflow the value in stack to bypass admin check cyclic(40):
So, we need to exploit overflow in buyBook function to get puts address, exploit "write a book" function to bypass admin check, exploit buffer overflow in admin function to ret2libc. Simple system('/bin/sh') dont work, need to use rop chain to syscall
