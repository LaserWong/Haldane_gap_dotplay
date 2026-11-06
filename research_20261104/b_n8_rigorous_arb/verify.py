# Verifier: all bounds in arb ball arithmetic from enclosures12.json / enclosures8.json.
import json, numpy as np, time
from flint import arb, fmpq, ctx
t0=time.time()
a=arb(fmpq(700741,500000)); b0=arb(fmpq(49,4)); CLAIM=arb(fmpq(1900577,1000000))
def enc(rec):
    eta=arb(rec['eta']); de=arb(rec['delta'])
    # arb(string with +/-) parses to a ball containing the stored ball; take its upper endpoint as an exact bound
    eu=eta.upper(); du=de.upper()
    return [(arb(x), eu*abs(arb(x))+du) for x in rec['lam_t']]
E12=json.load(open('enclosures12.json')); E8=json.load(open('enclosures8.json'))
import os
if os.path.exists('fix12.json'):   # blocks recomputed after the flint x**2-on-ball nan fix
    F=json.load(open('fix12.json')); print('overriding blocks from fix12.json:',sorted(F)); E12.update(F)
for key,rec in list(E12.items())+[('L8',E8)]:
    for f in ('eta','delta')+(('trace','frob2') if key!='L8' else ()):
        assert arb(rec[f]).is_finite(), ('non-finite',key,f)
    assert all(np.isfinite(rec['lam_t'])), ('non-finite lam_t',key)
lo12=[];hi12=[];m12=[]; dim=0; tr=arb(0); fr=arb(0)
for key,rec in E12.items():
    mu=rec['mult']; dim+=mu*len(rec['lam_t']); tr+=mu*arb(rec['trace']); fr+=mu*arb(rec['frob2'])
    for x,r in enc(rec): lo12.append(x-r); hi12.append(x+r); m12.append(mu)
# Sz=+-12: the two fully polarized states, E=12 exactly (H acts diagonally: 12 bonds * 1*1)
lo12+= [arb(12)]; hi12+=[arb(12)]; m12+=[2]; dim+=2; tr+=24; fr+=2*144
keys={tuple(map(int,k.split(','))) for k in E12}
assert keys=={(s,k) for s in range(12) for k in range(7)}, 'missing blocks'
print('L12 enclosures:',len(lo12),'distinct, total multiplicity',dim,'(3^12 =',3**12,')'); assert dim==3**12
print('  sum_blocks Tr H_k =',tr,'(exact Tr H = 0)  sum ||H_k||_F^2 =',fr,'(exact Tr H^2 = 8503056)')
assert tr.contains(0) and fr.contains(8503056)
lo8=[];hi8=[]
for x,r in enc(E8): lo8.append(x-r); hi8.append(x+r)
assert len(lo8)==3**8 and E8['trace_exact']==0 and E8['frob2_exact']==8*12*3**6
rad12=max(float((h-l).mid()) for h,l in zip(hi12,lo12))/2; rad8=max(float((h-l).mid()) for h,l in zip(hi8,lo8))/2
print('  max enclosure radius: L12 %.3e  L8 %.3e'%(rad12,rad8))
# (1) Z12(49/4): each true eigenvalue lies in [lo,hi]; exp(-b0(E+12a)) <= exp(-b0(lo+12a)) (b0>0)
Z=sum((mu*(-b0*(l+12*a)).exp() for l,mu in zip(lo12,m12)),arb(0))
print('(1) Z12(49/4) in',Z,'; rigorous upper endpoint', Z.upper().str(15),
      '\n    Z12 < 1.900577 :',bool(Z<CLAIM),'  margin >=',(CLAIM-Z).str(6))
# (2) sup_b f(b), f=Z12(2b)^(4/3)/Z8(b)^4 for b>=0.
#   Upper for Z12: bins of width w: c_j = multiplicity with lower bound in [x_j, x_j+w) -> term <= exp(-2b x_j).
#   Lower for Z8:  y_j = ceil of upper bound -> term >= exp(-b y_j). Evaluated with b as an arb ball [b1,b2].
w=fmpq(1,200)
def bins(vals,mults,shift,down):
    d={}
    for v,mu in zip(vals,mults):
        u=v+shift
        if down: j=int(np.floor((float(u.lower())-1e-9)/float(w))); assert arb(fmpq(j)*w)<=u.lower()
        else:    j=int(np.ceil((float(u.upper())+1e-9)/float(w)));  assert arb(fmpq(j)*w)>=u.upper()
        d[j]=d.get(j,0)+mu
    return [(arb(fmpq(j)*w),c) for j,c in sorted(d.items())]
X=bins(lo12,m12,12*a,True); Y=bins(hi8,[1]*len(hi8),8*a,False)
print('(2) bins: Z12',len(X),'Z8',len(Y),' (width 1/200, every edge checked in arb to lie outside the enclosure)')
def fup(b1,b2):
    B=arb(b1).union(arb(b2))   # ball containing [b1,b2]
    num=sum((c*(-2*B*x).exp() for x,c in X),arb(0)); den=sum((c*(-B*y).exp() for y,c in Y),arb(0))
    nu=num.upper(); dl=den.lower(); assert dl>0
    return (nu.log()*fmpq(4,3)-4*dl.log()).exp()
BMAX=64; todo=[(fmpq(i,2),fmpq(i+1,2)) for i in range(2*BMAX)]; worst=arb(0); wi=None; nint=0
while todo:
    b1,b2=todo.pop(); f=fup(b1,b2); nint+=1
    fu=f.upper()
    if fu>=arb(fmpq(1,10)) and b2-b1>fmpq(1,2000): m_=(b1+b2)/2; todo+= [(b1,m_),(m_,b2)]; continue
    if fu>worst: worst,wi=fu,(b1,b2)
print('    sup over b in [0,%d] <= %s  (worst interval [%s,%s]; %d intervals)'%(BMAX,worst.str(6),wi[0],wi[1],nint))
assert worst<arb(fmpq(1,2))
# tail b>=BMAX: Z12(2b) <= D exp(-2b x0), Z8(b) >= exp(-b y0) => ln f <= (4/3)ln D + b c,  c = -(8/3)x0 + 4 y0
x0=X[0][0]                         # <= every Z12 shifted lower bound (bins sorted)
y0=min(Y,key=lambda t:float(t[0]))[0]   # >= ground-state shifted upper bound of L=8 (bin edge)
c=-fmpq(8,3)*x0+4*y0; tail=(fmpq(4,3)*arb(3**12).log()+BMAX*c).exp()
print('    tail b>=%d: c in %s (<0 so decreasing), bound at %d: %s'%(BMAX,c.str(6),BMAX,tail.str(4))); assert c<0 and tail<arb(fmpq(1,2))
print('    => sup_b Z12(2b)^(4/3)/Z8(b)^4 <=',(worst if worst>tail else tail).str(6),'< 1/2')
print('verifier time %.1fs'%(time.time()-t0))
