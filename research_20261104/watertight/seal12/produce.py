# Producer: builds n=34 row with W windows in audit_scalar.py's certificate format.
import os,sys,json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paths import audit_copy
os.environ.setdefault('AUDIT_DIGITS','700')
sys.argv=['x']
A=str(audit_copy() / 'research_20261010/uniform_smaller_second_initialization')
src=open(A+'_review/audit_scalar.py').read()
pre=src.split("producer_hash=")[0].replace("os.sched_setaffinity(0,{0});","").replace("P=Path(__file__).resolve().parent","P=Path('"+A+"_review')")
exec(pre)
from fractions import Fraction as F
full=sys_full=os.environ.get('AUDIT_FULL_R68')=='1';gap=F(os.environ['GAP']);W=int(os.environ['W'])
C=js(R/'uniform_second_moment_optimization/certificate.json');L=js(A/'long_certificate.json');cert=js(A/'certificate.json');M={k:[tuple(map(F,v)) for v in rows] for k,rows in C['moment_intervals'].items()}
U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']));mj=M['J'][-1][1];mn=M['N'][-1][1]
def sector(s,n):
 m,h=(mj,U**12) if s=='J' else (mn,V**12);v=pack(m,h,F(n,12));key=f'{s}{n}'
 return min(v,F(L[key]['bound'])) if key in L else v
ours=ints(A/'anchors.out');n=34
ray=F(ours['H0_68'],ours['N0_68'])+68*F(700741,500000)
Z1=exp_lower(-F(49,4)*ray) if full else 1;Z2=exp_lower(-2*F(49,4)*ray) if full else 1
N2=3*sector('N',68)
lo,hi=F(9,10),F(1)
for _ in range(40):
 mid=F(int((lo+hi)/2*10**10),10**10)
 if Z1-pack(mj,mid**12,F(68,12))-N2>0 and mj-mid**12>0:lo=mid
 else:hi=mid
ell=lo;force=Z1-pack(mj,ell**12,F(68,12))-N2;assert force>0 and 0<mj-ell**12<ell**12
tail=power(mj-ell**12,F(n,12))[1]+3*sector('N',n);Q=sector('J',68)+3*sector('N',68)
S=down((1+tail/ell**n)**-2);T=down(Z2*Q**-2)
states=[];windows=[];s,t=S,T
for j in range(W):
 size=n*2**j;beta=F(49,4)*2**j
 if j: s=down(G(prev[0]**2*prev[1]));t=down(G(prev[1]**2*s))
 states.append({'n':size,'beta':str(beta),'S':str(s),'T':str(t)})
 K=s*s*t;root=power(2*K-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho);own=down((1-rho)*min(s*power(d,F(1,2))[0],d))
 m=down(own-exp_upper(beta*gap)*(1-own));assert m>0,('window',j)
 windows.append({'from':size,'to':2*size,'purity':str(own),'margin':str(m)});prev=s,t
u=max(1-s,1-t);am=down(1-5*u*exp_upper(beta*gap));assert u<=F(1,100) and am>0,'asym'
row=dict(next(r for r in cert['rows'] if r['n']==34))
row.update({'gap':str(gap),'ell':str(ell),'forcing_margin':str(down(force)),'tail':str(up(tail)),'Q':str(up(Q)),'S':str(S),'T':str(T),'states':states,'windows':windows,
 'asymptotic':{**row['asymptotic'],'from':size,'beta':str(beta),'defect':str(u),'margin':str(am)},'full_R68_forcing':full,'closure_factor':str(1-am)})
out=dict(cert);out['rows']=[r for r in cert['rows'] if r['n']!=34]+[row]
name=os.environ['AUDIT_CERT'];open(str(A)+'/'+name,'w').write(json.dumps(out,indent=1))
print('wrote',name,'ell',ell,'closure factor',float(1-am),'from',size)
