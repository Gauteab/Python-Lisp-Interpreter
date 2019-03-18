from re import match
from functools import reduce
import operator


def tokenize(filename):
    return (lex(s) for s in open(filename).read().split())


def lex(s):
    if   s in ('(', ')', 'let'): return s
    elif match(r'".*"', s):      return ("string", s[1:-1])
    elif match(r'[0-9]+', s):    return ("number", int(s))
    return ("name", s)


def parse(tokens) -> list:
    tree = []
    t = next(tokens)
    while t:
        if t == ')': return tree
        if t == '(':
            tree.append(parse(tokens))
        else:
            tree.append(t)
        try:    t = next(tokens)
        except: return tree


def eval(lisp, scope):

    if isinstance(lisp, tuple):
        return lisp[1] if lisp[0] != 'name' else scope[lisp[1]]

    if lisp[0] == 'let':
        scope.update({lisp[1][1]:lisp[2][1]})
        return None

    f = scope[lisp[0][1]]
    args = [eval(x, scope) for x in lisp[1:]]
    return f(args)


def main():
    scope = {
        'print': lambda xs: print(''.join(str(x) for x in xs)),
        '+':     lambda xs: reduce(operator.add, xs)
    }
    tokens = tokenize("hello.lisp")
    for x in parse(tokens):
        eval(x, scope)

if __name__ == "__main__":
    main()


