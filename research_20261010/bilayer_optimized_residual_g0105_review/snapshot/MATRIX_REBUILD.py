"""Fresh block reconstruction, rational rank, third moments and Rayleigh replay.
No producer Python module is imported or executed.
"""
import os,resource,sys
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import itertools,json,hashlib,time,math
import numpy as np
OUT=Path(__file__).resolve().parent;SNAP=OUT/'snapshot';P=SNAP/'producer'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):(OUT/'results'/name).write_text(json.dumps(x,indent=2)+'\n')
def mat(x):return np.array(x,dtype=object)
def zero(n,m):return np.zeros((n,m),dtype=object)
def graph(nx,ny):
 e=Counter()
 for x,y in itertools.product(range(nx),range(ny)):
  a=x*ny+y
  for b in (((x+1)%nx)*ny+y,x*ny+(y+1)%ny):e[tuple(sorted((a,b)))]+=1
 orbits=[];classes={};ids={}
 for a,b in itertools.combinations(range(nx*ny),2):
  ax,ay=divmod(a,ny);bx,by=divmod(b,ny)
  dx=min((ax-bx)%nx,(bx-ax)%nx);dy=min((ay-by)%ny,(by-ay)%ny)
  key=tuple(sorted((dx,dy))) if nx==ny else (dx,dy)
  if key not in classes:classes[key]=len(orbits);orbits.append([])
  index=classes[key];orbits[index].append((a,b));ids[a,b]=index
 assert all(sum(w for edge,w in e.items() if i in edge)==4 for i in range(nx*ny))
 return e,orbits,ids

def rebuild(nx,ny,g,geom):
 edges,orbits,ids=graph(nx,ny);n=len(orbits);d=n+1;t=g/2
 D=np.diag([1]+[3*len(x) for x in orbits]).astype(object)
 C=zero(d,d)
 # Direct q=0,2 physical action in the spatial pair orbit basis.
 for j in range(d):
  pair=defaultdict(F);vac=F(0)
  if j==0:
   for e,w in edges.items():pair[e]+=t*w
  else:
   for a,b in orbits[j-1]:
    w=edges.get((a,b),0);pair[a,b]+=2-2*t*w;vac+=3*t*w
    for (u,v),w in edges.items():
     if u in (a,b) and v not in (a,b):pair[tuple(sorted((v,b if u==a else a)))]+=t*w
     elif v in (a,b) and u not in (a,b):pair[tuple(sorted((u,b if v==a else a)))]+=t*w
  C[0,j]=vac
  for i,orb in enumerate(orbits,1):
   vals={pair[e] for e in orb};assert len(vals)==1;C[i,j]=vals.pop()
 FF,S,V,W,X,Y,Z=[mat(geom[k]) for k in ('F','S','V','W','X','Y','Z')]
 for name,M in [('F',FF),('S',S),('V',V),('W',W),('X',X),('Z',Z)]:assert np.array_equal(M,M.T),name
 E=np.vstack([zero(1,n),np.eye(n,dtype=object)])
 EF=E@FF;ES=E@S
 G=np.block([[D,zero(d,n),zero(d,n)],[zero(n,d),FF,S],[zero(n,d),S.T,V+W]])
 A=np.block([[D@C,t*EF,t*ES],[t*EF.T,4*FF+t*S,4*S+t*(V+W)],[t*ES.T,4*S.T+t*(V+W),4*V+6*W+t*(X+Y+Y.T+Z)]])
 assert np.array_equal(G,G.T) and np.array_equal(A,A.T)
 lower=mat([[F(t*EF[i,j],D[i,i]) for j in range(n)] for i in range(d)])
 Hmap=np.block([[C,lower],[t*E.T,4*np.eye(n,dtype=object)],[zero(n,d),t*np.eye(n,dtype=object)]])
 old=2*n+1;G0=G[:old,:old];A0=A[:old,:old];J0=Hmap.T@G@Hmap;H30=Hmap.T@A@Hmap
 B0=np.vstack([np.eye(d,dtype=object),zero(2*n,d)])
 B1=Hmap[:,:d];B2=Hmap@B1[:old,:]
 return dict(G=G,A=A,G0=G0,A0=A0,J0=J0,H30=H30,B0=B0,B1=B1,B2=B2,Hmap=Hmap,orbits=orbits)

def rank_psd(G):
 a=[[F(x) for x in row] for row in G];pivots=[];selected=[]
 for i in range(len(a)):
  p=a[i][i];assert p>=0,('nonPSD',i,p)
  if p:
   pivots.append(str(p));selected.append(i)
   for j in range(i+1,len(a)):
    for k in range(j,len(a)):
     a[j][k]-=a[j][i]*a[i][k]/p;a[k][j]=a[j][k]
  else:assert all(x==0 for x in a[i][i:])
 return selected,pivots

