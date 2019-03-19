from re import match
from functools import reduce
import operator


def tokenize(filename):
    return (lex(s) for s in open(filename).read().replace('(', ' ( ').replace(')',' ) ').split())


def lex(s: str) -> (str, str):
    if   s in ('(', ')', 'let', 'fn'):
        return s
    elif match(r'".*"', s):   return ("string", s[1:-1])
    elif match(r'[0-9]+', s): return ("number", int(s))
    return ("name", s)


def parse(tokens) -> list:
    tree = []
    t = next(tokens)
    while t:
        if t == ')': return tree
        if t == '(': tree.append(parse(tokens))
        else:        tree.append(t)
        try:    t = next(tokens)
        except: return tree


def fn(args, body, scope):
    args = [x[1] for x in args]
    return lambda xs: eval(body,
                           {**scope, **dict(zip(args,xs))})

def eval(lisp, scope):

    if isinstance(lisp, tuple):
        return lisp[1] if lisp[0] != 'name' else scope[lisp[1]]

    if lisp[0] == 'let':
        return scope.update({lisp[1][1]:eval(lisp[2], scope)})

    if lisp[0] == 'fn':
        return fn(lisp[1], lisp[2], scope)


    f = scope[lisp[0][1]]
    args = [eval(x, scope) for x in lisp[1:]]
    return f(args)


def main():
    scope = {
        'print': lambda xs: print(''.join(str(x) for x in xs)),
        '+':     lambda xs: reduce(operator.add, xs),
        '-':     lambda xs: reduce(operator.sub, xs)
    }
    tokens = tokenize("hello.lisp")
    for x in parse(tokens):
        eval(x, scope)

if __name__ == "__main__":
    main()


