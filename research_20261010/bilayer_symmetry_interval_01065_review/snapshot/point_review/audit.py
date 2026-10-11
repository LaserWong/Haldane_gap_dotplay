import os,resource,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,itertools,math,importlib.util,time
H=Path(__file__).resolve().parent;S=H/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();start=time.process_time()
spec=importlib.util.spec_from_file_location('previous_point_review',S/'previous_point_review/audit.py');Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q);R=Q.R;P=Q.P;qbounds=Q.qbounds;poly=Q.poly

def verify(name,seal):
 p=S/name;assert sha(p/'MANIFEST_SHA256.json')==seal
 for f,h in load(p/'MANIFEST_SHA256.json').items():assert sha(p/f)==h

def main():
 verify('previous_point_review','3cc265100d18353585289f677e3ba79a1bb79b6ec60ac43c0fcd7046cc113d68');verify('producer','c88289ad94b4d1370f1e6797488f794f9c0dc6e6a41c0bad3fefb68f007ee387')
 P.verify();prod=load(S/'producer/result.json');assert len(prod['results'])==1;row=prod['results'][0];cert=row['certificate'];assert cert==load(S/'producer/candidate_g01065.json');g=F(cert['g']);assert g==F(213,2000);phys=cert['physical'];assert row['physical']==phys
 mats={16:load(Q.S/'bilayer_split_H2_fixture_review/snapshot/producer/complete_H2_polynomial_4x4.json'),32:load(Q.S/'bilayer_complete_split_H2_8x4_review/audit.json')};choices={};uppers={};upperproof=[];strictproof=[]
 for N in (16,32):
  w=next(x for x in row['matrix_witnesses'] if x['N']==N);M=mats[N];assert w['dimension']==len(M['gram'])==(21 if N==16 else 57) and F(w['g'])==g
  choices[N]=[];lower=[]
  for kind in ('energy','pencil'):
   ww=w[kind+'_optimized'];c=ww['integer_coefficients'];assert all(type(x)is int for x in c) and len(c)==w['dimension']
   m=Q.moments(N,c,M,kind);rho=poly(m['rho'],g);second=poly(m['second'],g);var=poly(m['variance'],g);r1=P.reference(N,g,1);a=P.reference(N,g,2);assert var>=0 and rho<r1<a
   lo=rho-var/(a-rho);ell=F(ww['strict_endpoint']);witness=second-(a+ell)*rho+a*ell;assert ell<lo<a and witness<0
   for key,val in [('norm',m['norm']),('rho',rho),('second_moment',second),('variance',var),('r1',r1),('r2',a),('ground_lower',lo),('negative_pencil',witness)]:assert F(ww[key])==val
   for key,val in [('rayleigh_coefficients',m['rho']),('full_second_moment_coefficients',m['second']),('full_variance_coefficients',m['variance'])]:assert list(map(F,ww[key]))==val
   choices[N].append(m);lower.append(lo);strictproof.append(dict(N=N,kind=kind,strict_endpoint=str(ell),negative_pencil=str(witness),ground_lower=str(lo)))
  assert w['selected']==('energy' if lower[0]>=lower[1] else 'pencil') and F(w['exact_lower_gain_over_energy'])==lower[1]-lower[0]
  uppers[N]=poly(choices[N][0]['rho'],g)
 num=row['numerator_witness'];c=list(map(F,num['integer_coefficients']));assert num['dimension']==len(c)==43 and num['retained_states']==1 and int(num['full_dimension'])==4**64 and all(x.denominator==1 for x in c)
 n=(len(c)-1)//3;k=2*n+1;embedded=c[:k]+c[k:]+c[k:];geo=load(R.S/'third_moment_review/results/geometry_8x8.json');norm,co,numerator=R.split_rayleigh((8,8),geo,embedded,g)
 assert norm==F(num['norm']) and co==list(map(F,num['rayleigh_coefficients'])) and numerator==F(num['rayleigh'])==F(phys['numerator_rayleigh'])
 upperproof.append(dict(shape=[8,8],dimension=43,norm=str(norm),rayleigh=str(numerator),coefficients=list(map(str,co))))
 d=next(x['data'] for x in load(R.DATA/'bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100));ns=P.ns;patches=[];reports=[]
 for ix,N in enumerate((16,32)):
  a=P.reference(N,g,2);r1=P.reference(N,g,1);cands=[]
  for m in choices[N]:
   rho=poly(m['rho'],g);var=poly(m['variance'],g);assert var>=0 and rho<r1<a;cands.append((rho-var/(a-rho),rho,var,m))
  lower,rho,var,m=max(cands,key=lambda x:x[0]);pivot=uppers[N];saved=phys['patches'][ix]
  for key,val in [('r1',r1),('r2',a),('rho',rho),('variance',var),('ground_lower',lower),('pivot',pivot),('ground_width',pivot-lower),('global_ground_margin',r1-rho)]:assert F(saved[key])==val,key
  assert saved['ground_selection']==m['tag'] and lower<pivot<r1
  shape=(4,4) if N==16 else(8,4);arr=ns['fixed_arrays'](*shape,F(1,10));odd=[];margins=[]
  for mode,source in zip(saved['odd_details'],d['denominator_patches'][ix]['odd_band']['modes']):
   kx,ky=mode['momentum'];mo={k:ns['symbol'](v,*shape,kx,ky) for k,v in arr.items()};gg=mo['G'];assert ns['sign'](gg)>0 and gg==tuple(map(F,mode['gram_symbol']))
   theta=[ns['qd'](mo[k],gg) for k in ('Q','V')];second=[ns['qd'](mo[k],gg) for k in ('Q2','C','D')];variance=[ns['qs'](second[0],ns['qm'](theta[0],theta[0])),ns['qs'](second[1],ns['qm'](ns['q'](2),ns['qm'](theta[0],theta[1]))),ns['qs'](second[2],ns['qm'](theta[1],theta[1]))]
   assert theta==ns['qlist'](source['theta_coefficients']) and variance==ns['qlist'](source['residual_squared_coefficients']);th=ns['qpoly'](theta,g);vv=ns['qpoly'](variance,g);assert ns['sign'](vv)>=0 and th==tuple(map(F,mode['theta'])) and vv==tuple(map(F,mode['variance']))
   lo,hi=qbounds(th);vlo,vhi=qbounds(vv);assert hi<a;ell=max(r1,lo-max(F(0),vhi)/(a-hi));assert ell==F(mode['lower']) and a-hi==F(mode['cutoff_margin']);margins.append(a-hi);odd.append(ell-pivot)
  assert len(odd)==N and len(set(tuple(z['momentum']) for z in saved['odd_details']))==N and min(margins)==F(saved['odd_min_cutoff_margin'])
  tail=[P.reference(N,g,q)-pivot for q in range(2,N+1)];assert odd==list(map(F,saved['odd'])) and tail==list(map(F,saved['tail']));assert sum(math.comb(3*N+q-1,q) for q in range(N+1))>=4**N
  patches.append(dict(N=N,pivot=pivot,width=pivot-lower,odd=odd,tail=tail));reports.append(dict(N=N,chosen=m['tag'],ground_lower=str(lower),variance=str(var),global_margin=str(r1-rho),odd_min_margin=str(min(margins)),retained=1+3*N))
 en={'J1':8*patches[0]['pivot']-2*numerator,'J2':16*patches[0]['pivot']-4*numerator,'C0':4*patches[1]['pivot']-2*numerator};assert en=={k:F(v) for k,v in phys['energy_combinations'].items()};beta=F(cert['beta_initial']);totals=[]
 for i,mult in ((0,1),(0,2),(1,2)):
  p=patches[i];b=beta*mult;N=p['N'];total=R.ex(b*p['width'])[1]+3*sum(R.ex(-b*x)[1] for x in p['odd'])+sum(math.comb(3*N+q-1,q)*R.ex(-b*x)[1] for q,x in enumerate(p['tail'],2));totals.append(total)
 rr={k:R.floor(R.ex(beta*en[k])[0]/totals[i]**power) for k,i,power in [('J1',0,8),('J2',1,8),('C0',2,2)]};assert rr=={k:F(v) for k,v in cert['ratios'].items()}
 aa=R.G(rr['J1']);bb=R.G(rr['J2']*aa);cc=R.G(rr['C0']**4*aa*aa*bb);abc=[aa,bb,cc];gaps=[];states=[]
 for j,row in enumerate(cert['states']):
  assert min(abc)>0 and abc==list(map(F,row['raw'])) and row['n']==8*2**j and F(row['beta'])==2*beta*2**j;a,b,c=abc;can=[R.floor(a*R.root(b)),R.floor(a*a*b*R.root(c)),R.floor(a**4*b*b*c)];u=max(1-x for x in can);assert can==list(map(F,row['canonical'])) and u==F(row['common_defect'])
  if 'asymptotic_gap' in row:
   assert j==len(cert['states'])-1 and 0<u<=F(1,500);gap=F(row['asymptotic_gap']);assert R.ex(F(row['beta'])*gap)[1]*32*u<1
  else:
   assert min(b,c)>F(1,2);s=R.floor(b*b*R.root(2*c-1));assert s>F(1,2);v=R.floor(a**4*(2*b-1)*R.root(2*s-1));assert v==F(row['thermal_lower'])>F(1,2);gap=F(row['finite_window_gap']);assert R.ex(F(row['beta'])*gap)[1]*(1-v)<v
  assert gap>0;gaps.append(gap);states.append(dict(n=row['n'],beta=row['beta'],gap=str(gap),terminal='asymptotic_gap' in row))
  if j<len(cert['states'])-1:
   aa=R.G(a**4*b*b*c);bb=R.G(aa*c*c);cc=R.G(c**4*aa*aa*bb);abc=[aa,bb,cc]
 short=load(R.S/'bilayer_short_bridge_refinement_review/ACCEPTANCE.json')['continuous_positive_bounds'][0];assert F(short['coupling_interval'][0])<=g<=F(short['coupling_interval'][1]);final=min(F(short['gap_lower']),*gaps);assert final==F(cert['all_integer_L_ge2_gap'])==F(5362952719,250000000000)
 moment_report=[dict(tag=m['tag'],N=m['N'],norm=str(m['norm']),rho=list(map(str,m['rho'])),second=list(map(str,m['second'])),variance=list(map(str,m['variance']))) for vv in choices.values() for m in vv]
 out=dict(exact_new_vector_pencils=strictproof,fixed_vector_moment_polynomials=moment_report,status='PASS_G01065_OPTIMIZED_RATIONAL_POINT_ONLY',g=str(g),all_integer_L_ge2_gap=str(final),gap_decimal='.021451810876',unique_full_Hilbert_ground=True,continuous_coupling_extension=False,fresh_full_variance_and_count_gates=reports,split_rayleigh_uppers=upperproof,states=states,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['cpu_seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
