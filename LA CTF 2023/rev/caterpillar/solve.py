# -~ in js equals 1. So we simply need to parse the code

flag = list("lactf{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}")

with open("caterpillar.js", "r") as f:
    text = f.read().replace('([])', '(0)').replace('[]', '').split('\n')[1]

new_code = ""
check = False
counter = 0

for i in text:
    if i in ('-', '~'):
        check = True
    if check and i == '-':
        counter += 1
    if check and i not in ('-', '~'):
        check = False
        new_code += str(counter)
        counter = 0
    if not check:
        new_code += i 

new_code = new_code[4:-3].split('&&')

for i in new_code:
    flag[int(i[i.find('(') + 1: i.find(')')])] = chr(int(i[i.find('== ') + 3:]))

print("".join(flag))
