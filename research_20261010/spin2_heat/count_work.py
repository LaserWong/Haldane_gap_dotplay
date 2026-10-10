#!/usr/bin/env python3
"""Exact dimensions/orbits/edge counts by Burnside and generating polynomials."""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def conv(p,q):
    r=[0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
      for j,b in enumerate(q):r[i+j]+=a*b
    return r

def cycles(p):
    seen=set();cy=[]
    for i in range(len(p)):
      if i in seen:continue
      s=0;j=i
      while j not in seen:seen.add(j);s+=1;j=p[j]
      cy.append(s)
    return cy

def counts(n):
    pp=[1]
    for _ in range(n):pp=conv(pp,[1]*5)
    pp2=[1]
    for _ in range(n-2):pp2=conv(pp2,[1]*5)
    allowed=conv([1]*4,[0]+[1]*4);moves=conv(pp2,allowed)
    fixed=[0]*len(pp);flip=0
    for rev in [False,True]:
      for t in range(n):
        cy=cycles([(t-k if rev else t+k)%n for k in range(n)]);pol=[1]
        for length in cy:
            f=[0]*(4*length+1)
            for r in range(5):f[r*length]=1
            pol=conv(pol,f)
        for i,x in enumerate(pol):fixed[i]+=x
        flip+=5**sum(s%2==0 for s in cy)
    rows=[]
    for m in range(2*n+1):
        dim=pp[2*n-m]
        if m==0:num=fixed[2*n]+flip;den=4*n
        else:num=fixed[2*n-m];den=2*n
        assert num%den==0
        reps=num//den;nnz=dim+2*n*moves[2*n-m] if 2*n-m<len(moves) else dim
        rows.append({'M':-m,'dimension':dim,'representatives':reps,'stored_edges':nnz,'weight_sum':dim*(1 if m==0 else 2),'column_edge_products':reps*nnz,'column_dimension_products':reps*dim})
    assert sum(r['weight_sum'] for r in rows)==5**n
    return {'L':n,'hilbert_dimension':5**n,'rows':rows,'total_representatives':sum(r['representatives'] for r in rows),'total_column_edges':sum(r['column_edge_products'] for r in rows),'total_column_dimensions':sum(r['column_dimension_products'] for r in rows),'low_M_0_to_4_column_edges':sum(r['column_edge_products'] for r in rows[:5])}
if __name__=='__main__':
    out={str(n):counts(n) for n in [3,4,8,9,10]}
    for n in [9,10]:
        r=out[str(n)];print(n,r['total_representatives'],r['total_column_edges'],r['rows'][0])
    (ROOT/'results/exact_work_counts.json').write_text(json.dumps(out,indent=2)+'\n')
