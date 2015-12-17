'''
Implementation of Simple LZ factorization algorithm 
as proposed by Crochemore et al in 

Crochemore, Maxime, Lucian Ilie, and William F. Smyth. 
"A simple algorithm for computing the Lempel Ziv factorization." 
Data Compression Conference. IEEE, 2008.

Replace test.txt with the test file name 
Program accepts the number of characters to process
as command line argument.

Author: Solongo Munkhjargal

'''

import sys
import time
import tools_karkkainen_sanders as tks
from tools_karkkainen_sanders import *
from memory_profiler import profile

def compute_LPF(sa, _lcp):
    sa = sa[:len(_lcp)]
    sa.append(-1)
    STACK = [0]
    lpf = [0 for i in range(len(sa)-1)]
    n = len(lpf)
    lcp = [0] + _lcp

    for i in range(1,n):
        while (len(STACK) != 0) and \
            ((sa[i] < sa[STACK[-1]]) or \
            (sa[i] > sa[STACK[-1]] and lcp[i] <= lcp[STACK[-1]])):
            if (sa[i] < sa[STACK[-1]]):
                lpf[sa[STACK[-1]]] = max(lcp[i], lcp[STACK[-1]])
                lcp[i] = min(lcp[i], lcp[STACK[-1]])
            else:
                lpf[sa[STACK[-1]]] = lcp[STACK[-1]]
            STACK = STACK[:-1]
        if i < n:
             STACK.append(i)
    return lpf

def lempel_ziv_factorization(lpf):
    LZ = [0]
    i = 0
    n = len(lpf)
    while LZ[i] < len(lpf):
        LZ.append(LZ[i] + max(1, lpf[LZ[i]]))
        i += 1
    return LZ[:-1]
@profile
def compute_LZ_factors(s):
    s_unicode = unicode(s,'utf-8','replace')
    sa = simple_kark_sort(s_unicode)
    lcp = tks.LCP(s,sa)
    lpf = compute_LPF(sa, lcp)
    return lempel_ziv_factorization(lpf)

if __name__ == '__main__':
    N = int(sys.argv[1])
    with open('test.txt', 'rb') as fin:
        content = fin.read()
    _start = time.time()
    compute_LZ_factors(content[:N])

    print "Elapsed time : ", (time.time() - _start)