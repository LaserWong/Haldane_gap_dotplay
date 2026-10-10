"""Producer exact replay; separate sealed-review exponent implementation."""
exec(open(__file__.replace('verify.py','common.py')).read())
from collections import defaultdict,Counter
import math
import numpy as np
from inertia_trace import inertia
C=p.C
A=load('review_scalar',HERE.parent/'chain_low_band_review/audit_certificate.py')
def main():
 start=time.monotonic();mom=json.loads((HERE/'expanded_moments.json').read_text());states=list(map(tuple,mom['basis']));n=len(states);assert n==195 and len(set(states))==n
 assert all(sum(C.EX[x] for x in s)<4 for s in states) and sum(any(x>=4 for x in s) for s in states)==20
 weights=[math.prod(C.W[x] for x in s) for s in states];assert list(map(str,weights))==mom['Gram_diagonal'];ids=dict(zip(states,range(n)))
 acts=[];rows=defaultdict(list)
 for j,s in enumerate(states):
  out=defaultdict(F)
  for right in range(4):
   left=(right-1)%4
   for x,y,c in C.K[s[left],s[right]]:
    ss=list(s);ss[left]=x;ss[right]=y;out[tuple(ss)]+=c
  out={ss:c for ss,c in out.items() if c};acts.append(out)
  for ss,c in out.items():rows[ss].append((j,c))
 K=[[weights[i]*acts[j].get(states[i],F(0)) for j in range(n)] for i in range(n)]
 J=[[F(0)]*n for _ in range(n)]
 for ss,row in rows.items():
  w=math.prod(C.W[x] for x in ss)
  for i,x in row:
   for j,y in row:J[i][j]+=w*x*y
 R=[r[:] for r in J]
 for k in range(n):
  ii=[i for i in range(n) if K[i][k]]
  for i in ii:
   for j in ii:R[i][j]-=K[i][k]*K[k][j]/weights[k]
 for name,mat in [('unit_K',K),('unit_J',J),('unit_residual_Gram',R)]:assert [[str(x) for x in r] for r in mat]==mom[name]
 assert len(rows)==mom['full_action_union'] and len(set(rows)-set(states))==mom['residual_union']
 mags=[sum(C.MAG[x] for x in s) for s in states];blocks=[[i for i,m in enumerate(mags) if m==z] for z in sorted(set(mags))];assert blocks==mom['magnetic_blocks']
 assert all(K[i][j]==R[i][j]==0 for i in range(n) for j in range(n) if mags[i]!=mags[j])
 rec=json.loads((HERE/'expanded_inputs.json').read_text())[0];assert rec['g']=='1/4';g=F(1,4);s=rec['small'];info=s['expanded_band'];C.DATA=ROOT/rec['small_folder'];ground=C.check_ground(s)
 lc=info['local_comparison'];C.local_psd(lc);alpha=1-2*F(lc['a']);B=4*F(lc['b']);cut=4*alpha-B;assert [alpha,B,cut]==list(map(F,[info['alpha'],info['B'],info['omitted_cutoff']])) and alpha>0
 bins=Counter({0:1})
 for _ in range(4):
  new=Counter()
  for e,c in bins.items():
   for f,m in [(0,1),(1,3),(3,5)]:new[e+f]+=c*m
  bins=new
 assert sorted(bins.items())==[tuple(x) for x in info['complete_reference_bins']]
 assert sum(bins.values())==6561 and sum(c for e,c in bins.items() if e<4)==195 and info['remaining_count']==6366
 count=0;inertias=[]
 for row in info['comparison_endpoints']:
  t=F(row['lower']);assert t<cut;neg=zero=0;bc=[]
  for ix in blocks:
   mat=[[(cut-t)*((F(sum(C.EX[x] for x in states[i]))-t)*weights[i]*(i==j)+g*K[i][j])-g*g*R[i][j] for j in ix] for i in ix]
   den=math.lcm(*(x.denominator for rr in mat for x in rr));nn,zz=inertia(np.array([[int(x*den) for x in rr] for rr in mat],dtype=object));neg+=nn;zero+=zz;bc.append([len(ix),nn,zz])
  assert neg==count==row['negative_inertia'] and zero==row['zero_inertia']==0 and bc==row['magnetic_block_counts'];count+=row['multiplicity'];inertias.append([str(t),neg,zero])
 assert count==195
 tw=json.loads((HERE/'triplet_witness.json').read_text());vv=[list(map(F,v)) for v in tw['vectors']];assert len(vv)==3
 def total_action(vec,op):
  out=[F(0)]*n
  for j,x in enumerate(vec):
   if not x:continue
   for site in range(4):
    for dest in range(9):
     c=C.OPS[0,op][dest][states[j][site]]+C.OPS[1,op][dest][states[j][site]]
     if c:
      ss=list(states[j]);ss[site]=dest;assert tuple(ss) in ids;out[ids[tuple(ss)]]+=x*c
  return out
 assert all(x==0 for x in total_action(vv[0],'+')) and all(x==0 for x in total_action(vv[2],'-'))
 assert total_action(vv[0],'-')==vv[1] and total_action(vv[1],'-')==vv[2] and total_action(vv[1],'+')==vv[0] and total_action(vv[2],'+')==vv[1]
 for vec,mag in zip(vv,[1,0,-1]):
  assert all(x==0 or mags[i]==mag for i,x in enumerate(vec));norm=sum(w*x*x for w,x in zip(weights,vec));assert norm==F(tw['metric_norm'])>0
  full=defaultdict(F)
  for j,x in enumerate(vec):
   if not x:continue
   full[states[j]]+=sum(C.EX[q] for q in states[j])*x
   for ss,c in acts[j].items():full[ss]+=g*x*c
  en=sum(weights[i]*x*full[states[i]] for i,x in enumerate(vec))/norm;assert en==F(tw['shifted_rayleigh'])
 assert F(tw['excitation_relative_to_ground_rayleigh'])==F(tw['shifted_rayleigh'])-8-F(s['exact_rayleigh'])
 matrix=json.loads((HERE.parent/'chain_filter_extension/M8_two_trial_moments.json').read_text());rho8=A.expectation(matrix,list(map(int,rec['large']['combination_integers'])),g);assert rho8==F(rec['large']['exact_rayleigh'])
 obschecks=[]
 for filename,d_exact,threshold in [('obstruction_g1d4.json',-8+F(info['comparison_endpoints'][1]['lower'])-F(s['exact_rayleigh']),F(5,8)),('denominator_obstruction_g1d4.json',F(tw['excitation_relative_to_ground_rayleigh']),F(17,25))]:
  ob=json.loads((HERE/filename).read_text());delta=rho8-2*F(s['exact_rayleigh']);dl=F(ob['delta_lower']);du=F(ob['triplet_excitation_upper']);assert 0<dl<=delta and du>=d_exact>0 and d_exact==F(ob['triplet_excitation_exact'])
  assert len(ob['intervals'])==1200;largest=F(0)
  for k,row in enumerate(ob['intervals']):
   lo,hi=F(k,100),F(k+1,100);assert [lo,hi]==list(map(F,row['beta']));L=A.expbox(-2*lo*dl)[1];q1=1+3*A.expbox(-hi*du)[0];q2=1+3*A.expbox(-2*hi*du)[0]
   ju=min(F(1),L/q1**4);cu=min(F(1),L/q2**2);a=max(F(0),A.G(ju));z=cu*cu*a;b=max(F(0),A.G(z)) if z>0 else F(0);P=a*a*b
   saved=F(row['joint_after_first_cycle_upper']);assert P<=saved<threshold;largest=max(largest,saved)
  assert largest==F(ob['maximum_postcycle_joint_upper'])
  tail=A.expbox(-48*dl)[1];assert tail<=F(ob['beta_ge12_second_argument_upper'])<F(1,2)
  if 'M8_span_rayleigh_lower' in ob:
   lam=2*F(s['exact_rayleigh'])+dl;assert lam==F(ob['M8_span_rayleigh_lower']);m=[[F(matrix['K0'][i][j])+g*F(int(matrix['K1_scaled'][i][j]),matrix['weak_denominator'])-lam*F(matrix['G'][i][j]) for j in range(2)] for i in range(2)];piv=[m[0][0],m[1][1]-m[0][1]*m[1][0]/m[0][0]];assert min(piv)>0 and piv==list(map(F,ob['M8_span_positive_pivots']))
  obschecks.append(dict(file=filename,intervals=1200,maximum_postcycle_joint_upper=str(largest),threshold=str(threshold)))
 out=dict(status='EXACT_PRODUCER_REPLAY_PASS_PENDING_INDEPENDENT_REVIEW',ground=ground,inertias=inertias,triplet_excitation=str(F(tw['excitation_relative_to_ground_rayleigh'])),obstructions=obschecks,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (HERE/'verification.json').write_text(json.dumps(out,indent=2));print('REPLAY PASS',out['seconds'],out['peak_rss_kib'],flush=True)
if __name__=='__main__':main()
