from z3 import *


def shift_right(x, val):
    return x >> val
    
def keygen():
    s = Solver()
    a = [Int(f"a_{i}") for i in range(20)]

    # 1 - 5

    for i in range(5): # numbers from 1 to 9
        s.add(a[i] > 0)
        s.add(a[i] <= 9)

    s.add(a[0] % 2 == 0) # 1st byte is even
    s.add(a[4] % 2 == 1) # 5th byte is odd
    s.add(Sum(a[:5]) > 0x14)
    s.add(Sum(a[:5]) < 0x19)

    s.add((a[0] * 10000 + a[1] * 1000 + a[2] * 100 + a[3] * 10 + a[4]) % 5 == 0)
    s.add((a[0] * 10000 + a[1] * 1000 + a[2] * 100 + a[3] * 10 + a[4]) % 0x19 == 0)
    s.add((a[0] * 10000 + a[1] * 1000 + a[2] * 100 + a[3] * 10 + a[4]) % 0x997 == 0)

    # 5 - 10

    for i in range(5, 10):
        s.add(a[i] >= 51)
        s.add(a[i] <= 56)
        
    s.add(a[5 + 3] == ord('7'))
    s.add(a[5 + 4] == ord('6'))

    s.add(a[5 + 0] + a[5 + 1] - 0x5f == a[5 + 2] - 0x30)

    s.add(a[5 + 2] - 0x30 == (a[5 + 3] - 0x30) * 2 - a[0])

    s.add(((a[5 + 1] - 0x30) * 10 + a[5 + 2] - 0x30) % a[0] == 0)

    # 10 - 15

    answ_10_15 = 0
    for i in range(10000, 99999):
        if i >> 0xb == 0x1c - 4 and i & 0x1f == 0x1d and (i >> 5) & 0x3f == 0x2a:
            answ_10_15 = i

    for i in range(5):
        s.add(a[10+i] == int(str(answ_10_15)[i]))
    
    # 15 - 20

    answ_15_20 = 0
    for i in range(10000, 99999):
        if (i & 0xffffffff) % 2 == 0 and i % 4 == 0 and i % 8 == 0 and i % 0x15cd == 0:
            answ_15_20 = i
            break

    for i in range(5):
        s.add(a[15+i] == int(str(answ_15_20)[i]))

    if s.check() == sat:
        print('Model: ', end='')
        model = s.model()
        for i in a:
            if int(str(model[i])) > 9:
                print(chr(int(str(model[i]))), end='')
            else:
                print(model[i], end='')
    else:
        raise Exception("Not satisfiable")


keygen()
#  {FLG:1v4n0_1m_57uhl_und_d13_57umm3_f4hn3}
