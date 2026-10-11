import os,resource,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,itertools,math,importlib.util,time
H=Path(__file__).resolve().parent;S=H/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();start=time.process_time()
spec=importlib.util.spec_from_file_location('accepted_g011_review',S/'prior_review/audit.py');R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R);P=R.P
poly=lambda c,g:sum(F(x)*g**i for i,x in enumerate(c))
def contract(c,m):return sum(c[i]*F(m[i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
def check_group(name,expected):
 mf=S/name/'MANIFEST_SHA256.json';assert sha(mf)==expected;data=load(mf)
 for f in (S/name).rglob('*'):
  if f.is_file() and f!=mf and '__pycache__' not in f.parts:
   rel=str(f.relative_to(S/name));assert rel in data and sha(f)==data[rel],(name,rel)
def qbounds(z):
 a,b=z;r=R.root(F(2));v=[a+b*r,a+b*(r+F(1,10**60))];return min(v),max(v)
def moments(N,c,M,tag):
 c=list(map(F,c));norm=contract(c,M['gram']);rr=[contract(c,m)/norm for m in M['H_coefficients']];ss=[contract(c,m)/norm for m in M['H2_coefficients']];vv=[ss[0]-rr[0]**2,ss[1]-2*rr[0]*rr[1],ss[2]-rr[1]**2]
 assert norm>0 and vv[0]>=0 and vv[2]>=0 and 4*vv[0]*vv[2]>=vv[1]**2
 return dict(tag=tag,N=N,norm=norm,rho=rr,second=ss,variance=vv)
def main():
 check_group('producer','f0964e98022793c1f200e63c290acd340539e59833a6ecffc1610b4ef08132e3')
 check_group('prior_review','914b267d33635a576b591358c1b7e0e152b3b51111bbaeb18c7a0aa980f1f70a')
 check_group('bilayer_split_H2_fixture_review','7312565327e2b018b62051ddaf555a7f7c08f89376b897a95fc823d7a2a8a083')
 check_group('bilayer_complete_split_H2_8x4_review','874c87f1ff9b4b58f795ef5e01aad45ff4f22e560e4721c7a933ed27380166a5')
 check_group('bilayer_g0105_actual_point_review','02cdd689b9bf4608b540a95316672708eb4691b56057ad8fb23082a930185c12')
 check_group('bilayer_16d_4x4_residual_g0105','5cd6c9b53f9783d6b45b37b3c8ce5e05f6be45a886507a700848816672f53cb2')
 check_group('bilayer_optimized_residual_g0105','9df4cae3ebe0a8e6bfd5a9a0a7ed8e0cfc90963ec5f185818a03ef9f13f397fc')
 P.verify();M16=load(S/'bilayer_split_H2_fixture_review/snapshot/producer/complete_H2_polynomial_4x4.json');M32=load(S/'bilayer_complete_split_H2_8x4_review/audit.json');MM={16:M16,32:M32}
 w16=next(x for x in load(P.S/'optimization/result.json')['results'] if x['shape']==[4,4] and F(x['g'])==F(11,100));w32=next(x for x in load(R.S/'bilayer_split_pencil_optimization_review/audit.json')['physical_endpoints'] if F(x['g'])==F(11,100))
 # Exact .11 coefficient vector is pinned by the endpoint review's producer copy in the physical library's split data.
 source57=load(S/'WITNESS57.json');w32source=next(x for x in source57['results'] if F(x['g'])==F(11,100))
 assert sha(S/'WITNESS57.json')==load(R.S/'bilayer_split_pencil_optimization_review/MANIFEST_SHA256.json')['snapshot/producer/result.json']
 def embed(c):n=(len(c)-1)//3;k=2*n+1;return c[:k]+c[k:]+c[k:]
 choices={16:[moments(16,embed(w16['integer_coefficients']),M16,'g011')],32:[moments(32,w32source['integer_coefficients'],M32,'g011')]}
 for N,group in [(16,'bilayer_16d_4x4_residual_g0105'),(32,'bilayer_optimized_residual_g0105')]:
  c=load(S/group/'trial.json')['trial']['integer_coefficients'];m=moments(N,embed(c),MM[N],'g0105');old=load(S/'bilayer_g0105_actual_point_review/snapshot'/('physical_result_%d.json'%N));assert m['norm']==F(old['norm']) and poly(m['rho'],F(21,200))==F(old['shifted_Rayleigh']) and poly(m['variance'],F(21,200))==F(old['complete_variance']);choices[N].append(m)
 for N,oldlower in [(16,F(w16['Temple_lower'])),(32,F(w32['ground_lower']))]:
  m=choices[N][0];rho=poly(m['rho'],F(11,100));var=poly(m['variance'],F(11,100));assert rho-var/(P.reference(N,F(11,100),2)-rho)==oldlower
 prod=load(S/'producer/result.json');cert=next(x['certificate'] for x in prod['results'] if F(x['g'])==F(53,500));assert cert==load(S/'producer/candidate_g0106.json');g=F(cert['g']);assert g==F(53,500);phys=cert['physical']
 opts=load(R.DATA/'bilayer_split_basis_plan/reoptimization.json')['results'];uppers={};upperproof=[]
 for shape in ((4,4),(8,4),(8,8)):
  row=next(x['split'] for x in opts if x['shape']==list(shape) and F(x['g'])==F(11,100));geo=load(R.S/'third_moment_review/results/geometry_8x8.json') if shape==(8,8) else load(P.S/('GEOMETRY_%dx%d.json'%shape));norm,co,rho=R.split_rayleigh(shape,geo,list(map(F,row['integer_coefficients'])),g);assert norm==F(row['norm']) and co==list(map(F,row['rayleigh_coefficients']));uppers[math.prod(shape)]=rho;upperproof.append(dict(shape=shape,rayleigh=str(rho),coefficients=list(map(str,co))))
 oldnum=load(S/'bilayer_g0105_actual_point_review/snapshot/point_producer/candidate.json')['results'][0]['physical_input']['largest_base_trial'];c=list(map(F,oldnum['integer_coefficients']));assert len(c)==43
 # The old43D vector embeds in the same accepted57D first-H geometry; check its saved affine coefficients afresh.
 geo=load(R.S/'third_moment_review/results/geometry_8x8.json');_,co,oldrho=R.split_rayleigh((8,8),geo,embed(c),g);assert co==list(map(F,oldnum['rayleigh_coefficients']));numerator=min(uppers[64],oldrho);assert numerator==F(phys['numerator_rayleigh'])
 d=next(x['data'] for x in load(R.DATA/'bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100));ns=P.ns;patches=[];reports=[]
 for ix,N in enumerate((16,32)):
  a=P.reference(N,g,2);r1=P.reference(N,g,1);cands=[]
  for m in choices[N]:
   rho=poly(m['rho'],g);var=poly(m['variance'],g);assert var>=0 and rho<r1<a;cands.append((rho-var/(a-rho),rho,var,m))
  lower,rho,var,m=max(cands,key=lambda x:x[0]);pivot=min(uppers[N],*(x[1] for x in cands));saved=phys['patches'][ix]
  for key,val in [('r1',r1),('r2',a),('rho',rho),('variance',var),('ground_lower',lower),('pivot',pivot),('ground_width',pivot-lower),('global_ground_margin',r1-rho)]:assert F(saved[key])==val,key
  assert saved['chosen_ground_vector']==m['tag'] and lower<pivot<r1
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
 short=load(R.S/'bilayer_short_bridge_refinement_review/ACCEPTANCE.json')['continuous_positive_bounds'][0];assert F(short['coupling_interval'][0])<=g<=F(short['coupling_interval'][1]);final=min(F(short['gap_lower']),*gaps);assert final==F(cert['all_integer_L_ge2_gap'])==F(10472755223,500000000000)
 moment_report=[dict(tag=m['tag'],N=m['N'],norm=str(m['norm']),rho=list(map(str,m['rho'])),second=list(map(str,m['second'])),variance=list(map(str,m['variance']))) for vv in choices.values() for m in vv]
 out=dict(fixed_vector_moment_polynomials=moment_report,status='PASS_G0106_ALL_INTEGER_POINT_ONLY',g=str(g),all_integer_L_ge2_gap=str(final),gap_decimal='.020945510446',unique_full_Hilbert_ground=True,continuous_coupling_extension=False,fresh_full_variance_and_count_gates=reports,split_rayleigh_uppers=upperproof,states=states,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['cpu_seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
