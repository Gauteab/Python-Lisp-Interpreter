from re import match


def tokenize(filename):
    return (lex(s) for s in open(filename).read().split())


def lex(s):
    if   s in ('(', ')'):       return s
    elif match(r'".*"', s):     return ("string", s[1:-1])
    elif match(r'[0-9]+', s):   return ("number", int(s))
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


#def eval(lisp):
    #if isinstance(lisp, list): return eval(lisp)


def main():
    tokens = tokenize("hello.lisp")
    for x in parse(tokens):
        print(x)

if __name__ == "__main__":
    main()
