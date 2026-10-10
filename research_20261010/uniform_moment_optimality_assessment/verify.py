#!/usr/bin/env python3
"""Exact relaxed sharpness and explicit unit-count near-extremizers."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,hashlib,os,resource,time,sys
sys.set_int_max_str_digits(1000000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));t0=time.process_time();hashes={};B=10**30

def read(p):
 raw=p.read_bytes();hashes[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest();return raw

def row(x):return {'exact':str(x),'display':float(x)}
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def down(x):return F(x.numerator*B//x.denominator,B)
def sqrti(x):
 n=isqrt(x.numerator*B*B//x.denominator);lo=F(n,B);hi=F(n+1,B);assert lo*lo<=x<=hi*hi;return lo,hi
old=P.parent/'uniform_transfer_moment_assessment';mf=json.loads(read(old/'MANIFEST_SHA256.json'));raw=read(old/'results.json');assert hashlib.sha256(raw).hexdigest()==mf['results.json'];d=json.loads(raw)
moms={s:{int(j):tuple(F(v['exact']) for v in iv) for j,iv in dd['moment_intervals'].items()} for s,dd in d['hankel_caps'].items()};caps={s:F(v['x_cap']['exact']) for s,v in d['hankel_caps'].items()}
prop=json.loads(read(P/'unit_atom_proposals.json'));unit={s:list(zip(v['counts'],map(F,v['x_rational']))) for s,v in prop.items()}
# This tiny-eigenvalue integer block repairs C_2,C_3 positivity while changing m3 by1e-15.
unit['trivial'].append((10**15,F(1,10**10)))
radau={}; records={}
for s,h in caps.items():
 a,b,c=[sum(moms[s][j],F(0))/2 for j in (3,4,5)];t=(h*b-c)/(h*a-b);wh=(b-t*a)/(h-t);wt=a-wh
 assert 0<t<h and min(wt,wh)>0
 assert all(wh*h**j+wt*t**j==m for j,m in enumerate((a,b,c)))
 counts=(wh/h**3,wt/t**3);assert any(v.denominator!=1 for v in counts)
 radau[s]={'h':h,'t':t,'wh':wh,'wt':wt,'m':(a,b,c)}
 for count,x in unit[s]:assert isinstance(count,int) and count>=1 and 0<x<=h
 records[s]={'support_cap':row(h),'radau_node':row(t),'weighted_measure_masses':[row(wh),row(wt)],'effective_physical_counts':[row(v) for v in counts],'exact_center_moments':[row(v) for v in (a,b,c)],'unit_atoms':[{'count':n,'x':row(x)} for n,x in unit[s]]}

def unit_m(s,k):return sum(n*x**k for n,x in unit[s])
def radau_m(s,k):
 v=radau[s];return v['wh']*v['h']**(k-3)+v['wt']*v['t']**(k-3)
def raw_triplet(ms):
 i,o,n=ms;return {'I':i+2*o+3*n,'P':i+2*o-n,'C':i-o}
audit=json.loads(read(ROOT/'audit/independent/streamed_heat_audit.json'));trusted={a['certificate']:a['sha256'] for a in audit['independent_aggregate_intervals']}
checks=[]
for L in (6,8,10):
 relaxraw=raw_triplet([radau_m(s,L//2) for s in ('trivial','complex','vector')]);unitraw=raw_triplet([unit_m(s,L//2) for s in ('trivial','complex','vector')])
 for twist in ('I','P','C'):
  rel=f'heat_trace/results/A_L{L}_{twist}_full/certificate.json';cert=json.loads(read(ROOT/rel));assert hashes[rel]==trusted[rel]
  iv=[F(int(cert['interval'][b]['numerator']),int(cert['interval'][b]['denominator'])) for b in ('lower','upper')]
  for label,candidate in [('relaxed_center',relaxraw[twist]),('unit_count',unitraw[twist])]:
   assert iv[0]<candidate<iv[1]
   checks.append({'L':L,'seam':twist,'witness':label,'value':row(candidate),'distance_to_nearest_raw_endpoint':row(min(candidate-iv[0],iv[1]-candidate))})

def majorant(s,L):
 v=radau[s];h=v['h'];t=v['t'];k=L//2-3
 cc=(h**k-t**k-k*t**(k-1)*(h-t))/(h-t)**2;bb=k*t**(k-1)-2*cc*t;aa=t**k-k*t**k+cc*t*t
 coeff=(aa,bb,cc)
 center=sum(co*mv for co,mv in zip(coeff,v['m']));assert center==radau_m(s,L//2)
 outer=sum(co*moms[s][j][1 if co>=0 else 0] for co,j in zip(coeff,(3,4,5)))
 assert outer>=center and outer>=unit_m(s,L//2)
 return outer,center
bounds=[]
for L in range(10,122,2):
 vals=[majorant(s,L) for s in ('trivial','complex','vector')];outer=sum(mult*v[0] for mult,v in zip((1,2,3),vals));relaxed=sum(mult*v[1] for mult,v in zip((1,2,3),vals));integer=sum(mult*unit_m(s,L//2) for mult,s in zip((1,2,3),('trivial','complex','vector')))
 assert outer>=max(relaxed,integer)
 bounds.append({'L':L,'relaxation_feasible_lower':row(down(relaxed)),'rigorous_Hermite_upper':row(up(outer)),'unit_count_feasible_lower':row(down(integer)),'interval_uncertainty_gap_upper':row(up(outer-relaxed)),'maximum_possible_improvement_over_unit_witness':row(up(outer-integer)),'relative_unit_gap_upper':row(up((outer-integer)/outer))})
# Positive eigenvalues sqrt(x) yield positive I and full Z for all lengths.
# For C: L>=6, O_L<=O_6<1<I_L. For P: L>=8,N_L<=N_8<1<I_L.
assert unit['trivial'][0][1]>1
assert all(x<1 for s in ('complex','vector') for n,x in unit[s])
assert unit_m('complex',3)<1 and unit_m('vector',4)<1
finite=[]
for L in range(2,8):
 ivs=[]
 for s in ('trivial','complex','vector'):
  lo=hi=F(0)
  for count,x in unit[s]:
   if L%2:
    a,b=sqrti(x);lo+=count*x**(L//2)*a;hi+=count*x**(L//2)*b
   else:lo+=count*x**(L//2);hi=lo
  ivs.append((lo,hi))
 i,o,n=ivs;pl=i[0]+2*o[0]-n[1];cl=i[0]-o[1];assert min(pl,cl)>0
 finite.append({'L':L,'P_lower':row(pl),'C_lower':row(cl)})
out={'status':'PASS exact relaxed sharpness and integer-multiplicity feasible near-extremizers','scope':'Fixed beta0 nine raw moment intervals, support caps, A4 multiplicities and all-length positive seam traces. Not a physical Heisenberg realization or a cross-temperature counterexample.','sectors':records,'raw_interval_checks':checks,'long_trace_comparisons':bounds,'all_length_seam_positivity':{'finite_L2_through7':finite,'C_from6':'I_L>1>O_6>=O_L','P_from8':'I_L>1>N_8>=N_L; O_L>=0'},'resources':{'cpu_seconds':time.process_time()-t0,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps({'status':out['status'],'selected_bounds':[v for v in bounds if v['L'] in (24,26,48,50,52,96,100,104)],'resources':out['resources']},indent=2))
