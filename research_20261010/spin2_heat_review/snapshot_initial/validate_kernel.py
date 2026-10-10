#!/usr/bin/env python3
"""Independent Python-bigint column reconstruction, including small physical checks."""
import itertools,json,subprocess,time,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent;Q=2**56

def mul(x,y):
    z=[0]*4
    # Basis: sqrt(6)^b omega^a, integer polynomial reduction.
    for i,xi in enumerate(x):
      for j,yj in enumerate(y):
        ra=(i%2)+(j%2);om=(i//2)+(j//2);v=xi*yj*(6 if ra>=2 else 1);ra%=2
        if om<2:z[2*om+ra]+=v
        else:z[ra]-=v;z[2+ra]-=v
    return z

def conj(x):return (x[0]-x[2],x[1]-x[3],-x[2],-x[3])
def value(x,sgn=1):return x[0]+sgn*math.sqrt(6)*x[1]+complex(-.5,math.sqrt(3)/2)*(x[2]+sgn*math.sqrt(6)*x[3])
def block(n,m,tw):
    words=[w for w in itertools.product(range(-2,3),repeat=n) if sum(w)==m];idx={w:i for i,w in enumerate(words)}
    d=len(words);H=[[None]*d for _ in range(d)]
    rows=[{} for _ in words];b=39 if n>=8 else 40
    for j,w in enumerate(words):
        rows[j][j]=[512-b*n-8*sum(w[k]*w[(k+1)%n] for k in range(n)),0,0,0]
        for k in range(n):
            l=(k+1)%n
            for sign in [-1,1]:
                v=list(w);v[k]+=sign;v[l]-=sign
                if min(v)<-2 or max(v)>2:continue
                c1=6-w[k]*(w[k]+sign);c2=6-w[l]*(w[l]-sign)
                rad=c1*c2
                if rad==24:h=[0,-8,0,0]
                else:h=[-4*math.isqrt(rad),0,0,0];assert math.isqrt(rad)**2==rad
                power=(w[0]-v[0]) if l==0 else 0
                phase=([1,0,0,0] if not power or tw=='I' else [-1,0,0,0] if tw=='P' else [0,0,1,0] if power==1 else [-1,0,-1,0])
                ent=mul(h,phase);i=idx[tuple(v)];rows[i][j]=[a+b for a,b in zip(rows[i].get(j,[0]*4),ent)]
    for i,row in enumerate(rows):
        for j,x in row.items():assert tuple(x)==conj(rows[j][i])
    # Conjugating sqrt(6) is a diagonal unitary gauge, exactly.
    g=[(-1)**w.count(0) for w in words]
    for i,row in enumerate(rows):
        for j,x in row.items():assert [x[0],-x[1],x[2],-x[3]]==[g[i]*g[j]*a for a in x]
    return words,rows

def calc(words,rows,c,col,horner=False):
    d=len(words);K=max(i for i,x in enumerate(c) if x);cur=[[0]*4 for _ in words];prev=[[0]*4 for _ in words];acc=[[0]*4 for _ in words]
    if not horner:cur[col][0]=Q
    for k in (range(K,-1,-1) if horner else range(K+1)):
        if not horner:
            for i in range(d):
                for a in range(4):acc[i][a]+=c[k]*cur[i][a]//Q
            if k==K:break
        nxt=[]
        for i,row in enumerate(rows):
            s=[0]*4
            for j,h in row.items():s=[a+b for a,b in zip(s,mul(h,cur[j]))]
            nxt.append([x//512 for x in s] if horner or k==0 else [x//256-y for x,y in zip(s,prev[i])])
        if horner:nxt[col][0]+=c[k]
        prev,cur=cur,nxt
    return cur if horner else acc

def main():
    t=time.monotonic();out=[]
    for n,m in [(3,0),(4,0),(4,-1)]:
      for tw in ['I','P','C']:
       words,rows=block(n,m,tw)
       for alg in ['chebyshev','horner']:
        cf=ROOT/f'coefficients_{alg}_Q56.txt';c=list(map(int,cf.read_text().split()))
        cmd=[str(ROOT/'heat_columns_ubsan'),str(n),tw,str(m),'0','2',str(cf),'horner_dump' if alg=='horner' else 'dump']
        p=subprocess.run(cmd,capture_output=True,text=True,check=True);lines=p.stdout.splitlines();d=len(words);pos=1
        for r in range(2):
            got=[]
            for _ in range(d):
                vals=lines[pos].split();assert vals[0]=='V';got.append(list(map(int,vals[2:]))+[0]*(2 if tw!='C' else 0));pos+=1
            code,mult,n0,n1=map(int,lines[pos].split());pos+=1
            w=tuple((code//5**k)%5-2 for k in range(n-1,-1,-1));col=words.index(w)
            expected=calc(words,rows,c,col,alg=='horner');assert got==expected,(n,m,tw,alg,r)
            nn=[0]*4
            for x in got:nn=[a+b for a,b in zip(nn,mul(x,conj(x)))]
            assert nn==[n0,n1,0,0]
        # Floating direct diagonalization strictly limited to d<=85 validation.
        A=np.zeros((d,d),complex)
        for i,row in enumerate(rows):
            for j,x in row.items():A[i,j]=value(x)/512
        lam,U=np.linalg.eigh(A);F=(U*np.exp(256*(lam-1)))@U.conj().T
        actual=np.array([value(x)/Q for x in got]);err=float(np.linalg.norm(actual-F[:,col]));assert err<2e-12
        out.append({'L':n,'M':m,'twist':tw,'algorithm':alg,'columns':2,'dimension':d,'python_bigint_bitwise_match':True,'ubsan_pass':True,'small_floating_column_error':err})
    result={'checks':out,'exact_columns':2*len(out),'seconds':time.monotonic()-t,'scope':'Python bigint reference is independent in ring multiplication and loop structure; tiny eigensolver is a diagnostic, not a premise.'}
    (ROOT/'results/kernel_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