def bil(c,M):return F(mat(c)@M@mat(c))
def check_filter(saved,m1,m2,m3,norm):
 v=m2-m1*m1;z=m3-2*m1*m2+m1**3;R=z/v
 assert v>0 and F(saved['exact_original_norm'])==norm
 for key,x in [('exact_original_shifted_rayleigh',m1),('exact_second_moment',m2),('exact_third_moment',m3),('exact_original_variance',v),('exact_residual_H_expectation',z),('exact_residual_Rayleigh',R)]:assert F(saved[key])==x,key
 assert mat(saved['rational_two_vector_gram']).tolist()==[['1','0'],['0',str(v)]]
 assert [[F(x) for x in row] for row in saved['rational_two_vector_H']]==[[m1,v],[v,z]]
 f=saved['filter'];delta=F(f['improvement']);C=R-m1;alpha=F(f['t'])
 assert C>0 and delta>0 and alpha==delta/v and F(f['C'])==C and F(f['variance'])==v
 slack=v-delta*(C+delta);assert slack>=0 and F(f['quadratic_slack'])==slack
 n=1+alpha*alpha*v;energy=(m1-2*alpha*v+alpha*alpha*z)/n
 assert F(f['normalization_squared'])==n and energy==F(f['achieved_bound'])<=m1-delta
 unit=10**f['rounding_digits'];discr=C*C+4*v;k=math.isqrt(discr.numerator*unit*unit//discr.denominator)
 root=F(k,unit);assert root*root<=discr<(root+F(1,unit))**2
 elementary=v*C/(C*C+v);assert F(f['elementary_t_one_over_C_gain'])==elementary
 assert delta==max(F(0),(root-C)/2,elementary)
 assert F(saved['shifted_rayleigh_upper'])==F(f['shifted_rayleigh_upper'])==m1-delta
 assert saved['retained_numerator_states']==1 and saved['filtered_max_triplet_number']==6 and saved['no_filtered_residual_claim'] and saved['no_H4_of_original_trial_claim']
 return m1-delta,dict(exact_m3=str(m3),exact_residual_Rayleigh=str(R),filter_upper=str(m1-delta),filter_upper_display=float(m1-delta),actual_rational_filtered_energy=str(energy),positive_slack=str(slack))

def audit():
 inputs=load(OUT/'INPUT_SHA256.json');assert all(sha(SNAP/p)==h for p,h in inputs.items())
 freeze=load(P/'PHYSICAL_MANIFEST.json');assert all(sha(P/p)==h for p,h in freeze['files'].items())
 out=[]
 for shape in ('4x4','8x4','8x8'):
  nx,ny=map(int,shape.split('x'));geom=load(OUT/'results'/f'geometry_{shape}.json');old=load(SNAP/'original'/f'block1_{shape}_g9d100.json');g=F(old['coupling']);den=old['integer_matrix_denominator']
  prod=load(P/f'geometry_{shape}_origin.json');prior=load(SNAP/'prior_geometry'/f'geometry_{shape}.json')
  assert all(geom[k]==prod[k] for k in 'F S V W X Y Z'.split())
  assert all(geom[k]==prior[k] for k in 'F S V W'.split())
  r=rebuild(nx,ny,g,geom);G,A=r['G'],r['A'];rank,piv=rank_psd(G);oldrank,oldpiv=rank_psd(r['G0']);n=len(r['orbits']);d=n+1
  assert oldrank==old['selected_basis_indices'];sel=np.ix_(oldrank,oldrank)
  assert r['G0'][sel].tolist()==old['gram']
  assert (den*r['A0'][sel]).tolist()==old['shifted_hamiltonian_numerator']
  assert (den*den*r['J0'][sel]).tolist()==old['shifted_H2_numerator']
  moments=[mat(m) for m in old['shifted_integer_moments_M0_to_M4']];powers=[r['B0'],r['B1'],r['B2']]
  for i in range(3):
   for j in range(3):
    assert (den**(i+j)*(powers[i].T@G@powers[j])).tolist()==moments[i+j].tolist()
    if i+j<4:assert (den**(i+j+1)*(powers[i].T@A@powers[j])).tolist()==moments[i+j+1].tolist()
  c=list(map(F,old['coefficients']));norm=bil(c,r['G0'][sel]);m1=bil(c,r['A0'][sel])/norm;m2=bil(c,r['J0'][sel])/norm;m3=bil(c,r['H30'][sel])/norm
  assert m1==F(old['exact_rayleigh'])+F(3*nx*ny,4) and m2-m1*m1==F(old['exact_residual_squared'])
  filtered=load(P/f'filtered_{shape}_g9d100.json');fil,filterinfo=check_filter(filtered,m1,m2,m3,norm)
  larger=load(P/f'enlarged_{shape}_g9d100.json');assert rank==larger['selected_basis_indices'];sel=np.ix_(rank,rank)
  assert G[sel].tolist()==larger['gram'] and (den*A[sel]).tolist()==larger['shifted_H_numerator']
  coeff=list(map(F,larger['coefficients']));enorm=bil(coeff,G[sel]);energy=bil(coeff,A[sel])/enorm
  assert enorm>0 and enorm==F(larger['exact_norm']) and energy==F(larger['shifted_rayleigh_upper'])<fil<m1
  M5=den**5*r['B2'].T@A@r['B2'];assert M5.tolist()==larger['exact_integer_base_M5']
  assert len(rank)==larger['exact_gram_rank']==larger['proposed_basis_columns']==3*n+1
  assert larger['physical_spins']==2*nx*ny and larger['full_dimension']==4**(nx*ny)
  assert larger['retained_numerator_states']==1 and larger['max_triplet_number']==6 and larger['no_enlarged_trial_residual_claim'] and larger['no_base_M6_claim'] and larger['denominator_lower_bounds_unchanged']
  assert F(larger['energy_rayleigh_upper'])==energy-F(3*nx*ny,4)
  assert F(filtered['energy_rayleigh_upper'])==fil-F(3*nx*ny,4)
  out.append(dict(geometry=shape,g=str(g),physical_spins=2*nx*ny,full_Hilbert_dimension=str(4**(nx*ny)),original_rank=len(oldrank),enlarged_rank=len(rank),rank_pivots=piv,one_retained_numerator_state=True,old_G_A_J_and_M0_to_M4_exact=True,new_M5_exact=True,full_H3_exact=True,no_filtered_residual_certified=True,enlarged_upper=str(energy),enlarged_upper_display=float(energy),**filterinfo))
  print('PASS',shape,'rank',len(rank),'filter',float(fil),'enlarged',float(energy),flush=True)
 save('matrix_and_rayleigh_replay.json',out)
 return out
if __name__=='__main__':audit()
