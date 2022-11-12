from copy import deepcopy


def arr_equal(arr1, arr2):
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True


def metamorphosis(flag_byte, n):
    return flag_byte >> (8 - n % 8 & 0x1f) | flag_byte << n % 8


def encode(arr, val):
    inp = deepcopy(arr)
    length = len(inp)
    for i in range(length):
        tmp = metamorphosis(inp[i], val)
        inp[i] = tmp
        val = inp[i]
    for i in range(length):
        inp[i] = int("0x" + hex(inp[i])[-2:], 16)
    return inp


def main():
    lst = [
        0x89, 0xea, 0x8d, 0x6d, 0xac, 0x97, 0xb2, 0xed,
        0x6e, 0x1d, 0x24, 0xc6, 0x1b, 0xfa, 0x89, 0x66, 0x1d,
        0x8e, 0xcc, 0x27, 0xaf, 0x3a, 0xa1, 0x68, 0x6e, 0xd7,
        0xb9, 0xe8, 0x72, 0x99, 0xe4, 0x97, 0xbe, 0x00
          ]

    flag = list()
    for i in lst:
        for j in range(20, 140):
            flag.append(j)
            res = encode(flag, 0x2a)
            if arr_equal(res, lst[:len(res)]) is False:
                flag.pop()
            else:
                break

    for i in flag:
        print(chr(i), end='')


if __name__ == "__main__":
    main()
