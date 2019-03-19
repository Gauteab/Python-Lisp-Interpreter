from re import match
from functools import reduce
import operator
import sys

#########
# Lexer #
#########
def tokenize(filename):
    return (lex(s) for s in open(filename).read().replace('(', ' ( ').replace(')',' ) ').split())

def lex(s: str) -> (str, str):
    if   s in ('(', ')', 'let', 'fn', 'if', 'nil', 'begin'): return s
    elif match(r'".*"', s):   return ("string", s[1:-1])
    elif match(r'[0-9]+', s): return ("number", int(s))
    return ("name", s)

##########
# Parser #
##########
def parse(tokens) -> list:
    tree = []
    t = next(tokens)
    while t:
        if t == ')': return tree
        if t == '(': tree.append(parse(tokens))
        else:        tree.append(t)
        try:    t = next(tokens)
        except: return tree

###############
# Interpreter #
###############
def eval(lisp, scope):

    if lisp == 'nil': return 'nil'

    if isinstance(lisp, tuple):
        return lisp[1] if lisp[0] != 'name' else scope[lisp[1]]

    if lisp[0] == 'begin':
        return begin(lisp[1:], scope)

    if lisp[0] == 'let':
        return scope.update({lisp[1][1]:eval(lisp[2], scope)})

    if lisp[0] == 'fn':
        return fn(lisp[1], lisp[2], scope)

    if lisp[0] == 'if':
        return lisp_if(lisp[1], lisp[2], lisp[3], scope)

    return scope[lisp[0][1]]((eval(x, scope) for x in lisp[1:]))


################
# Core Library #
################
def fn(args, body, scope):
    return lambda xs: eval(body, {**scope, **dict(zip([x[1] for x in args], xs))})

def lisp_if(test, hit, miss, scope):
    if (eval(test, scope) != 0): return eval(hit, scope)
    else:                        return eval(miss, scope)

# TODO: Might not need to be a special form
def begin(xs, scope):
    r = None
    for x in xs:
        r = eval(x, scope)
    return r

###########################
# Main                    #
###########################
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

