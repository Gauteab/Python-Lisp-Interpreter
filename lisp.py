from re import match
from functools import reduce
import operator
import sys

#######################################################################
#                                Lexer                                #
#######################################################################

KEYWORDS = set(['(', ')', '[', ']', '{', '}', 'let', 'fn', 'nil', 'if'])

def tokenize(filename):
    return (lex(s) for s in open(filename).read().replace('(', ' ( ').replace(')',' ) ').split())

def lex(s: str) -> (str, str):
    if   s in (KEYWORDS): return s
    elif match(r'".*"', s):   return ("string", s[1:-1])
    elif match(r'[0-9]+', s): return ("number", int(s))
    return ("name", s)

#######################################################################
#                               Parser                                #
#######################################################################

def parse(tokens) -> list:
    tree = []
    t = next(tokens)
    while True:
        if t in (')', ']', '}'): return tree
        if t in ('(', '[', '{'): tree.append(parse(tokens))
        else:        tree.append(t)
        try:    t = next(tokens)
        except: return tree

#######################################################################
#                             Interpreter                             #
#######################################################################

def eval(lisp, scope):

    if lisp == 'nil': return 'nil'

    if isinstance(lisp, tuple):
        return lisp[1] if lisp[0] != 'name' else scope[lisp[1]]

    if lisp[0] == 'let':
        return scope.update({lisp[1][1]:eval(lisp[2], scope)})

    if lisp[0] == 'fn':
        return fn(lisp[1], lisp[2:], scope)

    if lisp[0] == 'if':
        return eval(lisp[2] if eval(lisp[1], scope) != 0 else lisp[3], scope)

    return scope[lisp[0][1]]((eval(x, scope) for x in lisp[1:]))

def fn(args, body, scope):
    def begin(body, scope):
        r = None
        for x in body:
            r = eval(x, scope)
        return r

    return lambda xs: begin(body, {**scope, **dict(zip([x[1] for x in args], xs))})

#######################################################################
#                                Main                                 #
#######################################################################

def main(filename):

    scope = {
        'println':  lambda xs: print(''.join(str(x) for x in xs), end=" \n" ),
        'print':    lambda xs: print(''.join(str(x) for x in xs), end=" "),
        '+':        lambda xs: reduce(operator.add, xs),
        '-':        lambda xs: reduce(operator.sub, xs),
        '*':        lambda xs: reduce(operator.mul, xs),
        '/':        lambda xs: reduce(operator.truediv, xs),
        '%':        lambda xs: reduce(operator.mod, xs),
        '=':        lambda xs: reduce(operator.eq, xs),
    }

    tokens = tokenize(filename)
    for x in parse(tokens):
        eval(x, scope)

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)

