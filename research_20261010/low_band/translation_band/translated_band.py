"""Translation-compressed, first-order dressed one-triplet band.
One exact sparse column supplies all circulant G/A/B moments. Fourier symbols
on tori with side lengths dividing eight lie in Q(sqrt(2)), handled exactly.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from dataclasses import dataclass
import json,math,time,gzip,argparse,resource
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RESEARCH=BAND.parent
sys.path.insert(0,str(RESEARCH/'symmetry'));sys.path.insert(0,str(BAND))
from symmetric_ground import Model
import number_sector_tail as NT
from low_band_certificate import down,upper_round,lower_round

@dataclass(frozen=True)
class Quad:
    a:F=F(0)
    b:F=F(0)
    def __post_init__(self):
        object.__setattr__(self,'a',F(self.a));object.__setattr__(self,'b',F(self.b))
    @staticmethod
    def cast(v):return v if isinstance(v,Quad) else Quad(v)
    def __add__(self,o):
        o=self.cast(o);return Quad(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return Quad(-self.a,-self.b)
    def __sub__(self,o):return self+-self.cast(o)
    def __rsub__(self,o):return self.cast(o)+-self
    def __mul__(self,o):
        o=self.cast(o);return Quad(self.a*o.a+2*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.cast(o);d=o.a*o.a-2*o.b*o.b;assert d
        return self*Quad(o.a/d,-o.b/d)
    def __float__(self):return float(self.a)+math.sqrt(2)*float(self.b)
    def sign(self):
        a,b=self.a,self.b
        if not b:return (a>0)-(a<0)
        if a>=0 and b>0:return 1
        if a<=0 and b<0:return -1
        if a>0:return (a*a>2*b*b)-(a*a<2*b*b)
        return (2*b*b>a*a)-(2*b*b<a*a)
    def bounds(self,bits=100):
        d=1<<bits;l=F(math.isqrt(2*d*d),d);h=l+F(1,d)
        return (self.a+self.b*l,self.a+self.b*h) if self.b>=0 else (self.a+self.b*h,self.a+self.b*l)
    def json(self):return [str(self.a),str(self.b)]

COS=[Quad(1),Quad(0,F(1,2)),Quad(),Quad(0,F(-1,2)),Quad(-1),Quad(0,F(-1,2)),Quad(),Quad(0,F(1,2))]

def translator(nx,ny,dx,dy):
    N=nx*ny;dx%=nx;dy%=ny;mask=(1<<(2*N))-1;rowmask=(1<<(2*ny))-1
    sx=2*ny*dx;sy=2*dy
    def tr(st):
        if dx:st=((st<<sx)|(st>>(2*N-sx)))&mask
        if dy:
            out=0
            for x in range(nx):
                row=(st>>(2*ny*x))&rowmask
                row=((row<<sy)|(row>>(2*ny-sy)))&rowmask
                out|=row<<(2*ny*x)
            st=out
        return st
    return tr

def displacement_rep(nx,ny,dx,dy):
    dx=min(dx%nx,(-dx)%nx);dy=min(dy%ny,(-dy)%ny)
    return tuple(sorted((dx,dy))) if nx==ny else (dx,dy)

def contraction(m,left,right,dx,dy):
    tr=translator(m.nx,m.ny,-dx,-dy)
    return sum(c*right.get(tr(st),0)*m.weight(st) for st,c in left.items())

def moments(nx,ny,g):
    start=time.monotonic();m=Model(nx,ny,g);bare={3:1};Tbare=m.apply(bare)
    W={3:2*m.den};W.update({st:-c for st,c in Tbare.items() if m.q(st)==3})
    TW=m.apply(W);assert all(m.q(st) in [1,3,5] for st in TW)
    reps=sorted({displacement_rep(nx,ny,dx,dy) for dx in range(nx) for dy in range(ny)})
    corr={}
    for dx,dy in reps:
        corr[dx,dy]=[contraction(m,W,W,dx,dy),contraction(m,W,TW,dx,dy),contraction(m,TW,TW,dx,dy)]
    arrays=[[[corr[displacement_rep(nx,ny,dx,dy)][j] for dy in range(ny)] for dx in range(nx)] for j in range(3)]
    tag=f'translated_{nx}x{ny}_g{g}'.replace('/','d')
    rec=dict(status='exact_translation_moments_pending_independent_review',nx=nx,ny=ny,N=m.N,g=str(g),
        matrix_denominator=m.den,trial_column_support=len(W),reached_column_support=len(TW),
        column_rule='W_r=2*den*(I-C_create/2)|t+_r>, where C_create raises total rung triplet number by two',
        displacement_representatives=[list(x) for x in reps],
        G=[[str(x) for x in row] for row in arrays[0]],A=[[str(x) for x in row] for row in arrays[1]],B=[[str(x) for x in row] for row in arrays[2]],
        seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (HERE/f'{tag}_moments.json').write_text(json.dumps(rec,indent=2))
    with gzip.open(HERE/f'{tag}_column.json.gz','wt') as f:json.dump(dict(W=[[str(s),str(c)] for s,c in sorted(W.items())],TW=[[str(s),str(c)] for s,c in sorted(TW.items())]),f)
    print('MOMENTS',tag,'support',len(W),len(TW),'sec',rec['seconds'],flush=True)
    return rec

def symbol(matrix,nx,ny,kx,ky):
    return sum((int(matrix[dx][dy])*COS[((8*kx*dx)//nx+(8*ky*dy)//ny)%8] for dx in range(nx) for dy in range(ny)),Quad())

def fourier_certificate(rec):
    nx,ny=rec['nx'],rec['ny'];assert 8%nx==8%ny==0;den=rec['matrix_denominator'];rows=[]
    for kx in range(nx):
        for ky in range(ny):
            G=symbol(rec['G'],nx,ny,kx,ky);A=symbol(rec['A'],nx,ny,kx,ky);B=symbol(rec['B'],nx,ny,kx,ky)
            assert G.sign()>0
            theta=A/(den*G);r2=B/(den*den*G)-theta*theta;assert r2.sign()>=0
            lo,hi=theta.bounds();rl,rh=r2.bounds()
            row=dict(momentum=[kx,ky],G=G.json(),A=A.json(),B=B.json(),theta=theta.json(),residual_squared=r2.json(),
                theta_lower=str(down(lo,digits=12)),theta_upper=str(-down(-hi,digits=12)),residual_squared_upper=str(-down(-rh,digits=12)))
            assert (Quad(F(row['residual_squared_upper']))-r2).sign()>=0
            rows.append(row)
    out=dict(status='exact_Qsqrt2_fourier_trial_certificate_pending_independent_review',source_moments=rec,
       triplet_multiplicity=3,retained_triplet_band_dimension=3*nx*ny,
       ritz_max_upper=str(max(F(x['theta_upper']) for x in rows)),residual_squared_bound=str(max(F(x['residual_squared_upper']) for x in rows)),modes=rows)
    tag=f'translated_{nx}x{ny}_g{rec["g"]}'.replace('/','d');(HERE/f'{tag}_fourier.json').write_text(json.dumps(out,indent=2))
    print('FOURIER',nx,ny,'rmax',float(F(out['ritz_max_upper'])),'eta2',float(F(out['residual_squared_bound'])),flush=True)
    return out

def check_physical_column_small(rec):
    """Exact comparison against the independently saved general rectangular map."""
    from low_band_certificate import make_map
    nx,ny=rec['nx'],rec['ny'];g=F(rec['g']);basis,Arect,den,weights,H=make_map(nx,ny,g,1,1,3)
    m=Model(nx,ny,g);bare={3:1};W={3:2*m.den};W.update({s:-c for s,c in m.apply(bare).items() if m.q(s)==3})
    states=[sum(v<<(2*i) for i,v in enumerate(st)) for st in basis];v=[W.get(st,0) for st in states]
    hv=[]
    for i in range(Arect.shape[0]):hv.append(sum(int(Arect.data[j])*v[int(Arect.indices[j])] for j in range(Arect.indptr[i],Arect.indptr[i+1])))
    n=sum(int(w)*c*c for w,c in zip(weights,v));h=sum(int(w)*c*d for w,c,d in zip(weights,v,hv));b=sum(int(w)*c*c for w,c in zip(weights,hv))
    assert n==int(rec['G'][0][0])
    assert F(h,den)==F(int(rec['A'][0][0]),m.den)
    assert F(b,den*den)==F(int(rec['B'][0][0]),m.den*m.den)
    return dict(G00_exact=True,A00_exact=True,B00_exact=True,trial_dimension=len(basis),reached_dimension=len(hv))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--nx',type=int,default=4);p.add_argument('--ny',type=int,default=4);p.add_argument('--g',default='3/100');p.add_argument('--check-small',action='store_true');a=p.parse_args();g=F(a.g)
    rec=moments(a.nx,a.ny,g);out=fourier_certificate(rec)
    if a.check_small:
        c=check_physical_column_small(rec);(HERE/f'translated_{a.nx}x{a.ny}_g{g}_crosscheck.json'.replace('/','d')).write_text(json.dumps(c,indent=2));print('CROSSCHECK',c,flush=True)
