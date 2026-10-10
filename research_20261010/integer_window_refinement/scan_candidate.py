import replay as R
import math,json,time
F=R.F
SOURCE=R.HERE.parent/'chain_frontier_above_02/expanded_inputs.json'
recs=json.loads(R.SOURCE.read_text()); candidate=json.loads((R.HERE.parent/'chain_numerator_pair_block_025/block_2.json').read_text()); recs[0]['large']['exact_rayleigh']=candidate['exact_rayleigh']
def G(x):return 1-(1-x)**2/(2*x*x) if 0<x<=1 else -1
def gap(p,beta):return math.log(p/(1-p))/beta if .5<p<1 else -1
def oldwin(s,t,k):
 p=max(s*s*t,k)
 if p<=.5:return -1
 w=(1+math.sqrt(2*p-1))/2;r=(1-w)/w;d=t/(1+r*r)
 return (1-r)*min(s*math.sqrt(d),d)
def tfwin(a,b):return a*a*math.sqrt(2*b-1) if b>.5 else -1
out=[]
for rec in recs:
 s=rec['small'];info=s['expanded_band'];rho=float(F(s['exact_rayleigh']));alpha=float(F(info['alpha']));B=float(F(info['B']));delta=float(F(rec['large']['exact_rayleigh'])-2*F(s['exact_rayleigh']))
 terms=[(1,rho-float(F(s['ground_lower'])))]+[(t['multiplicity'],rho+8-float(F(t['lower']))) for t in info['comparison_endpoints'][1:]]+[(m,rho+8-alpha*e+B) for e,m in info['complete_reference_bins'] if e>=info['omitted_reference_excitation']]
 def trace(x):return sum(m*math.exp(x*c) for m,c in terms)
 lc=s['relative_form_bound']['local_certificate'];short=min(1-2*float(F(lc['a']))-M*float(F(lc['b'])) for M in [2,3]);best=None;passes=0
 for i in range(200,3001):
  beta=i/100;L=math.exp(-2*beta*delta);J=L/trace(beta)**4;C=L/trace(2*beta)**2;a=G(J);b=G(C*C*a) if a>0 else -1
  initial=max(oldwin(math.sqrt(J),J,J),tfwin(math.sqrt(J),C));lim=min(short,gap(initial,beta))
  if lim<=0:continue
  n=8;be=2*beta
  for ts in range(8):
   if not(0<a<1 and 0<b<1):break
   P=a*a*b;s0=math.sqrt(P);t0=P;k=P;nn=n;bb=be;cg=lim
   for cs in range(8):
    u=max(1-s0,1-t0)
    if 0<u<=.01:
     total=min(cg,math.log(1/(5*u))/bb)
     cand=dict(g=rec['g'],beta=beta,time_steps=ts,canonical_steps=cs,onset=nn,gap=total)
     passes+=1
     if best is None or total>best['gap']:best=cand
     break
    purity=oldwin(s0,t0,k)
    if purity<=.5:break
    cg=min(cg,gap(purity,bb));s0=G(k);t0=G(t0*t0*s0) if s0>0 else -1;k=s0*s0*t0
    if t0<=0:break
    nn*=2;bb*=2
   purity=max(tfwin(a,b),oldwin(math.sqrt(P),P,P))
   if purity<=.5:break
   lim=min(lim,gap(purity,be));a=G(P);b=G(b*b*a) if a>0 else -1;n*=2;be*=2
 result=dict(g=rec['g'],status='BOUNDED_FLOAT_UNREVIEWED_NUMERATOR_CANDIDATE_ONLY',beta_grid=[2,30,.01],max_time_steps=7,max_canonical_steps=7,passes=passes,best=best,short_gap=short);out.append(result);print(result,flush=True)
(R.HERE/'candidate_numerator_path_scan.json').write_text(json.dumps(out,indent=2)+'\n')
