# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# contributed by Antoine Pitrou
# modified by Dominique Wahli and Daniel Nanz

from __future__ import print_function

import sys
import multiprocessing as mp


def make_tree(i, d):
 
    if d > 0:
        i2 = i + i
        d -= 1
        return (i, make_tree(i2 - 1, d), make_tree(i2, d))
    return (i, None, None)


def check_tree(node):

    (i, l, r) = node
    if l is None:
        return i
    else:
        return i + check_tree(l) - check_tree(r)


def make_check(itde, make=make_tree, check=check_tree):

    i, d = itde
    return check(make(i, d))


def get_argchunks(i, d, chunksize=5000):
    
    assert chunksize % 2 == 0
    chunk = []
    for k in range(1, i + 1):
        chunk.extend([(k, d), (-k, d)])
        if len(chunk) == chunksize:
            yield chunk
            chunk = []
    if len(chunk) > 0:
        yield chunk


def main(n, min_depth=4):

    max_depth = max(min_depth + 2, n)
    stretch_depth = max_depth + 1
    if mp.cpu_count() > 1:
        pool = mp.Pool()
        chunkmap = pool.map
    else:
        chunkmap = map
    
    print('stretch tree of depth {0}\t check: {1}'.format( 
          stretch_depth, make_check((0, stretch_depth))))

    long_lived_tree = make_tree(0, max_depth)
    
    mmd = max_depth + min_depth
    for d in range(min_depth, stretch_depth, 2):
        i = 2 ** (mmd - d)
        cs = 0
        for argchunk in get_argchunks(i,d):
            cs += sum(chunkmap(make_check, argchunk))
        print('{0}\t trees of depth {1}\t check: {2}'.format(i * 2, d, cs))
    
    print('long lived tree of depth {0}\t check: {1}'.format( 
          max_depth, check_tree(long_lived_tree)))


if __name__ == '__main__':
    main(int(sys.argv[1]))