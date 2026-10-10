"""Independent exact moment-pencil audit. No producer module is imported.
All physical input matrices are accepted only by hashes from sealed prior reviews.
Rational Schur complements and direct polynomial witnesses independently accept.
"""
from independent_math import *
from verify_inputs import check_hashes
from independent_scalar import number_bins
import time,copy
HERE=Path(__file__).resolve().parent;SRC=HERE/'snapshot';COMP=SRC/'low_band/ground_moment_pencil';OUT=HERE/'results'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def inertia(matrix):
 # Ordinary exact rational Schur complements, not producer fraction-free inertia.
 a=[[F(v) for v in row] for row in matrix];negative=positive=0
 assert all(len(r)==len(a) for r in a) and all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a)))
 while a:
  n=len(a);i=next((i for i in range(n) if a[i][i]),None)
  if i is None:
   pair=next(((i,j) for i in range(n) for j in range(i+1,n) if a[i][j]),None)
   if pair is None:return [negative,n,positive]
   i,j=pair
   for k in range(n):a[i][k]+=a[j][k]
   for k in range(n):a[k][i]+=a[k][j]
  a[0],a[i]=a[i],a[0]
  for row in a:row[0],row[i]=row[i],row[0]
  p=a[0][0];negative+=p<0;positive+=p>0
  a=[[a[i][j]-a[i][0]*a[0][j]/p for j in range(1,n)] for i in range(1,n)]
 return [negative,0,positive]

def combine(*terms):
 n=len(terms[0][1]);return [[sum((c*M[i][j] for c,M in terms),F(0)) for j in range(n)] for i in range(n)]
def quadratic(v,M):return sum((v[i]*M[i][j]*v[j] for i in range(len(v)) for j in range(len(v))),F(0))

