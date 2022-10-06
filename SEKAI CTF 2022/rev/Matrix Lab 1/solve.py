def transform(inp):
    carray2 = [
           [1, 2, 3, 4, 5, 6],
           [1, 2, 3, 4, 5, 6],
           [1, 2, 3, 4, 5, 6],
           [1, 2, 3, 4, 5, 6],
           [1, 2, 3, 4, 5, 6],
           [1, 2, 3, 4, 5, 6]
              ]
    i = 0
    while i < 36:
        carray2[i // 6][i % 6] = inp[i]
        i += 1
    return carray2


def solve(cArray):
    i = 0
    while i <= 3:
        j = 0
        while j < 6 - 2 * i - 1:
            c = cArray[i][i + j]
            cArray[i][i + j] = cArray[6 - 1 - i - j][i]
            cArray[6 - 1 - i - j][i] = cArray[6 - 1 - i][6 - 1 - i - j]
            cArray[6 - 1 - i][6 - 1 - i - j] = cArray[i + j][6 - 1 - i]
            cArray[i + j][6 - 1 - i] = c
            j += 1
        i += 1
    return cArray


def get_array(cArray, n, n2):
    n3 = 0
    n4 = 0
    carray2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    while n3 < 6:
        carray2[n4] = cArray[n][n3]
        n4 += 1
        n3 += 1

    n3 = 0
    while n3 < 6:
        carray2[n4] = cArray[n2][6 - 1 - n3]
        n4 += 1
        n3 += 1

    return carray2


def encrypt(cArray, n):
    n2 = 0
    n3 = 5
    n4 = 6
    carray2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    while n2 < 12:
        carray2[n2] = cArray[n3]
        n3 -= 1
        carray2[n2 + 1] = cArray[n4]
        n4 += 1
        n2 += 2
    n2 = 0

    while n2 < 12:
        n5 = n2
        n2 += 1
        carray2[n5] = chr(ord(carray2[n5]) ^ n)

    return "".join(carray2)


def transform_rev(array):
    res = ''
    for i in array:
        res += "".join(i)
    return res


def solve_rev(cArray):
    for i in range(0, 4):
        j = 0
        while j < 6 - 2 * i - 1:
            c = cArray[i + j][6 - 1 - i]
            cArray[i + j][6 - 1 - i] = cArray[6 - 1 - i][6 - 1 - i - j]
            cArray[6 - 1 - i][6 - 1 - i - j] = cArray[6 - 1 - i - j][i]
            cArray[6 - 1 - i - j][i] = cArray[i][i + j]
            cArray[i][i + j] = c
            j += 1
    return cArray


def get_array_rev(array):
    return [array[0:6], list(reversed(array[6:12]))]


def decrypt(encrypted, n):
    n2 = 0
    n3 = -1
    n4 = 12
    carray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    carray2 = list()

    for i in encrypted:
        carray2.append(chr(ord(i) ^ n))

    while n2 < 12:
        n4 -= 1
        carray[n4] = carray2[n2 + 1]
        n3 += 1
        carray[n3] = carray2[n2]
        n2 += 2

    return list(reversed(carray[0:6])) + list(reversed(carray[6:12]))


def challenge_solve():
    encrypted_flag = 'oz]{R]3l]]B#50es6O4tL23Etr3c10_F4TD2'

    part1 = encrypted_flag[0:12]
    part2 = encrypted_flag[12:24]
    part3 = encrypted_flag[24:36]

    dec1 = decrypt(part1, 2)  # 0, 5
    dec2 = decrypt(part2, 1)  # 1, 4
    dec3 = decrypt(part3, 0)  # 2, 3

    rev1 = get_array_rev(dec1)
    rev2 = get_array_rev(dec2)
    rev3 = get_array_rev(dec3)

    arr = [rev1[0], rev2[0], rev3[0], rev3[1], rev2[1], rev1[1]]

    fl = transform_rev(arr)
    return "SEKAI{" + fl + "}"


if __name__ == "__main__":
    print(challenge_solve())
