import os,sys,json,math,time,resource,hashlib,itertools
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parent
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));sys.dont_write_bytecode=True
D=1<<224

def root(x):
 x=F(x);assert x>=0;k=math.isqrt(x.numerator*D*D//x.denominator);lo=F(k,D);hi=F(k+1,D);assert lo*lo<=x<hi*hi;return lo,hi

def geometry(L):
 N=L*L;edges={}
 for i in range(N):
  x,y=divmod(i,L)
  for j in [((x+1)%L)*L+y,x*L+(y+1)%L]:
   p=tuple(sorted((i,j)));edges[p]=edges.get(p,0)+1
 assert all(sum(w for (a,b),w in edges.items() if i in (a,b))==4 for i in range(N))
 S=sum(w*w for w in edges.values());M3=sum(w**3 for w in edges.values());T=sum(edges.get((i,j),0)*edges.get((i,k),0)*edges.get((j,k),0) for i,j,k in itertools.combinations(range(N),3));return N,edges,S,M3,T

def local_A():
 # Unnormalized rung columns: s,t+,t0,t-. A=2*(S_i0.S_j0+S_i1.S_j1).
 R=[[0,1,0,0],[1,0,1,0],[-1,0,1,0],[0,0,0,1]];w=[2,1,2,1]
 U=[[R[i//4][a//4]*R[i%4][a%4] for a in range(16)] for i in range(16)]
 comp=[[F(0) for _ in range(16)] for _ in range(16)]
 for st in range(16):
  bits=[(st>>(3-i))&1 for i in range(4)]
  for i,j in [(0,2),(1,3)]:
   comp[st][st]+=F(1,2) if bits[i]==bits[j] else -F(1,2)
   if bits[i]!=bits[j]:comp[st^(1<<(3-i))^(1<<(3-j))][st]+=1
 H=[[sum(F(U[k][i])*comp[k][l]*U[l][j] for k in range(16) for l in range(16))/(w[i//4]*w[i%4]) for j in range(16)] for i in range(16)]
 assert all(H[i][j]*w[i//4]*w[i%4]==H[j][i]*w[j//4]*w[j%4] for i in range(16) for j in range(16))
 assert {i:H[i][0] for i in range(16) if H[i][0]}=={7:F(-2),10:F(1),13:F(-2)}
 return [[(i//4,i%4,H[i][j]) for i in range(16) if H[i][j]] for j in range(16)]
LOCAL=local_A()

def physical_moments(L):
 N,edges,S,M3,T=geometry(L);B={}
 for (i,j),w in edges.items():
  for a,b,c in [(1,3,-2),(2,2,1),(3,1,-2)]:B[(a<<(2*i))|(b<<(2*j))]=w*c
 mask=sum(1<<(2*i) for i in range(N))
 def weight(st):return F(1,1<<((st&mask).bit_count()))
 norm=sum(c*c*weight(st) for st,c in B.items());assert norm==3*S
 def inner_action(bra,ket):
  value=F(0)
  for st,c in ket.items():
   for (i,j),w in edges.items():
    a=(st>>(2*i))&3;b=(st>>(2*j))&3
    for x,y,h in LOCAL[4*a+b]:
     target=st^((a^x)<<(2*i))^((b^y)<<(2*j))
     if target in bra:value+=bra[target]*weight(target)*c*w*h
  return value
 cross=inner_action(B,{0:1});diagonal=inner_action(B,B)
 assert cross==3*S and diagonal==-6*M3+18*T
 k=F(-M3+3*T,S);assert k==(-2 if L==2 else 0 if L==3 else -1)
 return {'L':L,'N':N,'physical_spins':2*N,'full_Hilbert_dimension':str(4**N),'trial_dimension':2,'B_support':len(B),'edge_count':len(edges),'edge_weight_sum':sum(edges.values()),'edge_square_sum':S,'edge_cube_sum':M3,'weighted_triangle_sum':T,'weighted_degree':4,'reduced_B_norm':str(norm),'vacuum_A_B':str(cross),'B_A_B':str(diagonal),'pair_diagonal_slope':str(k)}

def bounds(L,g):
 _,_,S,M3,T=geometry(L);k=F(-M3+3*T,S);C=F(3*S,16);g=F(g);assert 0<=g<F(1,4);E=2+k*g;disc=E*E+3*S*g*g;dl,du=root(1-4*g);ql,qu=root(disc)
 lam=[C*(2*g-1)+(C+1)*d for d in [dl,du]];ritz=[(E-qu)/2,(E-ql)/2];gap=[lam[0]-ritz[1],lam[1]-ritz[0]]
 return {'L':L,'g':str(g),'second_eigenvalue_lower':str(lam[0]),'second_eigenvalue_upper_comparison_only':str(lam[1]),'Rayleigh_upper':str(ritz[1]),'Rayleigh_lower_in_trial_space_only':str(ritz[0]),'gap_lower':str(gap[0]),'gap_upper_of_this_bound_only':str(gap[1]),'gap_display':float(gap[0]),'delta_enclosure':list(map(str,[dl,du])),'Ritz_discriminant_enclosure':list(map(str,[ql,qu]))}

def fixed_trial_interval(L,gmax):
 _,_,S,M3,T=geometry(L);k=F(-M3+3*T,S);gmax=F(gmax);E=2+k*gmax;ql,qu=root(E*E+3*S*gmax*gmax)
 tlo=gmax/(E+qu);scale=10**18;t=F(tlo.numerator*scale//tlo.denominator,scale)
 def ray(g):return 3*S*((2+k*g)*t*t-g*t)/(1+3*S*t*t)
 endpoint=bounds(L,gmax);Rend=ray(gmax);g0=1-ray(F(0));gend=F(endpoint['second_eigenvalue_lower'])-Rend;uniform=min(g0,gend)
 return {'L':L,'coupling_interval':['0',str(gmax)],'fixed_rational_t':str(t),'state':'vacuum minus t times weighted nearest-neighbor singlet-pair sum','squared_norm_reduced':str(1+3*S*t*t),'rayleigh_at_zero':str(ray(F(0))),'rayleigh_at_upper':str(Rend),'gap_lower_at_zero':str(g0),'gap_lower_at_upper':str(gend),'uniform_gap_lower':str(uniform),'positive':uniform>0}

def root_bracket(L):
 lo,hi=F(0),F(249,1000);assert F(bounds(L,lo)['gap_lower'])>0 and F(bounds(L,hi)['gap_upper_of_this_bound_only'])<0
 for _ in range(48):
  mid=(lo+hi)/2;r=bounds(L,mid)
  if F(r['gap_lower'])>0:lo=mid
  elif F(r['gap_upper_of_this_bound_only'])<0:hi=mid
  else:raise AssertionError('insufficient root precision')
 return {'L':L,'lower':str(lo),'upper':str(hi),'lower_display':float(lo),'upper_display':float(hi),'lower_witness':bounds(L,lo),'upper_witness':bounds(L,hi)}

if __name__=='__main__':
 start=time.time();mom=[physical_moments(L) for L in range(2,8)];br=[root_bracket(L) for L in range(2,8)];rows=[]
 for g in map(F,('3/20','61/400','191/1250','153/1000','77/500','31/200','4/25')):
  rr=[bounds(L,g) for L in range(2,8)];fixed=[fixed_trial_interval(L,g) for L in range(2,8)];lower=min(F(r['uniform_gap_lower']) for r in fixed);rows.append({'continuous_coupling_interval':['0',str(g)],'uniform_short_size_gap':str(lower),'gap_display':float(lower),'positive':lower>0,'per_size':rr,'fixed_rational_trials':fixed,'decimal_gap_lower':str(F(lower.numerator*10**12//lower.denominator,10**12))})
 out={'status':'exact_short_size_bridge_candidate_pending_independent_review','scope':'OnlyL2..7, ordinary periodic bilayer. No all-size/bootstrap gap claim.','geometry_and_exact_physical_moments':mom,'continuous_endpoints':rows,'unique_zero_brackets_of_this_method':br,'seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 (HERE/'result_check.json').write_text(json.dumps(out,indent=2)+'\n');print([(x['continuous_coupling_interval'],x['gap_display']) for x in rows]);print([(x['L'],x['lower_display'],x['upper_display']) for x in br]);print('resources',out['seconds'],out['peak_rss_kib'])
