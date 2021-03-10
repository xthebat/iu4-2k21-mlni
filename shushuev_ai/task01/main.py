import numpy as np
import os
import sys

def path_func(path1, path2):
    path = os.path.join(path1, path2)
    return (path, len(path))

def main(args):
    x = 10
    y = 1.0
    output = f'x={x}, y={y}, sum={x + y}'
    print(output)

    path = os.path.join('home', 'art')

    print(path)

    #Медленно, поэтому не надо
    result = ''
    for it in args:
        result += it

    print(f'result={result}')

    #Как надо
    effective_result = "".join(args)

    print(f'efferctive_result={effective_result}')

    p, l = path_func('/home','arg')
    print(f'path={p}, length={l}')

if __name__ == '__main__':
    main(sys.argv)
