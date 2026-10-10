#!/usr/bin/env python3
"""Independent exact audit. Writes only this review directory; no large traces."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import math, json, hashlib, subprocess, time, resource, os

ROOT=Path(__file__).resolve().parent
SNAP=ROOT/'snapshot_initial'
Q=1<<56
ZERO=(0,0,0,0)
ONE=(1,0,0,0)

def add(x,y): return tuple(a+b for a,b in zip(x,y))
def scale(x,n): return tuple(n*a for a in x)
def conj(x): return (x[0]-x[2],x[1]-x[3],-x[2],-x[3])

# Multiplication table computed directly from s^2=6 and z^2=-1-z.
TABLE={}
for i in range(4):
    for j in range(4):
        r=(i&1)+(j&1); z=(i//2)+(j//2); out=[0]*4
        weight=6 if r==2 else 1; r%=2
        if z<2: out[2*z+r]=weight
        else: out[r]=-weight; out[2+r]=-weight
        TABLE[i,j]=tuple(out)

def mul(x,y):
    out=[0]*4
    for i,a in enumerate(x):
        if not a: continue
        for j,b in enumerate(y):
            if b:
                for k,t in enumerate(TABLE[i,j]):
                    if t: out[k]+=a*b*t
    return tuple(out)

def phase(tw,k):
    if tw=='I': return ONE
    if tw=='P': return scale(ONE,(-1)**(k%2))
    return [ONE,(0,0,1,0),(-1,0,-1,0)][k%3]

def enc(w):
    c=0
    for m in w: c=5*c+m+2
    return c

def graph(n,m,tw):
    words=[w for w in product(range(-2,3),repeat=n) if sum(w)==m]
    loc={w:i for i,w in enumerate(words)}
    rows=[{} for _ in words]
    b8=39 if n>=8 else 40
    for i,w in enumerate(words):
        rows[i][i]=(512-b8*n-8*sum(w[k]*w[(k+1)%n] for k in range(n)),0,0,0)
    # Build raising moves only, then add their exact Hermitian adjoints.
    for j,w in enumerate(words):
        for k in range(n):
            ell=(k+1)%n
            if w[k]==2 or w[ell]==-2: continue
            v=list(w);v[k]+=1;v[ell]-=1;v=tuple(v);i=loc[v]
            central=(w[k] in (-1,0))+(w[ell] in (0,1))
            h=[(-16,0,0,0),(0,-8,0,0),(-24,0,0,0)][central]
            h=mul(h,phase(tw,1 if ell==0 else 0))
            rows[i][j]=add(rows[i].get(j,ZERO),h)
            rows[j][i]=add(rows[j].get(i,ZERO),conj(h))
    return words,rows

def check_graph(words,rows,tw):
    loc={w:i for i,w in enumerate(words)}
    checks=0
    for i,row in enumerate(rows):
        wi=words[i]
        for j,h in row.items():
            wj=words[j]
            assert h==conj(rows[j][i])
            p=(-1)**((wi.count(0)+wj.count(0))%2)
            assert (h[0],-h[1],h[2],-h[3])==scale(h,p)
            ti=loc[(wi[-1],)+wi[:-1]];tj=loc[(wj[-1],)+wj[:-1]]
            assert rows[ti][tj]==mul(phase(tw,wj[-1]-wi[-1]),h)
            assert rows[loc[wi[::-1]]][loc[wj[::-1]]]==conj(h)
            if sum(wi)==0:
                assert rows[loc[tuple(-x for x in wi)]][loc[tuple(-x for x in wj)]]==conj(h)
            checks+=1
    return checks

def orbits(words):
    # Closure under three generators, independently of direct group enumeration.
    n=len(words[0]);zero=sum(words[0])==0;remain=set(words);out=[]
    while remain:
        seed=min(remain);seen={seed};pending=[seed]
        while pending:
            w=pending.pop()
            nxt=[w[1:]+w[:1],w[::-1]]
            if zero:nxt.append(tuple(-x for x in w))
            for v in nxt:
                if v not in seen:seen.add(v);pending.append(v)
        assert seen<=remain
        remain-=seen;out.append((enc(seed),len(seen)*(1 if zero else 2),words.index(seed)))
    return out

def exact_fixed_point(rows,c,col):
    d=len(rows);cur=[ZERO]*d;cur[col]=(Q,0,0,0);old=[ZERO]*d;acc=[ZERO]*d
    degree=max(i for i,x in enumerate(c) if x)
    for k in range(degree+1):
        if c[k]:acc=[add(a,tuple(c[k]*v//Q for v in x)) for a,x in zip(acc,cur)]
        if k==degree:break
        new=[]
        for i,row in enumerate(rows):
            value=ZERO
            for j,h in row.items():value=add(value,mul(h,cur[j]))
            new.append(tuple(v//512 for v in value) if k==0 else tuple(v//256-u for v,u in zip(value,old[i])))
        old,cur=cur,new
    return acc

def limits():
    resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
    resource.setrlimit(resource.RLIMIT_CPU,(580,600))

def run_kernel(exe,n,tw,m,reps,block=None,start=0,count=None):
    if count is None:count=len(reps)
    cmd=[str(ROOT/'bin'/exe),str(n),tw,str(m),str(start),str(count),str(SNAP/'coefficients_chebyshev_Q56.txt'),'dump']
    if block:cmd.append(str(block))
    p=subprocess.run(cmd,text=True,capture_output=True,check=True,timeout=600,preexec_fn=limits)
    name=f'{exe}_L{n}_{tw}_M{m}_b{block}_s{start}_c{count}'
    (ROOT/'logs'/f'{name}.stderr').write_text(p.stderr)
    return p.stdout

def parse(text,d,tw):
    lines=iter(text.splitlines());meta=next(lines).split();result=[]
    while True:
        try:line=next(lines)
        except StopIteration:break
        coords=[]
        for i in range(d):
            if i:line=next(lines)
            t=line.split();assert t[0]=='V' and int(t[1])==i
            v=list(map(int,t[2:]));coords.append(tuple(v if tw=='C' else v+[0,0]))
        code,mult,n0,n1=map(int,next(lines).split());result.append((code,mult,n0,n1,coords))
    return meta,result

def ceilsqrt(n):
    r=math.isqrt(n);return r+(r*r<n)

def expbounds(x,K=160):
    assert 0<=x<K+2
    t=s=F(1)
    for k in range(1,K+1):t=t*x/k;s+=t
    return s,s+t*x/F(K+1)/(1-x/F(K+2))

def coefficients():
    supplied=json.loads((SNAP/'results/coefficient_audit.json').read_text());result={}
    for name,mu,J in [('chebyshev',128,320),('horner',256,640)]:
        w=[math.factorial(J)]
        for k in range(1,J+1):
            v,r=divmod(w[-1]*mu,k);assert r==0;w.append(v)
        S=sum(w);tau=F(w[-1]*mu,S*(J+1))/(1-F(mu,J+2))
        if name=='chebyshev':
            coeff=[sum(w[j]*w[j+k] for j in range(J+1-k))*(1 if k==0 else 2) for k in range(J+1)]
            den=S*S;assert sum(coeff)==den
            mass=0
            for K,x in enumerate(coeff):
                mass+=x
                if 4*Q*(den-mass)<den:break
            assert 4*tau<F(1,4*Q)
            analytic=4*tau+F(den-mass,den)
        else:coeff=w;den=S;K=J;analytic=2*tau
        c=[Q*v//den for v in coeff[:K+1]]
        assert c==list(map(int,(SNAP/f'coefficients_{name}_Q56.txt').read_text().split()))
        floor=sum((F(v,den)-F(a,Q) for v,a in zip(coeff,c)),F(0))
        total=analytic+floor
        for key,v in [('polynomial_analytic_error',analytic),('coefficient_floor_error',floor),('total_uniform_error',total)]:assert v==F(supplied[name][key])
        assert total<F(75 if name=='chebyshev' else 139,Q)
        A=sum((F(k*(k+1)*a,2*Q) for k,a in enumerate(c)),F(0))
        assert A==F(supplied[name]['weighted_recurrence_error'])
        result[name]={'K':K,'last_nonzero':max(k for k,a in enumerate(c) if a),'nonzero':sum(a>0 for a in c),'Q_minus_mass':Q-sum(c),'A':str(A),'tail_times_Q_display':float(tau*Q),'total_error_times_Q_display':float(total*Q),'strict_total_bound_numerator':75 if name=='chebyshev' else 139,'exact_metadata_match':True}
    return result

def run():
    begin=time.monotonic();out={'coefficient_audit':coefficients(),'blocks':[],'complete_traces':[]}
    c=list(map(int,(SNAP/'coefficients_chebyshev_Q56.txt').read_text().split()))
    A=F(out['coefficient_audit']['chebyshev']['A'])
    oldtraces={a['twist']:a for a in json.loads((SNAP/'results/full_L4_validation.json').read_text())['checks']}
    for n in [3,4]:
        for tw in ['I','P','C']:
            trace=0;error2=0;weights=0;repcnt=0
            for m in range(0,-2*n-1,-1):
                words,rows=graph(n,m,tw);d=len(words);gc=check_graph(words,rows,tw);reps=orbits(words)
                reference=run_kernel('chebyshev_columns',n,tw,m,reps)
                for exe in ['compressed_columns','compressed_fast']:
                    for block in [1,2,4,8]:assert reference==run_kernel(exe,n,tw,m,reps,block),(exe,n,tw,m,block)
                    # Nonzero start and a partial ending, when the sector is large enough.
                    if len(reps)>3:
                        assert run_kernel('chebyshev_columns',n,tw,m,reps,start=1,count=3)==run_kernel(exe,n,tw,m,reps,4,start=1,count=3)
                meta,emitted=parse(reference,d,tw);assert int(meta[4])==d and int(meta[5])==len(reps)
                assert len(emitted)==len(reps)
                for (code,mult,col),got in zip(reps,emitted):
                    cc,mm,n0,n1,coords=got;assert (cc,mm)==(code,mult)
                    expected=exact_fixed_point(rows,c,col);assert coords==expected,(n,tw,m,code)
                    squared=ZERO
                    for w,x in zip(words,coords):
                        parity=(w.count(0)-words[col].count(0))%2
                        assert x[0]==x[2]==0 if parity else x[1]==x[3]==0
                        squared=add(squared,mul(x,conj(x)))
                    assert squared==(n0,0,0,0) and n1==0 and n0>=0
                    trace+=mult*n0;weights+=mult;repcnt+=1
                eta=(5*ceilsqrt(d)+1)//2;E=75+math.ceil(eta*(A+137));error2+=(d if m==0 else 2*d)*E*E
                out['blocks'].append({'L':n,'twist':tw,'M':m,'dimension':d,'representatives':len(reps),'exact_graph_symmetry_checks':gc,'python_bigint_all_coordinates_match':True,'compressed_block_sizes':[1,2,4,8],'base_and_fast_ubsan_pass':True})
                print(f'L{n} {tw} M{m} all {len(reps)} representatives passed',flush=True)
            assert weights==5**n
            e=ceilsqrt(error2);r=math.isqrt(trace);lo=F(max(0,r-e)**2,Q*Q);hi=F((r+e+1)**2,Q*Q)
            exp_lo,exp_hi=expbounds(8*n*(F(5)-F(5951,1250)))
            record={'L':n,'twist':tw,'norm_integer':str(trace),'weight_sum':weights,'representatives':repcnt,'frobenius_error_numerator':e,'b5_lower':str(lo),'b5_upper':str(hi),'physical_lower':str(lo*exp_lo),'physical_upper':str(hi*exp_hi),'physical_trace_display':[float(lo*exp_lo),float(hi*exp_hi)]}
            if n==4:
                old=oldtraces[tw];assert str(trace)==old['integer_norm'] and e==old['frobenius_error_numerator']
                assert lo==F(old['b5_trace_lower']) and hi==F(old['b5_trace_upper'])
                vals=dict(l.split('=',1) for l in (SNAP/f'original_dependencies/thermal4_{tw}_exact.txt').read_text().splitlines() if '=' in l)
                rat=F(int(vals['numerator']),int(vals['denominator']))
                t=s=F(1)
                for j in range(1,641):t*=F(144,j);s+=t
                olderr=2*625*(t*F(144,641)/(1-F(144,642)))/s
                assert lo<rat-olderr<rat+olderr<hi
                record['archived_GMP_rational_strictly_enclosed']=True
            out['complete_traces'].append(record)
    out['elapsed_seconds']=time.monotonic()-begin
    (ROOT/'results/independent_exact_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print('ALL EXACT CHECKS PASSED',out['elapsed_seconds'],flush=True)

if __name__=='__main__':run()
