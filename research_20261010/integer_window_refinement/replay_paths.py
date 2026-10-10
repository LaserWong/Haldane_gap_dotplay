"""Exact directed scalar replay over previously reviewed physical inputs."""
import replay as R
import json,hashlib,time,math
F=R.F
SOURCE=R.HERE.parent/'chain_frontier_above_02/expanded_inputs.json'
def sqrtlo(x):return R.powerbox(x,1,2)[0]
def uniform(a,b):return R.down(a*a*sqrtlo(2*b-1)) if b>F(1,2) else F(-1)
def oldwin(s,t,k):
 p=max(s*s*t,k)
 if p<=F(1,2):return F(-1)
 w=R.wlower(p);r=(1-w)/w;d=t/(1+r*r)
 return R.down((1-r)*min(s*sqrtlo(d),d))
def checkgap(p,beta,gap):
 assert p>F(1,2) and R.expbox(beta*gap)[1]<p/(1-p)
 return dict(purity_lower=str(p),purity_display=float(p),beta=str(beta))
def main():
 start=time.monotonic();recs=json.loads(SOURCE.read_text())[:3];proposals=json.loads((R.HERE/'path_scan.json').read_text())[:3];out=[]
 for rec,proposal in zip(recs,proposals):
  prop=proposal['best'];beta=F(str(prop['beta']));gap=F(int(prop['gap']*10**9)-1,10**9);s=rec['small'];delta=F(rec['large']['exact_rayleigh'])-2*F(s['exact_rayleigh']);L=R.expbox(-2*beta*delta)[0];J=R.down(L/R.trace(s,beta)**4);C=R.down(L/R.trace(s,2*beta)**2)
  initial=max(oldwin(sqrtlo(J),J,J),uniform(sqrtlo(J),C));windows=[dict(n=4,**checkgap(initial,beta,gap))]
  lc=s['relative_form_bound']['local_certificate'];short=[1-2*F(lc['a'])-M*F(lc['b']) for M in [2,3]];assert min(short)>gap
  a=R.G(J);b=R.G(R.down(C*C*a));n=8;be=2*beta
  for _ in range(prop['time_steps']):
   P=R.down(a*a*b);purity=max(uniform(a,b),oldwin(sqrtlo(P),P,P));windows.append(dict(n=n,a=str(a),b=str(b),**checkgap(purity,be,gap)))
   a=R.G(P);b=R.G(R.down(b*b*a));assert a>0 and b>0;n*=2;be*=2
  assert prop['canonical_steps']==0
  P=R.down(a*a*b);S=sqrtlo(P);T=P;u=max(1-S,1-T)
  gap=min(gap,F(int(math.log(float(1/(5*u)))/float(be)*10**9)-1,10**9));assert 0<u<=F(1,100) and R.expbox(be*gap)[1]<1/(5*u) and n==prop['onset']
  out.append(dict(g=rec['g'],status='EXACT_SCALAR_REPLAY_PASS_PENDING_INDEPENDENT_NEW_LEMMA_REVIEW',beta=str(beta),gap_lower=str(gap),gap_display=float(gap),time_steps=prop['time_steps'],canonical_steps=0,asymptotic_onset=n,asymptotic_beta=str(be),u=str(u),short_M2_M3=list(map(str,short)),windows=windows))
  print(rec['g'],float(gap),'PASS',flush=True)
 result=dict(status='EXACT_NEW_SCALAR_PATHS_PASS_PHYSICAL_INPUTS_INHERITED',results=out,physical_inputs_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),seconds=time.monotonic()-start)
 (R.HERE/'replay_paths.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
