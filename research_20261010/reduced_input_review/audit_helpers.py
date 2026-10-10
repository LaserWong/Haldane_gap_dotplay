"""Independent reduced-input proof helpers. Never imports producer modules."""
import os, resource
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[k]='1'
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'): os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys, json, math, itertools, hashlib, subprocess, time
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from functools import lru_cache
import numpy as np
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parent
GRID=1<<384

def load(path): return json.loads(Path(path).read_text())
def save(name,obj): (HERE/'results'/name).write_text(json.dumps(obj,indent=2)+'\n')
def floor(x,grid=GRID): x=F(x); return F(x.numerator*grid//x.denominator,grid)
def ceil(x,grid=GRID): return -floor(-x,grid)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
@lru_cache(None)
def expi(x):
    x=F(x);y=abs(x);k=0
    while y>F(1,8): y/=2;k+=1
    term=total=F(1)
    for j in range(1,91):term*=y/j;total+=term
    lo=floor(total);hi=ceil(total+(term*y/91)/(1-y/92))
    for _ in range(k):lo=floor(lo*lo);hi=ceil(hi*hi)
    return (lo,hi) if x>=0 else (floor(1/hi),ceil(1/lo))
def loglo(x):
    x=F(x);assert x>1;k=0
    while x>=2:x/=2;k+=1
    def atom(t):
        z=(t-1)/(t+1)
        return 2*sum((z**(2*j+1)/F(2*j+1) for j in range(100)),F(0))
    return k*atom(F(2))+atom(x)
def sqrtlo(x):
    x=F(x);d=10**40;n=math.isqrt(x.numerator*d*d//x.denominator);s=F(n,d)
    assert s*s<=x<(s+F(1,d))**2
    return s

def graph(nx,ny):
    edges=Counter()
    for x in range(nx):
        for y in range(ny):
            i=x*ny+y
            for j in [((x+1)%nx)*ny+y,x*ny+(y+1)%ny]: edges[tuple(sorted((i,j)))]+=1
    ids={};orbits=[];keys={}
    for i,j in itertools.combinations(range(nx*ny),2):
        a,b=divmod(i,ny);c,d=divmod(j,ny)
        dx=min((a-c)%nx,(c-a)%nx);dy=min((b-d)%ny,(d-b)%ny)
        key=tuple(sorted((dx,dy))) if nx==ny else (dx,dy)
        if key not in keys:keys[key]=len(orbits);orbits.append([])
        k=keys[key];orbits[k].append((i,j));ids[i,j]=k
    return edges,orbits,ids

def rebuild_fs():
    nx=ny=8;n=nx*ny;ed,orbits,ids=graph(nx,ny)
    p=HERE/'results/graph_8x8.txt'
    p.write_text(f'{n} {len(orbits)}\n{len(ed)}\n'+''.join(f'{i} {j} {w}\n' for (i,j),w in sorted(ed.items()))+' '.join(str(ids[i,j]) for i,j in itertools.combinations(range(n),2))+'\n')
    out=HERE/'results/geometry_fs_8x8.json';t=time.monotonic()
    with (HERE/'logs/fs_only.log').open('w') as f:
        subprocess.run([str(HERE/'rebuild_fs_only'),str(p),str(out)],stderr=f,stdout=f,check=True)
    rec=load(out);assert rec['all_q4']==math.comb(64,4)==635376
    assert set(rec)=={'N','orbits','all_q4','F','S'}
    return dict(seconds=time.monotonic()-t,all_q4=rec['all_q4'],all_q6=0,outputs=['F','S'],child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)

def ground_gk(nx,ny,g,geom):
    """No H², residual, q6, V or W is accepted or calculated."""
    ed,orbits,ids=graph(nx,ny);d=1+len(orbits);h=2*g.numerator;den=4*g.denominator
    D=np.diag([1]+[3*len(o) for o in orbits]).astype(object)
    C=np.zeros((d,d),dtype=object)
    for col in range(d):
        target=defaultdict(int);vacuum=0
        if col==0:
            for pair,mul in ed.items():target[pair]+=h*mul
        else:
            for i,j in orbits[col-1]:
                target[i,j]+=2*den-2*h*ed.get((i,j),0);vacuum+=3*h*ed.get((i,j),0)
                for (a,b),mul in ed.items():
                    if a==i and b!=j:target[tuple(sorted((b,j)))]+=h*mul
                    elif b==i and a!=j:target[tuple(sorted((a,j)))]+=h*mul
                    elif a==j and b!=i:target[tuple(sorted((i,b)))]+=h*mul
                    elif b==j and a!=i:target[tuple(sorted((i,a)))]+=h*mul
        C[0,col]=vacuum
        for row,orb in enumerate(orbits,1):
            vals={target[pair] for pair in orb};assert len(vals)==1;C[row,col]=next(iter(vals))
    fm=np.array(geom['F'],dtype=object);sm=np.array(geom['S'],dtype=object);q=d-1
    E=np.vstack([np.zeros((1,q),dtype=object),fm])
    G=np.block([[D,np.zeros((d,q),dtype=object)],[np.zeros((q,d),dtype=object),fm]])
    K=np.block([[D@C,h*E],[h*E.T,4*den*fm+h*sm]])
    assert np.array_equal(G,G.T) and np.array_equal(K,K.T)
    return G,K

def independent_columns(G):
    r=[[F(x) for x in row] for row in G];cols=[]
    for j in range(len(r)):
        p=r[j][j];assert p>=0
        if p:
            cols.append(j)
            for a in range(j+1,len(r)):
                for b in range(j+1,len(r)):r[a][b]-=r[a][j]*r[j][b]/p
        else:assert all(r[j][a]==0 for a in range(j,len(r)))
    return cols

def upper_trace(rec,beta):
    shift=F(rec['blocks'][0]['eigen_upper'][0]);hi=F(0)
    for block in rec['blocks']:
        for l in block['eigen_lower']:hi+=block['multiplicity']*expi(-beta*(F(l)-shift))[1]
    for row in rec['number_sector_bins']['bins'][2:]:
        hi+=row['multiplicity']*expi(-beta*(F(row['lower'])-shift))[1]
    return hi

def scalar(beta,upper16,upper32,largest_shift,largest_normalized_lower):
    """Exactly three denominator traces, one numerator trace. All bounds directed."""
    e0=F(upper16['energy_shift'])+F(upper16['blocks'][0]['eigen_upper'][0])
    e1=F(upper32['energy_shift'])+F(upper32['blocks'][0]['eigen_upper'][0])
    e2=F(largest_shift);q=F(largest_normalized_lower)
    t0=upper_trace(upper16,beta);t1=upper_trace(upper16,2*beta);t2=upper_trace(upper32,2*beta)
    j1=floor(expi(-2*beta*e2+8*beta*e0)[0]*q/t0**8,10**16)
    j2=floor(expi(-4*beta*e2+16*beta*e0)[0]*q*q/t1**8,10**16)
    c0=floor(expi(-2*beta*e2+4*beta*e1)[0]*q/t2**2,10**16)
    def G(z):assert 0<z<=1;return 1-(1-z)**2/(2*z*z)
    a=floor(G(j1),10**16);b=floor(G(j2*a),10**16);c=floor(G(c0**4*a*a*b),10**16)
    assert all(0<x<=1 for x in [a,b,c])
    abc=[floor(x,10**18) for x in [a*sqrtlo(b),a*a*b*sqrtlo(c),a**4*b*b*c]]
    return dict(J1=j1,J2=j2,C0=c0,permuted=[a,b,c],canonical=abc)

def replay(abc,beta):
    defects=[ceil(1-x,10**18) for x in abc];n=8;updates=[]
    for round in range(65):
        u=max(defects)
        if 0<u<=F(1,500):
            gap=floor(loglo(1/(32*u))/beta,10**12)
            assert expi(beta*gap)[1]*32*u<1
            return dict(n=n,beta=beta,u=u,defects=defects,updates=updates,gap=gap)
        for _ in range(3):
            p=(1-defects[0])**4*(1-defects[1])**2*(1-defects[2]);assert 0<p<=1
            new=ceil((1-p)**2/(2*p*p),10**18);assert 0<=new<1
            defects=defects[1:]+[new]
        n*=2;beta*=2;updates.append(list(defects))
    raise AssertionError('No accepted canonical replay')

def window(abc,beta):
    def one(s,t):
        p=s*s*t;assert p>F(1,2)
        w=(1+sqrtlo(2*p-1))/2;r=(1-w)/w;d=t/(1+r*r)
        ans=floor((1-r)*min(s*sqrtlo(d),d),10**40)
        assert (2*w-1)**2<=2*p-1 and r<1
        return ans
    a,b,c=abc;assert b>F(1,2);sx=a*a*sqrtlo(2*b-1)
    ty=one(b,c);thermal=one(sx,ty);assert thermal>F(1,2)
    gap=floor(loglo(thermal/(1-thermal))/beta,10**12)
    assert expi(beta*gap)[1]*(1-thermal)<thermal
    return thermal,gap
