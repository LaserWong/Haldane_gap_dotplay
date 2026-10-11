import os,resource
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,math,time,itertools
H=Path(__file__).resolve().parent;S=H/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Exact free *-algebra. x=C, y=Cdagger, z=D; no bosonic commutation assumed.
def clean(p):return {w:c for w,c in p.items() if c}
def plus(*ps):
 d=Counter()
 for p in ps:
  for w,c in p.items():d[w]+=c
 return clean(d)
def times(a,b):
 d=Counter()
 for x,c in a.items():
  for y,e in b.items():d[x+y]+=c*e
 return clean(d)
def scale(p,s):return clean({w:c*s for w,c in p.items()})
def adj(p):return {tuple({'x':'y','y':'x','z':'z'}[c] for c in reversed(w)):v for w,v in p.items()}
def comm(a,b):return plus(times(a,b),scale(times(b,a),-1))
x={('x',):1};y={('y',):1};z={('z',):1};K=comm(x,y);E=comm(z,y);N=comm(x,E);L=comm(comm(x,K),y)
def prod(*ops):
 r={():1}
 for a in ops:r=times(r,a)
 return r

def free_checks():
 rhs=plus(prod(y,x,z),prod(z,y,x),scale(prod(y,z,x),-1),prod(K,z),N)
 assert prod(x,z,y)==rhs
 assert plus(prod(K,z),N)==adj(plus(prod(K,z),N)) and N!=adj(N)
 bad=plus(prod(y,x,z),prod(z,y,x),scale(prod(y,z,x),-1),prod(z,K),N);assert prod(x,z,y)!=bad
 assert prod(z,y)==plus(prod(y,z),E)
 assert prod(x,E)==plus(prod(E,x),N)
 assert prod(x,y)==plus(prod(y,x),K)
 assert prod(adj(E),E)==plus(prod(E,adj(E)),comm(adj(E),E))
 rhs10=plus(prod(x,y,x,y),prod(y,x,K),prod(K,y,x),scale(prod(y,K,x),-1),prod(K,K),L)
 assert prod(x,x,y,y)==rhs10 and L==adj(L) and K==adj(K)
 assert prod(x,x,y,y)!=plus(rhs10,prod(y,K,x)) # removing required negative term fails
 for op in (K,N,L,comm(adj(E),E)):
  assert all(sum({'x':-2,'y':2,'z':0}[c] for c in w)==0 for w in op)
 return dict(m3_normal_order_exact=True,q8_cross_normal_order_exact=True,q8_norm_normal_order_exact=True,q10_norm_normal_order_exact=True,KD_plus_nested_Hermitian=True,nested_m3_not_individually_Hermitian=True,q10_L_Hermitian=True,wrong_orientation_and_dropped_negative_term_rejected=True,normal_ordered_m3_operator={''.join(k):v for k,v in rhs.items()},normal_ordered_q10_operator={''.join(k):v for k,v in rhs10.items()})

def mat(a):return [[F(x) for x in r] for r in a]
def mv(a,v):return [sum(x*y for x,y in zip(r,v)) for r in a]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def trans(a):return list(map(list,zip(*a)))
def block(a,i,j,n,m=None):return [r[j:j+(n if m is None else m)] for r in a[i:i+n]]
def solve(a,v):
 a=mat(a);v=list(map(F,v));n=len(v)
 for j in range(n):
  pivot=a[j][j];assert pivot>0
  for i in range(j+1,n):
   f=a[i][j]/pivot
   for k in range(j+1,n):a[i][k]-=f*a[j][k]
   v[i]-=f*v[j]
 out=[F(0)]*n
 for j in reversed(range(n)):out[j]=(v[j]-sum(a[j][k]*out[k] for k in range(j+1,n)))/a[j][j]
 return out

def krylov_upper_fixture():
 energies=[F(-1,2),F(2)];weights=[F(9,10),F(1,10)];mom=[sum(w*e**k for w,e in zip(weights,energies)) for k in range(5)];lo=F(-3,5);upper=F(2);a=F(2);target=F(-11,20)
 bound=(upper+lo)*mom[3]-lo*upper*mom[2];assert bound>=mom[4]
 G=[[1,mom[1]],[mom[1],mom[2]]];HH=[[mom[1],mom[2]],[mom[2],mom[3]]];JJ=[[mom[2],mom[3]],[mom[3],bound]];v=[F(2),F(-1)]
 p=[[JJ[i][j]-(a+target)*HH[i][j]+a*target*G[i][j] for j in range(2)] for i in range(2)]
 witness=dot(v,mv(p,v));assert witness<0 and lo<target<energies[0] and mom[2]-mom[1]**2>0
 invalid_lo=F(-2,5);invalid_bound=(upper+invalid_lo)*mom[3]-invalid_lo*upper*mom[2];assert invalid_bound<mom[4]
 return dict(spectrum=list(map(str,energies)),weights=list(map(str,weights)),moments=list(map(str,mom)),verified_lower=str(lo),verified_upper=str(upper),m4_upper=str(bound),upper_pencil_negative_witness=str(witness),target=str(target),improves_verified_lower=True,invalid_hypothetical_lower_breaks_m4_upper=True)

