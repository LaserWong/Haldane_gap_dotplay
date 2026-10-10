"""Exact fixed-center translated-triplet moments; no physical expansion.

The physical family w(z)=u+z v has Qu=u and Qv=3v. Fixed-center
H(p)=Q+pV moments follow analytically from the audited diagonal-family
G(z), A(z), B(z) polynomial data. The derivation is documented in PROOF.md.
"""
import json,sys,math,hashlib
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;R=HERE.parent;BAND=R/'low_band'
sys.path.insert(0,str(BAND/'translation_band'))
from translated_band import Quad,COS

def add(a,b):
 out=[F(0)]*max(len(a),len(b))
 for i,x in enumerate(a):out[i]+=x
 for i,x in enumerate(b):out[i]+=x
 return out

def mul(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out

def interpolate(xs,ys):
 out=[F(0)]*len(xs)
 for i,y in enumerate(ys):
  term=[y]
  for j,x in enumerate(xs):
   if i!=j:term=[v/(xs[i]-x) for v in mul(term,[-x,F(1)])]
  out=add(out,term)
 return out

def evaluate(cs,g):return sum((v*g**i for i,v in enumerate(cs)),F(0))
def source_path(nx,ny,g):
 if g<F(3,50):parent=BAND/'translation_band'
 elif g==F(3,50):parent=BAND/'frontier_g006'
 else:parent=BAND/'frontier_g007_g010'/f'g{g}'.replace('/','d')
 return parent/f'translated_{nx}x{ny}_g{g}_moments.json'.replace('/','d')

def extract(nx,ny):
 xs=list(map(F,('3/100','1/25','1/20','3/50','7/100','2/25','1/10')))
 ps=[source_path(nx,ny,g) for g in xs];rs=[json.loads(p.read_text()) for p in ps];out={};checks=0
 for key,power,degree in (('G',2,2),('A',3,3),('B',4,4)):
  arr=[]
  for i in range(nx):
   row=[]
   for j in range(ny):
    ys=[F(int(r[key][i][j]),4*r['matrix_denominator']**power) for r in rs]
    cs=interpolate(xs[:degree+1],ys[:degree+1]);assert len(cs)==degree+1
    for x,y in zip(xs,ys):assert evaluate(cs,x)==y;checks+=1
    row.append(list(map(str,cs)))
   arr.append(row)
  out[key]=arr
 # Fixed Q-eigenspaces imply the absent Gram cross coefficient and the exact
 # constant/linear Q-square identities. These are structural guard checks.
 for i in range(nx):
  for j in range(ny):
   gg,aa,bb=[list(map(F,out[k][i][j])) for k in ('G','A','B')]
   assert gg[1]==0 and aa[0]==gg[0] and bb[0]==gg[0] and bb[1]==2*aa[1]
 return dict(nx=nx,ny=ny,N=nx*ny,degrees={'G':2,'A':3,'B':4},
  normalization={'G':'4*d^2','A':'4*d^3','B':'4*d^4'},coefficient_arrays=out,
  exact_source_evaluation_checks=checks,source_sha256={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ps})

def symbol(arr,nx,ny,kx,ky):
 return sum((F(arr[i][j])*COS[((8*kx*i)//nx+(8*ky*j)//ny)%8] for i in range(nx) for j in range(ny)),Quad())

def fixed_modes(raw,z):
 nx,ny=raw['nx'],raw['ny'];arrays={k:[[None]*ny for _ in range(nx)] for k in ('G','Q','V','Q2','C','D')}
 for i in range(nx):
  for j in range(ny):
   gg,aa,bb=[list(map(F,raw['coefficient_arrays'][k][i][j])) for k in ('G','A','B')]
   vv=[aa[1],aa[2]-3*gg[2],aa[3]]
   cc=[2*vv[0],4*vv[1],6*vv[2]]
   dd=[bb[2]-9*gg[2]-cc[1],bb[3]-cc[2],bb[4]]
   vals={'G':gg[0]+z*z*gg[2],'Q':gg[0]+3*z*z*gg[2],
    'V':evaluate(vv,z),'Q2':gg[0]+9*z*z*gg[2],
    'C':evaluate(cc,z),'D':evaluate(dd,z)}
   for k,v in vals.items():arrays[k][i][j]=v
 rows=[]
 for kx in range(nx):
  for ky in range(ny):
   v={k:symbol(arr,nx,ny,kx,ky) for k,arr in arrays.items()};G=v['G'];assert G.sign()>0
   theta=[v['Q']/G,v['V']/G]
   second=[v['Q2']/G,v['C']/G,v['D']/G]
   var=[second[0]-theta[0]*theta[0],second[1]-2*theta[0]*theta[1],second[2]-theta[1]*theta[1]]
   assert all(x.sign()>=0 for x in (var[0],var[2],4*var[0]*var[2]-var[1]*var[1]))
   rows.append(dict(momentum=[kx,ky],gram_symbol=G.json(),theta_coefficients=[x.json() for x in theta],
    second_moment_coefficients=[x.json() for x in second],residual_squared_coefficients=[x.json() for x in var]))
 return dict(nx=nx,ny=ny,center=str(z),triplet_multiplicity=3,modes=rows,
  coefficient_arrays={k:[[str(x) for x in row] for row in a] for k,a in arrays.items()})

def save_sources():
 for nx,ny in ((4,4),(8,4)):
  raw=extract(nx,ny);(HERE/f'odd_polynomial_{nx}x{ny}.json').write_text(json.dumps(raw,indent=2)+'\n')
if __name__=='__main__':save_sources()
