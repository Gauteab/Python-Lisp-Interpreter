# Lisp Interpreter in Python

This an implementation of a simple Lisp in less than 100 lines of python.

The goal was to see how simple you can make i lisp interpreter (if you allow cutting a few corners, like error checking and having a performant lexer). The language has very few special forms. Core functionality like cons lists are implemented in the language itself, instead of in the interpreter.

Run: `python lisp.py <program>.lisp`