def barrier_check():
 assert sha(S/'BARRIER_MANIFEST.json')=='9c5454fa5a7baa7be1928b9cec5b289e02340ef81275f01bd17def266deaf744'
 for rel,h in load(S/'BARRIER_MANIFEST.json').items():assert sha(S/'barrier_producer'/rel)==h
 producer=load(S/'barrier_producer/result.json')
 data=load(S/'ENDPOINT57_audit.json'); row=next(x for x in data['physical_endpoints'] if F(x['g'])==F(11,100));rho=F(row['rayleigh']);v=F(row['complete_variance']);ell=F(row['ground_lower']);a=F(row['full_even_singlet_cutoff']);U=F(32)*(1+F(11,100));cap=8+32*F(11,100);m2=rho*rho+v
 assert ell==rho-v/(a-rho) and v>0
 low=a+ell-rho; high=U-v/(U-rho); assert low<cap<high
 b0=(U+ell)*rho-ell*U-m2;assert b0>0
 out=[]
 for target in data['target_exclusions']:
  l=F(target['target_lower']);p00=v+(rho-a)*(rho-l);assert p00>0
  def vals(R,sharp):
   m3=rho**3+2*rho*v+R*v
   M4=(U+ell)*m3-ell*U*m2
   if sharp:M4-=(-m3+(U+ell)*m2-ell*U*rho)**2/b0
   p01=v*(rho+R-a-l)
   p11=M4-2*rho*m3+rho*rho*m2-(a+l)*v*R+a*l*v
   return p00*p11-p01*p01
  bounds=[]
  for sharp in (False,True):
   c=vals(F(0),sharp);b=(4*vals(F(1),sharp)-vals(F(2),sharp)-3*c)/2;aa=vals(F(1),sharp)-b-c
   pb=next(z for z in producer['results'] if z['beta']==target['beta'])['bounds'][int(sharp)]
   assert list(map(F,pb['determinant_coefficients']))==[c,b,aa]
   plo,phi=map(F,pb['large_root_bracket']);assert vals(plo,sharp)>=0 and vals(phi,sharp)<0
   assert aa<0 and vals(low,sharp)>=0 and vals(cap,sharp)>0 and vals(high,sharp)<0
   assert (vals(low,sharp)==0)==sharp
   left,right=cap,high
   for _ in range(72):
    mid=(left+right)/2
    if vals(mid,sharp)>=0:left=mid
    else:right=mid
   bounds.append(dict(sharp_interval_PSD=sharp,determinant_coefficients=list(map(str,[c,b,aa])),feasible_endpoint_determinants=list(map(str,[vals(low,sharp),vals(cap,sharp)])),positive_root_bracket=list(map(str,[left,right])),root_display=[float(left),float(right)]))
  # Exact two-point Jacobi model has the same first two moments and bypasses both envelopes.
  R=F(9,2);m3=rho**3+2*rho*v+R*v;m4=m2*m2+v*(rho+R)**2
  off=v*(rho+R-a-l);bottom=m4-2*rho*m3+rho*rho*m2-(a+l)*v*R+a*l*v
  exactdet=p00*bottom-off*off;poly=lambda z:(z-rho)*(z-R)-v
  assert exactdet<0 and poly(ell)>0 and poly(l)>0 and poly(a)<0 and poly(U)>0 and ell<l<rho<a<U
  out.append(dict(beta=target['beta'],target=str(l),p00=str(p00),bounds=bounds,two_atom_counterexample=dict(R=str(R),m3=str(m3),m4=str(m4),negative_true_pencil_determinant=str(exactdet))))
 return dict(g='11/100',rho=str(rho),variance=str(v),verified_lower=str(ell),cutoff=str(a),global_upper=str(U),residual_R_lower=str(low),residual_R_upper=str(cap),support_q_max=8,interaction_upper_proof='Each two-layer exchange edge has upper1/2;64 weighted edges give V<=32, hence q<=8 implies R<=8+32g=288/25.',cases=out,scope='Only this fixed57D witness, these two targets, and these two m4 envelopes; exact Krylov and other witnesses remain open.')

