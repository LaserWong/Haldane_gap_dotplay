#!/usr/bin/env python3
"""Independent exact audit. Reads producer; writes only this review directory."""
from fractions import Fraction as Q
from pathlib import Path
import os,resource,json,hashlib,time,itertools
P=Path(__file__).resolve().parent; R=P.parents[1]; A=P.with_name('uniform_transfer_moment_assessment')
aff=os.sched_getaffinity(0);cpu=5 if 5 in aff else min(aff);os.sched_setaffinity(0,{cpu})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(180,180));t0=time.process_time()
inputs={}
def read(p):
 p=Path(p);b=p.read_bytes();inputs[str(p.relative_to(R))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(read(p))
def ceilq(q,scale):return Q(-((-q.numerator*scale)//q.denominator),scale)
def floorq(q,scale):return Q((q.numerator*scale)//q.denominator,scale)
def root(q,k,scale=10**36):
 assert q>=0 and k>0
 if not q:return Q(0)
 # Integer comparison, without rational exponentiation inside the search.
 n=q.numerator*scale**k;d=q.denominator;lo=0;hi=scale
 while hi**k*d<n:hi*=2
 while hi-lo>1:
  mid=(hi+lo)//2
  if mid**k*d<n:lo=mid
  else:hi=mid
 assert lo**k*d<n<=hi**k*d
 return Q(hi,scale)
def exp_bounds(x):
 # Independently chosen degree and grid; positive series and reciprocal.
 inverse=x<0;x=abs(x);squarings=0
 while x>Q(1,8):x/=2;squarings+=1
 term=Q(1);total=term
 for j in range(1,65):term*=x/j;total+=term
 remainder=(term*x/65)/(1-x/66)
 lo=floorq(total,10**45);hi=ceilq(total+remainder,10**45)
 for j in range(squarings):lo=floorq(lo*lo,10**45);hi=ceilq(hi*hi,10**45)
 return (1/hi,1/lo) if inverse else (lo,hi)
def exact(row):return Q(row['exact'])
def iv(co,vals):
 return tuple(sum(c*v[(side if c>=0 else 1-side)] for c,v in zip(co,vals)) for side in (0,1))
manifest=js(A/'MANIFEST_SHA256.json')
for f,h in manifest.items():assert hashlib.sha256(read(A/f)).hexdigest()==h
for f,h in js(A/'INPUT_SHA256.json').items():assert hashlib.sha256(read(R/f)).hexdigest()==h

for doc in ('AGENTS.md','README.md','audit/APPENDIX_A_BRIDGE.md','heat_trace/PROOF.md','research_20261010/nonperturbative_mps_review/REVIEW.md'):
 read(R/doc)
producer=js(A/'results.json');audit=js(R/'audit/independent/streamed_heat_audit.json')
assert audit['all_9_appendix_A_physical_inputs_verified'];trusted={v['certificate']:v['sha256'] for v in audit['independent_aggregate_intervals']}
coeff={'trivial':(Q(1,12),Q(1,4),Q(2,3)),'complex':(Q(1,12),Q(1,4),Q(-1,3)),'vector':(Q(1,4),Q(-1,4),Q(0))};mult={'trivial':1,'complex':2,'vector':3}
m={s:{} for s in coeff}
for L in (6,8,10):
 vals=[]
 for twist,theta in [('I','0'),('P','pi'),('C','2*pi/3')]:
  path=f'heat_trace/results/A_L{L}_{twist}_full/certificate.json';d=js(R/path)
  assert inputs[path]==trusted[path]
  assert (d['L'],d['twist'],d['theta'],d['beta'],d['energy_shift_a'],d['physical_dimension'])==(L,twist,theta,'21/2','700741/500000',3**L)
  vals.append(tuple(Q(int(d['interval'][side]['numerator']),int(d['interval'][side]['denominator'])) for side in ('lower','upper')))
 for s,co in coeff.items():
  low,high=iv(co,vals);m[s][L//2]=(floorq(low,10**12),ceilq(high,10**12))
  assert list(m[s][L//2])==[exact(v) for v in producer['hankel_caps'][s]['moment_intervals'][str(L//2)]]
# Verify character inversion as a full 3x3 exact matrix, not merely total multiplicity.
forward=((1,2,3),(1,2,-1),(1,-1,0))
for i,co in enumerate(coeff.values()):
 for j in range(3):assert sum(co[k]*forward[k][j] for k in range(3))==int(i==j)
caps={};certificate={}
for s,v in m.items():
 a,b,c=v[3][1],v[4][0],v[5][1]
 poly=lambda x:a*c-b*b-c*x**3+2*b*x**4-a*x**5
 derivative=lambda x:-3*c+8*b*x-5*a*x*x
 assert min(a,b,c)>0 and c**4<b**5
 # Find a rigorous bracket on the same 1e-10 lattice without producer bisection.
 scale=10**10;low=int(ceilq(4*b/(5*a),scale)*scale);high=int(root(c,5,scale)*scale)
 assert poly(Q(low,scale))>0 and poly(Q(high,scale))<0
 while high-low>1:
  mid=(low+high)//2
  if poly(Q(mid,scale))<0:high=mid
  else:low=mid
 cap=Q(high,scale);caps[s]=cap
 assert cap==exact(producer['hankel_caps'][s]['x_cap'])
 assert poly(cap)<0 and derivative(cap)<0 and cap>=4*b/(5*a)
 assert root(cap,2)<=exact(producer['hankel_caps'][s]['lambda_cap_upper'])
 certificate[s]={'x_cap':str(cap),'F_cap':str(poly(cap)),'derivative_quadratic':str(derivative(cap)),'domain_margin_b5_minus_c4':str(b**5-c**4)}
def bound(s,L):
 assert L>=10 and L%2==0
 cap=caps[s];M=m[s][5][1];h=cap**5;q=int(M/h);r=M-q*h
 assert 0<=r<h
 return q*cap**(L//2)+root(r**(L//2),5),q
bounds={};trace={}
for L in range(10,122,2):
 total=Q(0)
 for s in coeff:
  val,q=bound(s,L);p=producer['all_even_trace_bounds'][str(L)]['sectors'][s]
  assert val<=exact(p['upper']) and q==p['packed_full_atoms'];total+=mult[s]*val
 trace[L]=total
 assert total<=exact(producer['all_even_trace_bounds'][str(L)]['Z_upper'])
 bounds[L]=str(total)
for L,display in [(24,'1.238492320537'),(48,'1.131484383792')]:assert trace[L]<=exact(producer['all_even_trace_bounds'][str(L)]['Z_upper'])<=Q(display)
def integers(path):return {k:int(v) for line in read(path).decode().splitlines() if '=' in line for k,v in [line.split('=',1)]}
g=integers(R/'research_20261010/mps_excited_seed_witnesses/ground_lengths.out');ph=js(R/'research_20261010/mps_excited_seed_witnesses/PHYSICAL_MANIFEST_SHA256.json')
assert inputs['research_20261010/mps_excited_seed_witnesses/ground_lengths.out']==ph['files']['ground_lengths.out']
rays={int(k[3:]):Q(v,g['N0_'+k[3:]]) for k,v in g.items() if k.startswith('H0_')}
old=integers(R/'audit/mps/contraction.out')
for L in (72,120):rays[L]=L*Q(old['U'+str(L)],old['V'+str(L)])
G=lambda z:1-(1-z)**2/(2*z*z)
scan=[]
for p in producer['fixed_D26_cooling_scan']:
 L=p['numerator_length'];n=L//2;Rshift=rays[L]+Q(700741,500000)*L;assert Rshift==exact(p['R_shifted'])
 # Preserve the producer's denominator recipe exactly while independently enclosing exp.
 U=exact(producer['all_even_trace_bounds'][str(n)]['Z_upper']);elo,ehi=exp_bounds(-21*Rshift);jl,jh=elo/U**4,ehi/U**4
 assert exact(p['J_lower_C_lower'])<=jl<=jh<=exact(p['J_C_recipe_upper'])
 assert 0<jl<=jh<1
 assert exact(p['U_beta'])==U and exact(p['U_2beta_by_cooling'])==U*U
 assert exact(p['first_G'])==G(exact(p['J_lower_C_lower']))
 assert exact(p['first_G_recipe_upper'])==G(exact(p['J_C_recipe_upper']))
 if 'second_G' in p:
  z=exact(p['J_lower_C_lower'])**2*exact(p['first_G'])
  assert exact(p['second_argument'])==z and exact(p['second_G'])==G(z)
 if G(jh)<0:failure='first G'
 else:
  assert 0<G(jl)<=G(jh)<1 and G(jh*jh*G(jh))<0;failure='second G'
 if n==24:assert G(jh)<Q(2,5) and G(Q(2,5))==Q(-1,8)
 scan.append({'n':n,'J_interval':[str(jl),str(jh)],'J_display':float(jl),'failure':failure,'first_G_upper_display':float(G(jh))})
assert [p['n'] for p in scan]==[10,12,14,16,20,24,36,60]
# Adversarial checks and constructive examples.
tests=[]
def passed(name):tests.append(name)
# Finite repeated/signed spectra: square variable preserves all even moments, not odd.
lambdas=[Q(-3,4),Q(-3,4),Q(1,2),Q(-1,3)];xs=[x*x for x in lambdas]
for k in (6,8,10,24,48):assert sum(x**k for x in lambdas)==sum(y**(k//2) for y in xs)
assert sum(lambdas)!=sum(abs(x) for x in lambdas);passed('signed spectrum requires even exponents')
for i,x in enumerate(xs):
 residual=[sum(y**j for k,y in enumerate(xs) if k!=i) for j in (3,4,5)]
 assert residual[0]*residual[2]>=residual[1]**2
passed('remove one occurrence of a repeated eigenvalue')
# Infinite unit-atom spectrum x_i=2^-i: moments are exactly 1/(2^j-1).
for i in (1,2,13):
 x=Q(1,2**i);r=[Q(1,2**j-1)-x**j for j in (3,4,5)]
 assert all(z>=0 for z in r) and r[0]*r[2]>=r[1]**2
passed('infinite-rank geometric unit atoms obey residual PSD')
# Unit atom is essential: a weight 1/2 at x=1 has all moments 1/2;
# subtracting coefficient one spuriously gives negative residuals.
assert Q(1,2)-1<0;passed('arbitrary positive weights cannot replace unit atom multiplicities')
# Wrong square of negative lower endpoint rejects a true single-atom spectrum.
x=Q(1);a=c=Q(1);b=Q(1,2)
assert (a-x**3)*(c-x**5)>=max(Q(0),b-x**4)**2
assert not (a-x**3)*(c-x**5)>=(b-x**4)**2
passed('negative lower residual must be clamped before squaring')
# A downward m3 replacement can falsely reject the valid atoms 1 and 1/2.
a=Q(1)+Q(1,8);b=Q(1)+Q(1,16);c=Q(1)+Q(1,32)
assert (a-1)*(c-1)==(b-1)**2
assert (a-Q(1,100)-1)*(c-1)<(b-1)**2
passed('using lower m3 endpoint is an invalid exclusion')
# Interval corners independently exhaust coefficient-sign bounds.
boxes=[(Q(1),Q(2)),(Q(3),Q(5)),(Q(7),Q(11))]
for co in coeff.values():
 lo,hi=iv(co,boxes);values=[sum(c*z for c,z in zip(co,corner)) for corner in itertools.product(*boxes)]
 assert (lo,hi)==(min(values),max(values))
passed('negative character coefficients reverse interval endpoints')
# Exhaustive rational finite packing checks; integer power comparisons eliminate roots.
for atoms in itertools.product([Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)],repeat=4):
 M=sum(atoms);h=Q(1);q=int(M);r=M-q
 for k in (1,2,3,7):assert sum(x**k for x in atoms)<=q+r**k
passed('625 finite atom sets obey convex mass packing')
for value in (Q(0),Q(1,7),Q(1),Q(19,3)):
 for k in (2,5):assert root(value,k)**k>=value
passed('directed roots include zero and values greater than one')
# Old baseline evaluated at requested lengths with directed fractional powers.
oldcaps={'trivial':Q('1.00245')**2,'vector':Q('0.88643')**2};oldM={'trivial':Q('1.042655'),'complex':Q('0.040041'),'vector':Q('0.401625')}
oldbounds={}
for s,u,v in [('trivial',Q(-2),Q(10)),('vector',Q(-25),Q(100))]:
 cap=oldcaps[s]
 filtered_upper=u*u*m[s][3][1]+2*u*v*m[s][4][0]+v*v*m[s][5][1]
 assert cap**3*(u+v*cap)**2>filtered_upper
 # d/dx[x^3(u+vx)^2]=x^2(u+vx)(3u+5vx)>0 beyond cap.
 assert u+v*cap>0 and 3*u+5*v*cap>0
passed('original fixed square filters remain certified')
for L in (24,48):
 total=2*root(oldM['complex']**(L//2),5)
 for s in ('trivial','vector'):
  cap=oldcaps[s];h=cap**5;M=oldM[s];q=int(M/h)
  total+=mult[s]*(q*cap**(L//2)+root((M-q*h)**(L//2),5))
 assert total>trace[L]
 currentM_oldcap=2*root(m['complex'][5][1]**(L//2),5)
 for s in ('trivial','vector'):
  cap=oldcaps[s];h=cap**5;M=m[s][5][1];q=int(M/h)
  currentM_oldcap+=mult[s]*(q*cap**(L//2)+root((M-q*h)**(L//2),5))
 assert currentM_oldcap>trace[L]
 oldbounds[L]={'old_outward_display':str(ceilq(total,10**12)),'old_caps_current_moments_outward_display':str(ceilq(currentM_oldcap,10**12)),'new_outward_display':str(ceilq(trace[L],10**12))}
output={'verdict':'PASS, scoped to inherited physical/transfer premises and stated fixed recipe','producer_manifest_sha256':hashlib.sha256((A/'MANIFEST_SHA256.json').read_bytes()).hexdigest(),'verified_producer_manifest_files':len(manifest),'caps':certificate,'trace_bounds':bounds,'scan':scan,'old_baseline_comparison':oldbounds,'adversarial_tests':tests,'resources':{'cpu':cpu,'cpu_seconds':time.process_time()-t0,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'independent_results.json').write_text(json.dumps(output,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
print(json.dumps({k:output[k] for k in ('verdict','verified_producer_manifest_files','scan','old_baseline_comparison','adversarial_tests','resources')},indent=2))
