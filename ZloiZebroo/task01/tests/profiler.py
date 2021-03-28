import cProfile
from task01 import maze as graph
import pstats, math
import io




def main():
    pr = cProfile.Profile()
    pr.run('graph.main()')

    result = io.StringIO()
    pstats.Stats(pr, stream=result).print_stats()
    result = result.getvalue()
    # chop the string into a csv-like buffer
    result = 'ncalls' + result.split('ncalls')[-1]
    result = '\n'.join([';'.join(line.rstrip().split(None, 5)) for line in result.split('\n')])
    # save it to disk

    with open('test.csv', 'w+') as f:
        f.write(result)
        f.close()

    # cProfile.run('graph.main()')
    return 0


if __name__ == '__main__':
    main()