def one(grpath,check_inertias=True):
 rec=load(grpath);nx,ny,n,g=rec['nx'],rec['ny'],rec['N'],F(rec['g']);assert n==nx*ny
 deps=rec['source_sha256'];assert len(deps)==3
 for path,h in deps.items():assert sha(SRC/path)==h
 ground=load(SRC/next(p for p in deps if Path(p).name.startswith('block1_')))
 bins=load(SRC/next(p for p in deps if Path(p).name.startswith('quadratic_bins_')))
 old=load(SRC/next(p for p in deps if Path(p).name.startswith('temple_')))
 G=ground['gram'];Knum=ground['shifted_hamiltonian_numerator'];Jnum=ground['shifted_H2_numerator'];d=ground['integer_matrix_denominator'];m=len(G)
 assert type(d) is int and d>0 and m==({(4,4):11,(8,4):29,(8,8):29}[(nx,ny)])
 assert all(type(v) is int for M in [G,Knum,Jnum] for r in M for v in r)
 assert all(len(M)==m and all(len(r)==m for r in M) and all(M[i][j]==M[j][i] for i in range(m) for j in range(m)) for M in [G,Knum,Jnum])
 # No fixed-width integer products: denominator d^2 is a Python arbitrary integer.
 A=combine((F(1,d),Knum));B=combine((F(1,d*d),Jnum));c=ground['coefficients'];norm=quadratic(c,G);assert norm>0
 rho=quadratic(c,A)/norm;r2=quadratic(c,B)/norm-rho*rho
 assert rho==F(ground['exact_rayleigh'])-F(ground['E00'])==F(rec['ground_upper']) and r2==F(ground['exact_residual_squared'])>=0
 assert F(rec['energy_shift'])==F(ground['E00'])==-F(3*n,4)
 (a0,a1,a),counts=number_bins(bins,'quadratic')
 assert rho<a1<a and bins['bins'][2]['first_ordered_index']==2+3*n
 assert old['blocks'][0]['k']==old['blocks'][0]['multiplicity']==1
 assert old['blocks'][1]['k']==n and old['blocks'][1]['multiplicity']==3 and len(old['blocks'][1]['eigen_upper'])==n
 assert max(map(F,old['blocks'][1]['eigen_upper']))<a==F(old['global_lambda_kplus1_lower'])
 assert old['retained_full_band_dimension']==1+3*n and old['full_hilbert_dimension']==4**n
 assert F(rec['whole_band_count_cutoff_margin'])==a-max(map(F,old['blocks'][1]['eigen_upper']))>0
 pencil=rec['pencil'];assert pencil['external_low_count_required']==1 and pencil['trial_dimension']==m and F(pencil['external_cutoff'])==a
 assert len(pencil['endpoints'])==1 and pencil['negative_inverse_ritz_count']==1
 ep=pencil['endpoints'][0];l=F(ep['lower']);u=F(ep['optimal_pencil_endpoint_upper']);oldl=F(old['blocks'][0]['eigen_lower'][0])
 assert ep['sector_eigenvalue_index_one_based']==1 and oldl<l<=rho<a and l<u<a and u-l==F(ep['pencil_root_bracket_width'])
 shift=combine((1,A),(-a,G));square=combine((1,B),(-2*a,A),(a*a,G))
 endpoint=combine((1,B),(-(a+l),A),(a*l,G));upper=combine((1,B),(-(a+u),A),(a*u,G))
 witness=ep['negative_direction_witness'];v=witness['coefficients'];assert len(v)==m and all(type(x) is int for x in v)
 q=quadratic(v,endpoint);assert q==F(witness['exact_endpoint_quadratic_form'])<0
 # Cross-check the acceptance polynomial using only three integer quadratic forms.
 vg,va,vb=[quadratic(v,M) for M in [G,Knum,Jnum]]
 integer_polynomial=F(vb,d*d)-(a+l)*F(va,d)+a*l*vg
 assert q==integer_polynomial and vg>0
 matrices=[G,shift,square,endpoint,upper];expected=[[0,0,m],[1,0,m-1],[0,0,m],[1,0,m-1],[0,0,m]]
 verified=[inertia(M) for M in matrices] if check_inertias else None
 if check_inertias:assert verified==expected
 if check_inertias:assert verified==[pencil['gram_inertia'],pencil['cutoff_ritz_inertia'],pencil['shifted_squared_moment_inertia'],ep['endpoint_pencil_inertia'],ep['upper_pencil_inertia']]
 assert rec['ground_trial_dimension']==m and rec['retained_ground_states']==1 and rec['physical_spin_count']==2*n and rec['full_hilbert_dimension']==4**n
 assert l==F(rec['ground_lower']) and oldl==F(rec['old_ground_lower'])
 assert [rho-oldl,rho-l,l-oldl]==[F(rec[k]) for k in ['old_ground_width','ground_width','improvement']]
 tag=f'{nx}x{ny}_g{g}'.replace('/','d');patched=load(COMP/f'temple_{tag}.json')
 expectedpatch=copy.deepcopy(old)
 for key in ['status','method','ground_width','ground_moment_pencil_source','ground_moment_pencil_source_sha256']:
  expectedpatch[key]=patched[key]
 expectedpatch['blocks'][0]['previous_eigen_lower']=expectedpatch['blocks'][0]['eigen_lower'][:]
 expectedpatch['blocks'][0]['eigen_lower']=[str(l)]
 assert expectedpatch==patched,'Unexpected changes outside declared ground endpoint metadata'
 assert patched['ground_moment_pencil_source']==grpath.name and patched['ground_moment_pencil_source_sha256']==sha(grpath)
 assert F(patched['ground_width'])==rho-l
 return dict(g=str(g),shape=f'{nx}x{ny}',d=d,trial_dimension=m,retained_ground_states=1,retained_complete_band=1+3*n,physical_spin_count=2*n,full_hilbert_dimension=4**n,
   ground_lower=str(l),ground_upper=str(rho),old_lower=str(oldl),width=str(rho-l),improvement=str(l-oldl),inertias=verified,
   exact_negative_quadratic_form=str(q),negative_form_per_trial_norm=str(q/vg),external_cutoff=str(a),global_ground_identification_margin=str(a1-rho),external_triplet_count_margin=str(a-max(map(F,old['blocks'][1]['eigen_upper']))),
   exact_polynomial_acceptance=True,integer_normalization_verified=True,full_H2_sealed_physical_dependency=True,external_even_sector_count=1,source_sha256=deps)

