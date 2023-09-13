when program get our review, we need to pass ascii chars (48 bytes):

We cant find two dword numbers to sum to get 0xb98c5f37 and be full ascii chars, but we can split this number to:

0x3c2c3937 + 0x7d602600

We cant write 00 byte in the input, program will not read it

But the program adds 00 byte at the and. So the idea is pass 0x3c2c3937 and 0x7d602641 and then pass new input to overwrite 0x41 byte with byte terminator 0x00 to get 0x7d602600
