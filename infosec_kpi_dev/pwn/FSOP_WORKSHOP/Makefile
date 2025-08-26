# Compile in ubuntu:16.04

TARGET := fsop
CC := gcc
CFLAGS := -O0 -fstack-protector-strong -fPIE -pie -Wl,-z,relro,-z,now -Wl,-z,noexecstack -Wl,-rpath,./glibc -Wl,--dynamic-linker=./glibc/ld.so.2 -g -I/usr/include

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	$(RM) $(TARGET)