def synthetic():
 # Exact prescribed spectra make cutoff, leakage, rank and count issues explicit.
 rows=[]
 for k in [1,2,3]:
  energies=[F(-k+i) for i in range(k)]+[F(0),F(2),F(5)]
  n=len(energies);m=k+2;W=[[F(0) for _ in range(m)] for _ in range(n)]
  for j in range(k):W[j][j]=1
  W[k][k]=W[k][k+1]=1;W[k+1][k]=1;W[k+2][k+1]=1
  G=[[sum(W[t][i]*W[t][j] for t in range(n)) for j in range(m)] for i in range(m)]
  A=[[sum(W[t][i]*energies[t]*W[t][j] for t in range(n)) for j in range(m)] for i in range(m)]
  B=[[sum(W[t][i]*energies[t]**2*W[t][j] for t in range(n)) for j in range(m)] for i in range(m)]
  assert inertia(G)==inertia(B)==[0,0,m] and inertia(A)==[k,0,m-k]
  for j in range(1,k+1):
   l=energies[k-j]-F(1,10);mat=combine((1,B),(-l,A))
   assert inertia(mat)[0]==j
  rows.append(dict(k=k,m=m,cutoff_eigenvalue_present=True,strict_endpoint_inertias_valid=True))
 # Ground polynomial remains valid even when a cutoff eigenvector makes S singular.
 assert inertia([[1,0],[0,0]])==[0,1,1]
 assert quadratic([1,0],[[-F(1,10),0],[0,0]])<0
 # Wrong k=1: visible state -1 would give l=-11/10 although hidden ground is -2.
 l=-F(11,10);assert (-1)*(-1-l)<0 and F(-2)<l
 # A trial with leakage, m>1 and full B: W0=e_ground+e_high/10.
 theta=F(-3)+F(2,100);second=F(9)+F(4,100);norm=F(101,100);a=0
 l=second/theta-F(1,100);assert l<-3 and second-l*theta<0
 return dict(status='PASS independent exact theorem regression cases',cases=rows,cutoff_singular_S_direct_test_valid=True,missing_external_count_counterexample_verified=True,nonzero_leakage_full_second_moment_verified=True)

def main():
 start=time.monotonic();check_hashes();(OUT/'synthetic_review.json').write_text(json.dumps(synthetic(),indent=2)+'\n');rows=[]
 for g in map(F,['3/100','1/25','1/20','3/50','7/100','2/25','1/10']):
  for nx,ny in [(4,4),(8,4),(8,8)]:
   p=COMP/f'ground_{nx}x{ny}_g{g}.json'.replace('/','d');r=one(p);rows.append(r)
   (OUT/'ground_review.json').write_text(json.dumps(rows,indent=2)+'\n')
   print('PASS exact ground',g,r['shape'],'m',r['trial_dimension'],'width',float(F(r['width'])),flush=True)
 summary=load(COMP/'ground_summary.json');assert summary['patches']==[load(COMP/f'ground_{r["shape"]}_g{r["g"]}.json'.replace('/','d')) for r in rows]
 check_hashes();(OUT/'ground_summary.json').write_text(json.dumps(dict(status='PASS independent full-ground moment certificate audit',patches=len(rows),exact_negative_witnesses=21,independent_inertias=105,seconds=time.monotonic()-start,maximum_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
 print('PASS ALL 21 PHYSICAL ENDPOINTS',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
