#!/usr/bin/env python3
"""Fresh integer verification of the open-eight M0 ground lower bound.

SU(2) invariance implies every integer-spin multiplet contains an M0 vector,
so the M0 ground lower bound is a lower bound on the entire open cluster.
"""
import hashlib,json,time
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parents[1]/'upstream/extracted/cases/spin2_campaign/higher_inputs'
def verify():
    t=time.monotonic();n=8;rec=json.loads((SRC/'open8_m0.json').read_text())
    vecpath=SRC/rec['vector_file'];q=json.loads(vecpath.read_text());lo=F(rec['lower'])
    codes=[];words=[];index={};powers=[5**k for k in range(n)]
    for code in range(5**n):
        r=[code//p%5 for p in powers]
        if sum(r)==2*n:index[code]=len(codes);codes.append(code);words.append(r)
    assert len(q)==len(codes)==38165 and all(isinstance(x,int) and x>0 for x in q)
    y=[0]*len(q);edges=0
    for j,(code,r) in enumerate(zip(codes,words)):
        y[j]+=2*sum((r[k]-2)*(r[k+1]-2) for k in range(n-1))*q[j]
        for k in range(n-1):
            a,b=r[k:k+2]
            if a<4 and b>0:
                i=index[code+powers[k]-powers[k+1]];y[i]-=(4-a)*b*q[j];edges+=1
            if a>0 and b<4:
                i=index[code-powers[k]+powers[k+1]];y[i]-=a*(4-b)*q[j];edges+=1
    margins=[yi*lo.denominator-2*qi*lo.numerator for yi,qi in zip(y,q)]
    assert min(margins)>=0
    density=lo/F(n-1)
    assert density>F(-39,8)
    result={'cluster_length':n,'M':0,'dimension':len(q),'integer_offdiagonal_edges':edges,
      'all_integer_inequalities_pass':True,'lower_energy':str(lo),'periodic_lower_energy_per_bond':str(density),
      'safe_dyadic_lower_per_bond':'-39/8','scope':'Any periodic L>=8, any z seam twist; SU2 ground multiplet supplies M0 open-cluster minimum',
      'source_vector_sha256':hashlib.sha256(vecpath.read_bytes()).hexdigest(),'minimum_integer_margin':str(min(margins)),
      'seconds':time.monotonic()-t}
    (ROOT/'cluster_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':verify()
