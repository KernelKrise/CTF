from pwn import *

p = remote('prog.dvc.tf', 7753)

for _ in range(51):
    try:
        resp = p.recvuntil('Chord').decode()
    except:
        resp = p.recv().decode()
    piano = resp[resp.find('________________'):resp.find('Chord')-2]

    if piano == '':
        print(resp) # flag
        break

    print(piano)
    ans = list()

    default = """_________________________________________________________________________________________________________________________________________________________________________________________________________________________________
|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
|  |c| |d|  |  |f| |g| |a|  |  |c| |d|  |  |f| |g| |a|  |  |c| |d|  |  |f| |g| |a|  |  |c| |d|  |  |f| |g| |a|  |  |c| |d|  |  |f| |g| |a|  |  |c| |d|  |  |f| |g| |a|  |  |c| |d|  |  |f| |g| |a|  |  |c| |d|  |  |f| |g| |a|  |
|  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| C | D | E | F | G | A | B | C | D | E | F | G | A | B | C | D | E | F | G | A | B | C | D | E | F | G | A | B | C | D | E | F | G | A | B | C | D | E | F | G | A | B | C | D | E | F | G | A | B | C | D | E | F | G | A | B |
|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|"""
    
    keyboard_length = piano.find('\n')
    default = default.split('\n')
    for i in range(len(default)):
        default[i] = default[i][:keyboard_length]
    default = '\n'.join(default)
    print(default)

    chords = {
        b"C"  : {'C', 'E', 'G'},
        b"C#" : {'c', 'F', 'g'},
        b"D"  : {'D', 'f', 'A'},
        b"D#" : {'d', 'G', 'a'},
        b"E"  : {'E', 'g', 'B'},
        b"F"  : {'F', 'A', 'C'},
        b"F#" : {'f', 'a', 'c'},
        b"G"  : {'G', 'B', 'D'},
        b"G#" : {'g', 'C', 'd'},
        b"A"  : {'A', 'c', 'E'},
        b"A#" : {'a', 'D', 'F'},
        b"B"  : {'B', 'd', 'f'},

        b"Cm" : {'C', 'd', 'G'},
        b"C#m": {'c', 'E', 'g'},
        b"Dm" : {'D', 'F', 'A'},
        b"D#m": {'d', 'f', 'a'},
        b"Em" : {'E', 'G', 'B'},
        b"Fm" : {'F', 'g', 'C'},
        b"F#m": {'f', 'A', 'c'},
        b"Gm" : {'G', 'a', 'D'},
        b"G#m": {'g', 'B', 'd'},
        b"Am" : {'A', 'C', 'E'},
        b"A#m": {'a', 'c', 'F'},
        b"Bm" : {'B', 'D', 'f'},

        b"C-" : {'C', 'd', 'f'},
        b"C#-": {'c', 'E', 'G'},
        b"D-" : {'D', 'F', 'g'},
        b"D#-": {'d', 'f', 'A'},
        b"E-" : {'E', 'G', 'a'},
        b"F-" : {'F', 'g', 'B'},
        b"F#-": {'f', 'A', 'C'},
        b"G-" : {'G', 'a', 'c'},
        b"G#-": {'g', 'B', 'D'},
        b"A-" : {'A', 'C', 'd'},
        b"A#-": {'a', 'c', 'E'},
        b"B-" : {'B', 'D', 'F'},

        b"C+" : {'C', 'E', 'g'},
        b"C#+": {'c', 'e', 'A'},
        b"D+" : {'D', 'f', 'a'},
        b"D#+": {'d', 'G', 'B'},
        b"E+" : {'E', 'g', 'C'},
        b"F+" : {'F', 'A', 'c'},
        b"F#+": {'f', 'a', 'D'},
        b"G+" : {'G', 'B', 'd'},
        b"G#+": {'g', 'C', 'E'},
        b"A+" : {'A', 'c', 'F'},
        b"A#+": {'a', 'D', 'f'},
        b"B+" : {'B', 'd', 'G'}
    }

    notes = set()
    for i in range(0, len(piano)):
        if piano[i] == 'X':
            notes.add(default[i])
    print(f'FIND NOTES: {notes}')

    for chord in chords:
        if chords[chord] == notes:
            ans.append(chord.decode())
            print(f'FIND CHORD: {chord.decode()}')
    print(ans)
    p.sendline(str(ans).encode())
