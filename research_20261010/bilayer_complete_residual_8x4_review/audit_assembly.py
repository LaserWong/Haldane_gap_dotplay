"""Exact assembly from independent geometry and full physical q-sector contractions."""
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib
R=Path(__file__).resolve().parent;P=R.parent
rd=lambda p:json.loads(p.read_text())
def run():
 trial=rd(R/'snapshot/ground_8x4_trial.json')
 for path,digest in trial['source_sha256'].items():assert hashlib.sha256((P/path).read_bytes()).hexdigest()==digest,path
 gr=rd(P/'low_band/frontier_g007_g010/g1d10/block1_8x4_g1d10.json');geo=rd(P/'third_moment_review/results/geometry_8x4.json')
 res=rd(R/'independent_8x4.json');raw=rd(R/'snapshot/residual_8x4_origin.json')
 for key,value in res.items():
  if key!='seconds':assert value==raw[key],key
 c=trial['coefficients'];n=14;b=15;dim=43;d=gr['integer_matrix_denominator'];h=2
 assert d==40 and F(gr['coupling'])==F(1,10) and trial['selected_basis_indices']==list(range(dim))
 base=gr['shifted_integer_moments_M0_to_M4'];gb=base[0];ab=base[1]
 ff,ss,vv,ww,xx,yy,zz=[geo[k] for k in ['F','S','V','W','X','Y','Z']]
 G=[[0]*dim for _ in range(dim)];K=[[0]*dim for _ in range(dim)]
 for i in range(b):
  for j in range(b):G[i][j]=int(gb[i][j]);K[i][j]=int(ab[i][j])
 for i in range(n):
  for j in range(n):
   f,s,v,w,x,y,yt,z=map(int,[ff[i][j],ss[i][j],vv[i][j],ww[i][j],xx[i][j],yy[i][j],yy[j][i],zz[i][j]])
   G[b+i][b+j]=f;G[b+i][b+n+j]=G[b+n+j][b+i]=s;G[b+n+i][b+n+j]=v+w
   K[i+1][b+j]=K[b+j][i+1]=h*f;K[i+1][b+n+j]=K[b+n+j][i+1]=h*s
   K[b+i][b+j]=4*d*f+h*s;K[b+i][b+n+j]=K[b+n+j][b+i]=4*d*s+h*(v+w)
   K[b+n+i][b+n+j]=4*d*v+6*d*w+h*(x+y+yt+z)
 assert G==list(map(list,zip(*G))) and K==list(map(list,zip(*K)))
 mul=lambda A:[sum(x*y for x,y in zip(row,c)) for row in A]
 gc,kc=mul(G),mul(K);norm=sum(x*y for x,y in zip(c,gc));mean=F(sum(x*y for x,y in zip(c,kc)),d*norm)
 assert norm==int(trial['norm']) and mean==F(trial['rayleigh'])
 coeff=list(map(int,(R/'snapshot/ground_8x4_coefficients.txt').read_text().split()));assert coeff==[d,h]+c[1:]
 # B spans the complete invariant q0 plus q2 singlet space; its Gram is diagonal.
 assert all(gb[i][j]==0 for i in range(b) for j in range(b) if i!=j)
 sectors={'0':F(kc[0]**2,int(gb[0][0])),'2':sum((F(kc[i]**2,int(gb[i][i])) for i in range(1,b)),F(0)),'4':F(res['Tpsi_q4_norm']),'6':F(res['Tpsi_q6_norm']),'8':h*h*F(res['q8_creation_norm'])}
 second=sum(sectors.values())/(d*d*norm);variance=second-mean*mean;assert variance>0
 patch=rd(P/'low_band/combined_ground_bounds/combined/patch_8x4_g1d10.json');a=F(patch['global_lambda_kplus1_lower']);a1=F(patch['all_excited_global_lower']);assert a==F(trial['cutoff'])
 bins=patch['number_sector_bins']['bins'];offset=1
 for q,entry in enumerate(bins):
  assert entry['q']==q and entry['multiplicity']==math.comb(96+q-1,q) and entry['first_ordered_index']==offset;offset+=entry['multiplicity']
 assert offset>=2**64+1 and bins[2]['first_ordered_index']==98 and F(bins[1]['lower'])==a1 and F(bins[2]['lower'])==a
 odd=patch['blocks'][1];assert len(odd['eigen_upper'])==32 and odd['multiplicity']==3 and max(map(F,odd['eigen_upper']))<a
 assert mean<a1<a and patch['retained_full_band_dimension']==97
 lower=mean-variance/(a-mean);budget=F(trial['residual_squared_budget'])
 prod=rd(R/'snapshot/physical_result.json')
 assert str(norm)==prod['exact_norm'] and str(mean)==prod['shifted_rayleigh'] and str(second)==prod['exact_second_moment'] and str(variance)==prod['exact_variance'] and str(lower)==prod['ground_lower']
 assert {k:str(v) for k,v in sectors.items()}==prod['Tpsi_sector_norms']
 return dict(status='PASS_complete_positive_variance_and_sector_Temple',norm=str(norm),rayleigh=str(mean),sector_Tintpsi_norms={k:str(v) for k,v in sectors.items()},second_moment=str(second),variance=str(variance),variance_display=float(variance),cutoff=str(a),unique_global_ground_cutoff=str(a1),Temple_lower=str(lower),Temple_lower_display=float(lower),variance_budget=str(budget),meets_75percent_budget=variance<budget,q8_creation_norm=res['q8_creation_norm'],q6_M_zero_image_norm=res['Tpsi_q6_norm_on_M_zero_supports'],full_dimension=str(2**64),trial_dimension=43,retained_ground_states=1)
if __name__=='__main__':
 out=run();(R/'assembly_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
