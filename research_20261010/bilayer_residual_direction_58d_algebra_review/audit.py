import os,resource,sys,time,json,hashlib,math,ast,itertools
from pathlib import Path
from fractions import Fraction as F
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,((6,6) if "--witness-only" in sys.argv else (60,60)));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));sys.set_int_max_str_digits(0)
P=Path(__file__).resolve().parent;R=P.parent;S=P/'snapshot';start=time.process_time()
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def seal(folder,h):
 assert sha(folder/'MANIFEST_SHA256.json')==h
 for f,v in load(folder/'MANIFEST_SHA256.json').items():assert sha(folder/f)==v,f
seal(S,'1bdec7a19aa4f7c8aa586fbb6b66bda65035e99fd86871c4952e134cf88f301b')
assert sha(S/'RESOURCE_ADDENDUM_SHA256.json')=='ecb288368cfc2d2f21a2f0d2ec21974ec203d7481fab8aae4e28d6a2bb23d119'
for f,h in load(S/'RESOURCE_ADDENDUM_SHA256.json').items():assert sha(S/f)==h
paths={'M58':R/'bilayer_complete_residual_direction_58d_review','M57':R/'bilayer_complete_split_H2_8x4_review','OLD_REVIEW':R/'bilayer_residual_pencil_optimization_review'}
for key,h in [('M58','13e12855678f844ce419319908087ad05a7de6d5dd547ee2060d4db7ccee1887'),('M57','874c87f1ff9b4b58f795ef5e01aad45ff4f22e560e4721c7a933ed27380166a5'),('OLD_REVIEW','9c6a17ceb920c20f323ccd27751b2d863f264566b0b1c8d46d5db4f2ea50c053')]:assert sha(paths[key]/'MANIFEST_SHA256.json')==h
for key in ['M58','M57']:assert sha(paths[key]/'audit.json')==load(paths[key]/'MANIFEST_SHA256.json')['audit.json']
old=paths['OLD_REVIEW'];om=load(old/'MANIFEST_SHA256.json')
for f in ['snapshot/ACCEPTED_ODD_AUDIT.py','snapshot/ODD_STRUCTURAL_POLYNOMIALS.json']:assert sha(old/f)==om[f]
def poly(c,g):return sum(x*g**j for j,x in enumerate(c))
def root(x):
 d=10**60;k=math.isqrt(x.numerator*d*d//x.denominator);r=F(k,d);assert r*r<=x<(r+F(1,d))**2;return r
def ref(N,g,q):return F(3*N,8)*(2*g-1)+(F(3*N,8)+q)*root(1-4*g)
def mat(x):return [[F(v) for v in row] for row in x]
def bil(c,a):return sum(c[i]*sum(x*y for x,y in zip(row,c)) for i,row in enumerate(a))
def combine(cs,g):return [[sum(m[i][j]*g**k for k,m in enumerate(cs)) for j in range(len(cs[0]))] for i in range(len(cs[0]))]
def parse(m):return mat(m['gram']),list(map(mat,m['H_coefficients'])),list(map(mat,m['H2_coefficients']))
M58=load(paths['M58']/'audit.json');M57=load(paths['M57']/'audit.json');producer=load(S/'complete_58d_polynomial.json')
for k in ['gram','H_coefficients','H2_coefficients']:assert producer[k]==M58[k]
M16=load(R/'bilayer_split_H2_fixture_review/snapshot/producer/complete_H2_polynomial_4x4.json');NM=load(R/'bilayer_g0105_actual_point_review/snapshot/NUMERATOR_8x8_MATRIX.json')
# Independent accepted Q(sqrt2) odd-band algebra, stripped of all execution/resource statements.
ns={'F':F,'math':math,'poly':poly,'Z':(F(0),F(0)),'ONE':(F(1),F(0))};ns['COS']=[(F(1),F(0)),(F(0),F(1,2)),(F(0),F(0)),(F(0),F(-1,2)),(F(-1),F(0)),(F(0),F(-1,2)),(F(0),F(0)),(F(0),F(1,2))]
names={'q','qa','qs','qm','qd','sign','qpoly','qlist','symbol','decompose','fixed_arrays'};nodes=[n for n in ast.parse((old/'snapshot/ACCEPTED_ODD_AUDIT.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in nodes}==names;exec(compile(ast.Module(body=nodes,type_ignores=[]),'accepted_independent_odd','exec'),ns)
raw=load(old/'snapshot/ODD_STRUCTURAL_POLYNOMIALS.json')['coefficients'];ns['ODD']={tuple(map(int,k.split('x'))):{key:[[[F(c) for c in cell] for cell in row] for row in a] for key,a in v.items()} for k,v in raw.items()}
def qb(x):
 a,b=x;r=root(F(2));ends=[a+b*r,a+b*(r+F(1,10**60))];return min(ends),max(ends)
def witness(w,m,N,g):
 G,hc,jc=parse(m);c=w['integer_coefficients'];assert all(type(x)is int for x in c) and len(c)==len(G) and c[0]==2**96
 norm=bil(c,G);rho=[bil(c,a)/norm for a in hc];second=[bil(c,a)/norm for a in jc];var=[second[0]-rho[0]**2,second[1]-2*rho[0]*rho[1],second[2]-rho[1]**2];r=poly(rho,g);v=poly(var,g);a=ref(N,g,2);r1=ref(N,g,1);lo=r-v/(a-r);ell=F(w['strict_endpoint']);pen=poly(second,g)-(a+ell)*r+a*ell
 assert norm>0 and v>=0 and r<r1<a and ell<lo<a and pen<0
 for k,x in [('norm',norm),('rho',r),('second_moment',poly(second,g)),('variance',v),('r1',r1),('r2',a),('ground_lower',lo),('negative_pencil',pen)]:assert F(w[k])==x,k
 for k,x in [('rayleigh_coefficients',rho),('full_second_moment_coefficients',second),('full_variance_coefficients',var)]:assert list(map(F,w[k]))==x,k
 return dict(lower=lo,rho=r,variance=v,strict=ell,pencil=pen)
def odd_check(patch,N,g,pivot):
 shape=(4,4) if N==16 else(8,4);arr=ns['fixed_arrays'](*shape,F(1,10));seen=set();lowers=[];margins=[];a=ref(N,g,2);r1=ref(N,g,1)
 for saved in patch['odd_details']:
  kx,ky=saved['momentum'];assert (kx,ky) not in seen;seen.add((kx,ky));symbols={k:ns['symbol'](x,*shape,kx,ky) for k,x in arr.items()};gg=symbols['G'];assert ns['sign'](gg)>0 and gg==tuple(map(F,saved['gram_symbol']))
  theta=[ns['qd'](symbols[k],gg) for k in ['Q','V']];second=[ns['qd'](symbols[k],gg) for k in ['Q2','C','D']];variance=[ns['qs'](second[0],ns['qm'](theta[0],theta[0])),ns['qs'](second[1],ns['qm'](ns['q'](2),ns['qm'](theta[0],theta[1]))),ns['qs'](second[2],ns['qm'](theta[1],theta[1]))]
  th=ns['qpoly'](theta,g);vv=ns['qpoly'](variance,g);assert ns['sign'](vv)>=0 and th==tuple(map(F,saved['theta'])) and vv==tuple(map(F,saved['variance']))
  l,u=qb(th);vl,vu=qb(vv);assert u<a;lower=max(r1,l-max(F(0),vu)/(a-u));assert lower==F(saved['lower']) and a-u==F(saved['cutoff_margin']);lowers.append(lower-pivot);margins.append(a-u)
 assert seen==set(itertools.product(range(shape[0]),range(shape[1]))) and len(seen)==N
 assert lowers==list(map(F,patch['odd'])) and min(margins)==F(patch['odd_min_cutoff_margin'])
 assert [ref(N,g,q)-pivot for q in range(2,N+1)]==list(map(F,patch['tail']))
 return {'odd_modes':N,'spin_multiplicity':3,'retained_below_r2':1+3*N,'minimum_margin':str(min(margins)),'complete_momentum_count':True}
rows=load(S/'result.json');reports=[];matrices={}
for row in rows['results']:
 g=F(row['g']);assert g in [F(217,2000),F(11,100)];witnesses={};selected={}
 for label,m,N in [('old57',M57,32),('new58',M58,32),('patch16_witness',M16,16)]:
  w=row[label];assert w['dimension']==len(m['gram']) and F(w['g'])==g
  vals={kind:witness(w[kind+'_optimized'],m,N,g) for kind in ['energy','pencil']};assert w['selected']==max(vals,key=lambda k:vals[k]['lower']);assert F(w['exact_lower_gain_over_energy'])==vals['pencil']['lower']-vals['energy']['lower'];selected[label]=vals[w['selected']];witnesses[label]=vals
 assert F(row['ground_lower_gain'])==selected['new58']['lower']-selected['old57']['lower']>0
 pcounts=[]
 for i,(label,N) in enumerate([('patch16_witness',16),('new58',32)]):
  p=row['physical']['patches'][i];s=selected[label];pivot=witnesses[label]['energy']['rho'];assert F(p['pivot'])==pivot and F(p['ground_lower'])==s['lower'] and F(p['rho'])==s['rho'] and F(p['variance'])==s['variance'];assert F(p['global_ground_margin'])==ref(N,g,1)-s['rho']>0;assert F(p['ground_width'])==pivot-s['lower']>0
  pcounts.append(odd_check(p,N,g,pivot))
 num=row['numerator_witness'];c=list(map(F,num['integer_coefficients']));norm=bil(c,mat(NM['gram']));co=[bil(c,mat(a))/norm for a in NM['affine_A']];assert norm==F(num['norm']) and co==list(map(F,num['rayleigh_coefficients'])) and poly(co,g)==F(num['rayleigh'])==F(row['physical']['numerator_rayleigh'])
 assert row['successful_beta_grid_candidates']==0 and 'conditional_scalar_certificate' not in row
 G,hc,jc=parse(M58);matrices[g]=(G,combine(hc,g),combine(jc,g),ref(32,g,2))
 reports.append({'g':str(g),'dimension':58,'ground_lower':str(selected['new58']['lower']),'strict_endpoint':str(selected['new58']['strict']),'negative_pencil':str(selected['new58']['pencil']),'gain_over_fresh57':str(F(row['ground_lower_gain'])),'global_ground_identified':True,'sector':'full even-singlet sector cutoff after complete odd count','count_gates':pcounts,'grid_failure_scope':'Producer finite grid only; not independently rerun; no universal no-go'})
print('PASS fresh rational vectors, full variances and global/sector count gates',flush=True)
if '--witness-only' in sys.argv:
 destination=P/(sys.argv[sys.argv.index('--witness-only')+1]);destination.write_text(json.dumps({'results':reports,'cpu_limits':resource.getrlimit(resource.RLIMIT_CPU),'address_limits':resource.getrlimit(resource.RLIMIT_AS),'cpu_seconds':time.process_time()-start},indent=2)+'\n');sys.exit(0)
# Fraction-free LDL: independent of producer GMP rational elimination.
def positive_ff(m):
 n=len(m);assert all(m[i][j]==m[j][i] for i in range(n) for j in range(n));den=1
 for row in m:
  for x in row:den=math.lcm(den,x.denominator)
 a=[[int(x*den) for x in row] for row in m];previous=1;piv=[];mins=[]
 for j in range(n):
  pivot=a[j][j];assert pivot>0,(j,pivot);mins.append(str(pivot));piv.append(str(F(pivot,previous*den)))
  for i in range(j+1,n):
   for k in range(i,n):
    v=a[i][k]*pivot-a[i][j]*a[k][j];assert v%previous==0;a[k][i]=a[i][k]=v//previous
  previous=pivot
 return piv,{'scale':str(den),'positive_leading_minors':mins}
assert positive_ff(mat([[2,1],[1,2]]))[0]==['2','3/2']
ldls={r['name']:r for r in load(S/'ldl_complete_results.json')};targetreports=[]
accepted_targets=load(R/'bilayer_pencil_scalar_assessment/result.json')['results'][0]['hypothetical_ground32_targets']
for t in rows['selected_target_checks']:
 g=F(t['g']);ell=F(t['target']);G,H,J,a=matrices[g];m=[[J[i][j]-(a+ell)*H[i][j]+a*ell*G[i][j] for j in range(58)] for i in range(58)];piv,certificate=positive_ff(m)
 assert ldls[t['name']]['PSD'] and ldls[t['name']]['rank_if_PSD']==58 and piv==ldls[t['name']]['pivots']
 if 'beta' in t:assert ell==F(next(x['target_ground32_lower'] for x in accepted_targets if F(x['beta'])==F(t['beta'])))
 lower=next(F(r['ground_lower']) for r in reports if F(r['g'])==g);assert ell-lower==F(t['shortfall'])>0
 targetreports.append({'name':t['name'],'g':str(g),'target':str(ell),'positive_definite':True,'pivots':piv,'fraction_free_certificate':certificate,'scope':t['scope']})
 print('PASS target',t['name'],time.process_time()-start,flush=True)
out={'status':'PASS_58D_RATIONAL_ENDPOINTS_AND_SCOPED_TARGET_EXCLUSIONS','results':reports,'targets':targetreports,'complete_matrix_previously_independently_accepted':True,'producer_resource_compliance':'UNVERIFIED; retained separately from mathematical acceptance','no_new_all_size_gap':True,'cpu_seconds':time.process_time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['cpu_seconds'],out['peak_rss_kib'])
