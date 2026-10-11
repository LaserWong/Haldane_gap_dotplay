import os,resource,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));sys.dont_write_bytecode=True
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,math,importlib.util,itertools,time
H=Path(__file__).resolve().parent;S=H/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();start=time.process_time()
spec=importlib.util.spec_from_file_location('accepted_point_review',S/'point_review/audit.py');Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q);R=Q.R;P=Q.P;ns=P.ns;OLD=Q.Q
poly=lambda c,g:sum(F(x)*g**i for i,x in enumerate(c))
def verify(name,seal,partial=False):
 p=S/name;assert sha(p/'MANIFEST_SHA256.json')==seal;mf=load(p/'MANIFEST_SHA256.json')
 if partial:
  for f in p.iterdir():
   if f.name!='MANIFEST_SHA256.json':assert sha(f)==mf[f.name]
 else:
  for f,h in mf.items():assert sha(p/f)==h

def review_cert(cert):
 lo,hi=map(F,cert['coupling_interval']);assert F(27,250)<=lo<hi<=F(433,4000);phys=cert['physical']
 M={16:load(OLD.S/'bilayer_split_H2_fixture_review/snapshot/producer/complete_H2_polynomial_4x4.json'),32:load(OLD.S/'bilayer_complete_split_H2_8x4_review/audit.json')};mom={}
 point=load(Q.S/'producer/result.json')['results'][0];assert F(point['g'])==F(433,4000)
 for N in (16,32):
  w=next(x for x in point['matrix_witnesses'] if x['N']==N);assert w['selected']=='pencil';c=w['pencil_optimized']['integer_coefficients'];mom[N]=OLD.moments(N,c,M[N],'pencil');m=mom[N];saved=next(x for x in load(S/'point_review/audit.json')['actual_point']['fixed_vector_moment_polynomials'] if x['N']==N and x['tag']=='pencil')
  for k in ('rho','second','variance'):assert m[k]==list(map(F,saved[k]))
 oldnum=point['numerator_witness'];c=list(map(F,oldnum['integer_coefficients']));n=(len(c)-1)//3;k=2*n+1;embedded=c[:k]+c[k:]+c[k:];geo=load(R.S/'third_moment_review/results/geometry_8x8.json');_,num,_=R.split_rayleigh((8,8),geo,embedded,lo);assert num==list(map(F,oldnum['rayleigh_coefficients']))==list(map(F,phys['numerator_coefficients']))
 base=next(x['data'] for x in load(R.DATA/'bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100));patches=[];reports=[]
 for ix,N in enumerate((16,32)):
  m=mom[N];rho=m['rho'];var=m['variance'];mean=[poly(rho,g) for g in (lo,hi)];variance=[poly(var,g) for g in (lo,hi)];refs=[[P.reference(N,g,q)-poly(rho,g) for g in (lo,hi)] for q in range(1,N+1)];mins=[min(v) for v in refs];assert min(mins[:2])>0;V=max(variance);width=V/mins[1];s=phys['patches'][ix]
  for key,v in [('mean_coefficients',rho),('variance_coefficients',var),('mean_endpoint_values',mean),('variance_endpoint_values',variance),('tail',mins[1:])]:assert list(map(F,s[key]))==v,key
  assert [[F(x) for x in row] for row in s['reference_relative_endpoint_lowers']]==refs
  for key,v in [('ground_identification_margin',mins[0]),('even_Temple_denominator',mins[1]),('uniform_ground_width',width)]:assert F(s[key])==v
  shape=(4,4) if N==16 else(8,4);arr=ns['fixed_arrays'](*shape,F(1,10));odd=[];margins=[]
  assert len(s['odd_details'])==N and [x['momentum'] for x in s['odd_details']]==[list(k) for k in itertools.product(range(shape[0]),range(shape[1]))]
  for saved,old in zip(s['odd_details'],base['denominator_patches'][ix]['odd_band']['modes']):
   kx,ky=saved['momentum'];mo={k:ns['symbol'](a,*shape,kx,ky) for k,a in arr.items()};gram=mo['G'];assert ns['sign'](gram)>0 and gram==tuple(map(F,saved['gram_symbol']))
   theta=[ns['qd'](mo[k],gram) for k in ('Q','V')];second=[ns['qd'](mo[k],gram) for k in ('Q2','C','D')];vv=[ns['qs'](second[0],ns['qm'](theta[0],theta[0])),ns['qs'](second[1],ns['qm'](ns['q'](2),ns['qm'](theta[0],theta[1]))),ns['qs'](second[2],ns['qm'](theta[1],theta[1]))];disc=ns['qs'](ns['qm'](ns['q'](4),ns['qm'](vv[0],vv[2])),ns['qm'](vv[1],vv[1]));assert ns['sign'](vv[0])>=0 and ns['sign'](vv[2])>=0 and ns['sign'](disc)>=0
   assert theta==ns['qlist'](old['theta_coefficients']) and vv==ns['qlist'](old['residual_squared_coefficients'])
   for k,v in [('c0',vv[0]),('c2',vv[2]),('four_c0_c2_minus_c1sq',disc)]:assert tuple(map(F,saved['variance_form'][k]))==v
   encl=[Q.qbounds(ns['qpoly'](theta,g)) for g in (lo,hi)];vup=[Q.qbounds(ns['qpoly'](vv,g))[1] for g in (lo,hi)];denends=[P.reference(N,g,2)-e[1] for g,e in zip((lo,hi),encl)];den=min(denends);assert den>0;rel=min(e[0]-r for e,r in zip(encl,mean));ell=max(mins[0],rel-max(vup)/den);odd.append(ell);margins.append(den)
   assert [list(map(F,e)) for e in saved['mean_endpoint_enclosures']]==[list(e) for e in encl] and list(map(F,saved['variance_endpoint_upper']))==vup and list(map(F,saved['cutoff_margins']))==denends
   for k,v in [('uniform_Temple_denominator',den),('theta_minus_pivot_lower',rel),('uniform_odd_lower',ell)]:assert F(saved[k])==v
  assert odd==list(map(F,s['odd'])) and sum(math.comb(3*N+q-1,q) for q in range(N+1))>=4**N
  patches.append(dict(N=N,width=width,odd=odd,tail=mins[1:]));reports.append(dict(N=N,ground_min_margin=str(mins[0]),even_min_margin=str(mins[1]),ground_variance_max=str(V),ground_width=str(width),odd_min_margin=str(min(margins)),odd_mode_count=N,endpoint_checks=2*N))
 energies={}
 for k,w in [('J1',(8,0,-2)),('J2',(16,0,-4)),('C0',(0,4,-2))]:
  co=[sum(w[j]*rr[i] for j,rr in enumerate([mom[16]['rho'],mom[32]['rho'],num])) for i in range(2)];ends=[poly(co,g) for g in (lo,hi)];e=min(ends);saved=phys['energy_combination_details'][k];assert list(map(F,saved['coefficients']))==co and list(map(F,saved['endpoint_values']))==ends and F(saved['uniform_lower'])==e==F(phys['energy_combinations'][k]);energies[k]=e
 beta=F(cert['beta_initial']);assert beta in (F(193,20),F(19,2));totals=[]
 for ii,(ix,mult) in enumerate(((0,1),(0,2),(1,2))):
  p=patches[ix];b=beta*mult;N=p['N'];parts=[R.ex(b*p['width'])[1],3*sum(R.ex(-b*x)[1] for x in p['odd']),sum(math.comb(3*N+q-1,q)*R.ex(-b*x)[1] for q,x in enumerate(p['tail'],2))];saved=cert['trace_components'][ii];assert saved['N']==N and F(saved['beta'])==b
  for k,v in zip(('ground','odd','tail'),parts):assert F(saved[k])>=v
  assert F(saved['total'])==sum(F(saved[k]) for k in ('ground','odd','tail'))>=sum(parts);totals.append(sum(parts))
 rr={k:R.floor(R.ex(beta*energies[k])[0]/totals[i]**power) for k,i,power in [('J1',0,8),('J2',1,8),('C0',2,2)]};assert rr=={k:F(v) for k,v in cert['ratios'].items()}
 a=R.G(rr['J1']);b=R.G(rr['J2']*a);c=R.G(rr['C0']**4*a*a*b);abc=[a,b,c];gaps=[];states=[]
 for j,row in enumerate(cert['states']):
  assert min(abc)>0 and abc==list(map(F,row['raw'])) and row['n']==8*2**j and F(row['beta'])==2*beta*2**j;a,b,c=abc;can=[R.floor(a*R.root(b)),R.floor(a*a*b*R.root(c)),R.floor(a**4*b*b*c)];u=max(1-x for x in can);assert can==list(map(F,row['canonical'])) and u==F(row['common_defect'])
  if 'asymptotic_gap' in row:
   assert j==len(cert['states'])-1 and 0<u<=F(1,500);gap=F(row['asymptotic_gap']);assert R.ex(F(row['beta'])*gap)[1]*32*u<1
  else:
   assert min(b,c)>F(1,2);s=R.floor(b*b*R.root(2*c-1));assert s>F(1,2);v=R.floor(a**4*(2*b-1)*R.root(2*s-1));assert v==F(row['thermal_lower'])>F(1,2);gap=F(row['finite_window_gap']);assert R.ex(F(row['beta'])*gap)[1]*(1-v)<v
  assert gap>0;gaps.append(gap);states.append(dict(n=row['n'],beta=row['beta'],gap=str(gap),terminal='asymptotic_gap' in row))
  if j<len(cert['states'])-1:
   aa=R.G(a**4*b*b*c);bb=R.G(aa*c*c);cc=R.G(c**4*aa*aa*bb);abc=[aa,bb,cc]
 short=load(R.S/'bilayer_short_bridge_refinement_review/ACCEPTANCE.json')['continuous_positive_bounds'][0];assert F(short['coupling_interval'][0])<=lo<hi<=F(short['coupling_interval'][1]);gap=min(F(short['gap_lower']),*gaps);assert gap==F(cert['all_integer_L_ge2_gap'])
 return dict(interval=[str(lo),str(hi)],gap=str(gap),physical_uniform_checks=reports,states=states)

def main():
 verify('point_review','e9b6f4f3451a71a44b9644f02c759512550b21d13325f2a7cc2ef4484f2501e4');verify('producer','9e577cf4f9a225c0e51e889450f6cbcb429b0eeedc773eba76402e97cb07cd1b');verify('prior_interval','61283a4637b0906e2c059e25023933003ba9a4815771ec0b52a680a0bb713f0b',True)
 result=load(S/'producer/result.json');assert result['coupling_interval']==['27/250','433/4000'] and len(result['certificates'])==2
 rows=[review_cert(c) for c in result['certificates']]
 assert rows[0]['interval'][0]=='27/250' and rows[-1]['interval'][1]=='433/4000' and all(a['interval'][1]==b['interval'][0] for a,b in zip(rows,rows[1:]))
 gap=min(F(x['gap']) for x in rows);assert gap==F(result['uniform_gap'])==F(293202989,500000000000)
 old=load(S/'prior_interval/ACCEPTANCE.json');assert old['combined_interval']==['0','27/250'] and old['all_integer_square_sides_from']==2 and old['unique_full_Hilbert_ground'];combined=min(gap,F(old['combined_uniform_gap_lower']));assert combined==F(293202989,500000000000) and F(old['combined_uniform_gap_lower'])==F(4499695659,10**12)
 join=load(S/'producer/proposed_join.json');assert join['combined_interval']==['0','433/4000'] and F(join['combined_uniform_gap_lower'])==combined and join['combined_closed_pieces']==88
 preserved=join['preserved_stronger_nested_certificate'];assert preserved['review_seal']==join['previous_review_seal']==sha(S/'prior_interval/MANIFEST_SHA256.json')
 assert preserved['coupling_interval']==old['combined_interval'] and F(preserved['uniform_gap'])==F(old['combined_uniform_gap_lower']) and preserved['closed_pieces']==old['combined_closed_pieces']==86
 out=dict(preserved_stronger_nested_certificate=preserved,status='PASS_TWO_CLOSED_PIECES_WITH_STRONGER_NESTED_COVER',extension_interval=['27/250','433/4000'],extension_uniform_gap=str(gap),combined_interval=['0','433/4000'],combined_uniform_gap=str(combined),combined_closed_pieces=old['combined_closed_pieces']+len(rows),all_integer_square_L_ge=2,unique_full_Hilbert_ground=True,no_gap_monotonicity_assumption=True,new_physical_support=False,certificates=rows,superseded_initial_outputs_not_used=True,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['cpu_seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
