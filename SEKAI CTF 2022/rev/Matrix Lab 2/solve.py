import numpy as np


def solve():
    encrypted_flag = np.array([[2094, 2962, 1014, 2102],
                               [2172, 3955, 1174, 3266], 
                               [3186, 4188, 1462, 3936], 
                               [3583, 5995, 1859, 5150]])

    x = [[16, 2, 3, 13],
         [5, 11, 10, 8],
         [9, 7, 6, 12],
         [4, 14, 15, 1]]

    y = [[1, 1, 1, 1],
         [1, 2, 3, 4],
         [1, 3, 6, 10],
         [1, 4, 10, 20]]

    c = [[None for _ in range(len(x))] for _ in range(len(x))]
    for i in range(len(x)):
        for j in range(len(x[i])):
            c[i][j] = x[i][j] + y[i][j]

    inverse_c = np.linalg.inv(c)
    multiplied = np.array([list(map(lambda h: round(h), i)) for i in np.matmul(inverse_c, encrypted_flag)])
    rotated = np.rot90(multiplied, 3)
    transposed = np.transpose(rotated)

    a = []
    for i in transposed:
        a += list(i)

    flag = "".join([chr(i ^ 42) for i in a])
    return "SEKAI{" + flag + "}"


print(solve())
