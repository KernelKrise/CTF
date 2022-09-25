from json import *
import sys
import hashlib

sys.setrecursionlimit(2000)

f = open('LOCK.txt', 'r')  # $node LOCK_to_json.js > LOCK.txt
lock_list = load(f)
f.close()

val = 0
key = ''
stack = list()
saved_stack = list()
C = [62, 223, 233, 153, 37, 113, 79, 195, 9, 58, 83, 39, 245, 213, 253, 138, 225, 232, 123, 90, 8, 98, 105, 1, 31, 198,
     67, 83, 41, 139, 118, 138, 252, 165, 214, 158, 116, 173, 174, 161, 6, 233, 37, 35, 86, 7, 108, 223, 97, 251, 2,
     245, 129, 118, 227, 120, 26, 70, 40, 26, 183, 90, 172, 155]


def multisearch(arr):
    global val
    c = 0
    for i in arr:
        if type(i) is list:
            stack.append(c)
            multisearch(i)
            stack.pop()
        if i == val:
            stack.append(c)
            global saved_stack
            saved_stack = stack.copy()
            return
        c += 1
    return


def key_gen(arr):
    result = ''
    for i in arr:
        result += '1' * i + '0'
    return result


def sha512(key):
    hashed_key = hashlib.sha512(key.encode('utf-8')).hexdigest()
    res = list()
    for i in range(0, 128, 2):
        res.append(int(hashed_key[i: i + 2], 16))
    return res


def get_flag(hash):
    ret = ''
    for i in range(64):
        ret += chr(C[i] ^ hash[i])
    return ret


for i in range(1, 1338):
    val = i
    multisearch(lock_list)
    key += key_gen(saved_stack)
    stack.clear()
    saved_stack.clear()

hsh = sha512(key)
flag = get_flag(hsh)
print(flag)