def main():
 start=time.monotonic();pm=S/'PRODUCER_MANIFEST.json';assert sha(pm)=='e20d397dec2b07d66900d4740b6896ddbf404fb0069092108f6ed18ca3a17b47'
 for rel,h in load(pm).items():assert sha(S/'producer'/rel)==h
 assert sha(S/'COST_ERRATUM.json')=='4dd66a84b3b29ca86993d7e63af260561b33b534397060d1f42e736e26c43e1f'
 for tag,h in [('MATRIX57','874c87f1ff9b4b58f795ef5e01aad45ff4f22e560e4721c7a933ed27380166a5'),('ENDPOINT57','fc205510f91902c1c9da6ba9bbdedefe69900a0fb1505fbd541aefe312417381')]:
  mf=S/(tag+'_MANIFEST_SHA256.json');assert sha(mf)==h
  for name in ['audit.json','ACCEPTANCE.json']:assert sha(S/(tag+'_'+name))==load(mf)[name]
 assert sha(S/'OLD43_audit.json')==load(S/'MATRIX57_MANIFEST_SHA256.json')['snapshot/OLD43_audit.json']
 assert sha(S/'WITNESSES57.json')==load(S/'ENDPOINT57_MANIFEST_SHA256.json')['snapshot/producer/result.json']
 algebra=free_checks();toy=krylov_upper_fixture();barrier=barrier_check();full=load(S/'MATRIX57_audit.json');G=mat(full['gram']);A=[[2*F(x) for x in r] for r in full['H_coefficients'][1]];V=block(G,29,29,14);W=block(G,43,43,14);X=block(A,29,29,14);Y=block(A,29,43,14);Z=block(A,43,43,14);G4=block(G,15,15,28)
 blocks={k:mat(v) for k,v in full['blocks'].items()};old=load(S/'OLD43_audit.json');CM=mat(old['blocks']['CMCM']);Q8=mat(old['q8_Gram']);shapes=load(S/'producer/cached_shapes.json')['results'];wit=load(S/'WITNESSES57.json')['results'];endpoints=load(S/'ENDPOINT57_audit.json')['physical_endpoints'];ranks=[]
 for row in shapes:
  g=F(row['g']);w=next(x for x in wit if F(x['g'])==g);c=list(map(F,w['integer_coefficients']));cr=c[29:43];ct=c[43:57];norm=F(w['norm']);variance=F(w['variance']);t=g/2
  for key,v in [('P_integer_R_coefficients',cr),('P_integer_M_coefficients',ct),('T_integer_R_coefficients',cr),('T_integer_M_coefficients',ct)]:assert list(map(F,row[key]))==v
  hp=[x+y for x,y in zip(mv(V,cr),mv(W,ct))]+[x+y for x,y in zip(mv(X,cr),mv(Y,ct))];ht=[x+y for x,y in zip(mv(trans(Y),cr),mv(Z,ct))]
  pn=dot(cr,mv(blocks['R4R4'],cr))+2*dot(cr,mv(blocks['R4CM'],ct))+dot(ct,mv(CM,ct));tn=dot(cr,mv(blocks['R6R6'],cr))+2*dot(cr,mv(blocks['R6M6'],ct))+dot(ct,mv(blocks['M6M6'],ct))
  ps=pn-dot(hp,solve(G4,hp));ts=tn-dot(ht,solve(W,ht));assert ps==F(row['P_schur_norm'])>0 and ts==F(row['T_schur_norm'])>0
  parts=dict(q4_outside57=t*t*ps/norm,q6_outside57=t*t*ts/norm,q8_outside57=t*t*dot(ct,mv(Q8,ct))/norm);parts['inside57_residual']=variance-sum(parts.values());assert all(v>=0 for v in parts.values()) and sum(parts.values())==variance
  assert {k:F(v) for k,v in row['residual_parts'].items()}==parts and row['T_only_dimension']==58 and row['P_and_T_dimension']==59
  assert F(next(e for e in endpoints if F(e['g'])==g)['complete_variance'])==variance
  ranks.append(dict(g=str(g),P_schur_norm=str(ps),T_schur_norm=str(ts),T_only_rank=58,P_and_T_rank=59,residual_parts={k:str(v) for k,v in parts.items()},residual_fractions={k:str(v/variance) for k,v in parts.items()}))
 costs=load(S/'producer/cost_counts.json');expected=dict(fixed_origin_q4=math.comb(31,3),fixed_origin_q6=math.comb(31,5),fixed_origin_q8=math.comb(31,7),fixed_origin_q10=math.comb(31,9),T_q6_int128_cache_bytes=math.comb(31,5)*15*16,P_q4_int128_cache_bytes=math.comb(32,4)*3*16,q8_int128_cache_bytes=math.comb(31,7)*105*16,connected_ordered_edge_triples_upper=64*7*12,connected_ordered_edge_quadruples_upper=64*7*12*16)
 for k,v in expected.items():assert costs[k]==v
 err=load(S/'COST_ERRATUM.json');assert err['connected_prefix_quadruples_upper']==expected['connected_ordered_edge_quadruples_upper'] and err['uniform_quartet_family_upper']==2*64*7*12*16==172032
 out=dict(status='PASS_SYMBOLIC_NORMAL_ORDERING_AND_CACHED_RANK_COST_PLAN_ONLY',free_algebra=algebra,m4_upper_pencil_fixture=toy,cached_rank_checks=ranks,exact_cost_counts=expected,corrected_uniform_quartet_ceiling=172032,scoped_m4_envelope_barrier=barrier,recommended_first_fixture='Generic q6 T lookup and signed K small-geometry fixture for58D; alternatively exact m4 nested-commutator local fixture. Skip m3-only full support for selected targets.',exact_m4_fixture_deferred=False,no_new_physical_support=True,no_new_m3_or_m4_for_actual_witness=True,no_new_energy_or_gap=True,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
