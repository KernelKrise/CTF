with open('cap.c', 'r') as f:
    code = f.read()

code = code.replace('lit ', 'int ')
code = code.replace('legit ', 'void ')
code = code.replace('finna', '{')
code = code.replace('tho', '}')
code = code.replace('ongod', '(')
code = code.replace('af', ')')
code = code.replace('tryna', 'if')
code = code.replace('be', '==')
code = code.replace('cap', '0')
code = code.replace('lookin', '=')
code = code.replace('fr fr', 'fr')
code = code.replace(' fr', ';')
code = code.replace('lowkey', '<')
code = code.replace('playin', '++')
code = code.replace('deadass', 'return')
code = code.replace('sheeeesh ', 'printf')
code = code.replace(' bruh', ',')
code = code.replace('dub', '+')
code = code.replace('no', '!')
code = code.replace('downbad', '--')
code = code.replace('clean', 'char')
code = code.replace('yeet', '[')
code = code.replace(' rn', ']')
code = code.replace('poppin ', 'for')
code = code.replace('mf ', '* ')
code = code.replace('boutta ', 'while')
code = code.replace('chill', 'continue')
code = code.replace('bussin', '1')
code = code.replace('highkey', '>')
code = code.replace('respectfully', 'do')
code = code.replace('lackin', '-')
code = code.replace('wack', '/')
code = code.replace('like', '||')
code = code.replace('#define', '//')
code = code.replace('sus ', '? ')
code = code.replace('drip ', ': ')
code = code.replace('', '')

with open('decoded.c', 'w') as f:
    f.write(code)
