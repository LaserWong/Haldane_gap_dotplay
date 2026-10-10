#!/usr/bin/env python3
"""Exact cyclotomic checks of magnetic/antiunitary symmetry and word coverage."""
import json, subprocess, time
from collections import defaultdict
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def mul(x,y):
    a,b=x;c,d=y;return a*c-b*d,a*d+b*c-b*d
def conj(x):a,b=x;return a-b,-b
def phase(twist,p):
    if twist=='I':return 1,0
    if twist=='P':return (-1 if p%2 else 1),0
    return [(1,0),(0,1),(-1,-1)][p%3]
def right(w):return (w[-1],)+w[:-1]
def reflect(w):return tuple(reversed(w))
def flip(w):return tuple(-x for x in w)
def encode(w):
    c=0
    for x in w:c=3*c+x+1
    return c
def matrix_column(w,twist):
    n=len(w);col={w:(16-3*n//2-sum(w[k-1]*w[k] for k in range(n)),0)}
    for k in range(n):
        l=(k+1)%n
        for delta in (-1,1):
            v=list(w);v[k]-=delta;v[l]+=delta
            if min(v)<-1 or max(v)>1:continue
            p=w[0]-v[0] if l==0 else 0
            a,b=phase(twist,p);v=tuple(v)
            old=col.get(v,(0,0));col[v]=(old[0]-a,old[1]-b)
    return col
def word_orbit(w):
    result=set()
    for original in (w,flip(w),reflect(w),flip(reflect(w))):
        for t in range(len(w)):result.add(original[t:]+original[:t])
    return result
def check(n,twist):
    start=time.monotonic();words=list(product((-1,0,1),repeat=n));matrix={w:matrix_column(w,twist) for w in words}
    edges=0
    for w,column in matrix.items():
        tau=phase(twist,-w[-1])
        for v,a in column.items():
            # M T = T M, T|w>=z^(-w[-1])|right(w)>.
            assert mul(tau,matrix[right(w)][right(v)])==mul(phase(twist,-v[-1]),a)
            # M B K = B K M and M V K = V K M.
            assert matrix[reflect(w)][reflect(v)]==conj(a)
            assert matrix[flip(w)][flip(v)]==conj(a)
            edges+=1
    expected={}
    for w in words:
        orb=word_orbit(w)
        # The executable deliberately chooses a nonpositive-M representative.
        eligible=[v for v in orb if sum(v)<=0]
        representative=min(eligible)
        expected[encode(representative)]=len(orb)
    actual={}
    for m in range(-n,1):
        out=subprocess.check_output([str(ROOT/'stream_horner'),str(n),twist,'full',str(m),'0','0',str(ROOT/'coefficients_A.txt'),'list'],text=True)
        for line in out.splitlines()[1:]:
            c,mult=map(int,line.split());assert c not in actual;actual[c]=mult
    assert actual==expected
    assert sum(actual.values())==3**n
    return {'L':n,'twist':twist,'matrix_entries_checked':edges,'orbits':len(actual),'dimension':3**n,'seconds':time.monotonic()-start,'exact_checks_passed':True}
if __name__=='__main__':
    results=[]
    for n in (4,6):
        for twist in ('I','P','C'):
            result=check(n,twist);results.append(result);print(json.dumps(result),flush=True)
    (ROOT/'symmetry_validation.json').write_text(json.dumps({'tests':results},indent=2)+'\n')
