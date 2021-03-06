#!/usr/bin/python3

from string import (ascii_lowercase, ascii_uppercase, ascii_letters,
                    digits, punctuation)
from sys import argv
from secrets import choice
import subprocess

alias = {
    'l' : ascii_lowercase,
    'u' : ascii_uppercase,
    'd' : digits,
    's' : '!@#$%',
    'p' : punctuation,
    'a' : ascii_letters
}

def usage(progname="passgen.py"):
    print(f'{progname} [-c] [length] [alphabet]')
    print()
    print(f'''Alphabet is specificed as follows:

    l: {alias["l"]}
    u: {alias["u"]}
    d: {alias["d"]}
    s: {alias["s"]}
    p: {alias["p"]}
    a: {alias["a"]}
    c: <custom alphabet>

    Use `-c' to copy password to clipboard instead of stdout.

Examples,

    # 10 character long password picked from {{a,b,c,d}}
    $ {progname} 10 cabcd
    abbacbaaba

    # 5 charactor long password picked from "a" and "p" alphabets above.
    $ {progname} 5 pa
    ?(Pqv
''')

args = argv[1:]
progname = argv[0].split('/')[-1]

if len(args) < 2:
    usage(progname)
    exit(0)

copy_to_clipboard = args[0] == '-c'
args = args[(1 if copy_to_clipboard else 0):]

try:
    ln = int(args[0])
    if ln == 0:
        raise ValueError
except ValueError:
    print(f'"{args[0]}" is not a valid length')

spec = args[1]
alph = set()
if spec[0] == 'c':
    # cannot use `set` here as we want to be able to introduce biases
    alph = spec[1:]
else:
    for c in spec:
        try:
            alph.update(alias[c])
        except KeyError:
            print(f'ignoring unknown alphabet spec: {c}')
    alph = ''.join(c for c in alph)

if not len(alph):
    print(f'empty alphabet for spec={spec}')

pwd = ''.join(choice(alph) for _ in range(ln))
if copy_to_clipboard:
    p1 = subprocess.Popen(['echo', '-n', pwd], stdout=subprocess.PIPE)
    subprocess.Popen(['xclip', '-selection', 'c'], stdin=p1.stdout)
else:
    print(pwd)
