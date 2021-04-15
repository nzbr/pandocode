#!/usr/bin/python3

from sys import exit

#$begin
def algorithm(a, b):
    if a == b:
        return a
    elif b > a:
        return b
    else:
        return a + b

def main():
    x = algorithm(5, 7)
    #$-
    print(x)
    #$= x = x + 1
    x += 1
    if x <= 0:
        # Some things are still broken with raw \LaTeX lines, see return statement below
        #$= :: \State\textsf{x must be $>$ 0 $\lightning$}
        raise Exception("x must be greater than 0")

    return x
#$end

print(main())

