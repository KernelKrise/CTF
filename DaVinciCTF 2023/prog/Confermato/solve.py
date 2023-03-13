from pwn import *

p = remote('prog.dvc.tf', 7752)

for _ in range(51):
    resp = p.recv().decode()
    piano = resp[resp.find('________________'):resp.find('Chord')-2]

    if piano == '':
        print(resp) # flag
        break

    print(piano)
    ans = b''

    default = """_________________________________________________________
|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
|  |c| |d|  |  |f| |g| |a|  |  |c| |d|  |  |f| |g| |a|  |
|  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| C | D | E | F | G | A | B | C | D | E | F | G | A | B |
|___|___|___|___|___|___|___|___|___|___|___|___|___|___|"""

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
        b"Bm" : {'B', 'D', 'f'} 
    }

    notes = set()
    for i in range(150, len(resp) - 57):
        if piano[i] == 'X':
            notes.add(default[i])
    print(f'FIND NOTES: {notes}')
    for chord in chords:
        if chords[chord] == notes:
            ans = chord
            print(f'FIND CHORD: {chord.decode()}')
            break
    p.sendline(chord)
