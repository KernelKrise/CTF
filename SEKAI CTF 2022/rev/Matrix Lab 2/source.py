# uncompyle6 version 3.5.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: Matrix_Lab.py
print('Welcome to Matrix Lab 2! Hope you enjoy the journey.')
print('Lab initializing...')
try:
    import matlab.engine
    engine = matlab.engine.start_matlab()
    flag = input('Enter the lab passcode: ').strip()
    outcome = False
    if len(flag) == 23:
        if flag[:6] == 'SEKAI{':
            pass
    if flag[-1:] == '}':
        A = [ord(i) ^ 42 for i in flag[6:-1]]
        B = matlab.double([A[i:i + 4] for i in range(0, len(A), 4)])
        X = [list(map(int, i)) for i in engine.magic(4)]
        Y = [list(map(int, i)) for i in engine.pascal(4)]
        C = [[None for _ in range(len(X))] for _ in range(len(X))]
        for i in range(len(X)):
            for j in range(len(X[i])):
                C[i][j] = X[i][j] + Y[i][j]

        C = matlab.double(C)
        if engine.mtimes(C, engine.rot90(engine.transpose(B), 1337)) == matlab.double([[2094, 2962, 1014, 2102], [2172, 3955, 1174, 3266], [3186, 4188, 1462, 3936], [3583, 5995, 1859, 5150]]):
            outcome = True
        if outcome:
            print('Access Granted! Your input is the flag.')
        else:
            print('Access Denied! Your flag: SADGE{aHR0cHM6Ly95b3V0dS5iZS9kUXc0dzlXZ1hjUQ==}')
except:
    print('Unknown error. Maybe you are running the lab in an unsupported environment...')
    print('Your flag: SADGE{ovg.yl/2M6pWQB}')
