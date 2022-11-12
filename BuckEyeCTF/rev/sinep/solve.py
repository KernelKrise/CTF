#just reverse encoding algorithm in elf main function
#script:

def to_hex_arr(hstr):
    enc_bytes = list()
    c = 0
    while c < len(hstr):
        enc_bytes.append(int(hstr[c:c+2], 16))
        c += 2
    return enc_bytes


def solve():
    enc = "111c0d0e150a0c151743053607502f1e10311544465c5f551e0e"
    base = "70656e6973"
    flag = ""

    enc_bytes = to_hex_arr(enc)
    base_bytes = to_hex_arr(base)[::-1]

    for i in range(len(enc_bytes)):
        flag += chr(base_bytes[i % 5] ^ enc_bytes[i])

    print(flag)


if __name__ == "__main__":
    solve()
