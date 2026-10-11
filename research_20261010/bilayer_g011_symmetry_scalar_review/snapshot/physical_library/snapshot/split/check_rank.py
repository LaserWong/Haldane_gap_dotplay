import json,hashlib,time,resource,os
from pathlib import Path
from fractions import Fraction as F
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
p=Path(__file__).resolve().parent;src=p.parent/'third_moment_review';out=[];start=time.time()
def pivots(A):
 A=[[F(x) for x in row] for row in A];ps=[]
 for k in range(len(A)):
  a=A[k][k];assert a>=0
  if not a:assert all(x==0 for x in A[k][k:]);continue
  ps.append(str(a))
  for i in range(k+1,len(A)):
   for j in range(i,len(A)):
    A[i][j]-=A[i][k]*A[k][j]/a;A[j][i]=A[i][j]
 return ps
manifest=json.loads((src/'MANIFEST_SHA256.json').read_text());manifest=manifest.get('files',manifest)
for shape in ('4x4','8x4','8x8'):
 f=src/'results'/('geometry_'+shape+'.json');h=hashlib.sha256(f.read_bytes()).hexdigest();assert h==manifest['results/'+f.name]
 z=json.loads(f.read_text());n=z['orbits'];q4=[z['F'][i]+z['S'][i] for i in range(n)]+[[z['S'][j][i] for j in range(n)]+z['V'][i] for i in range(n)]
 a,b=pivots(q4),pivots(z['W']);assert len(a)==2*n and len(b)==n
 out.append(dict(shape=shape,source=str(f.relative_to(p.parent)),sha256=h,pair_orbits=n,base_rank=n+1,q4_rank=len(a),q6_rank=len(b),full_rank=1+n+len(a)+len(b),q4_positive_LDL_pivots=a,q6_positive_LDL_pivots=b,available_blocks=list(z.keys()),all_q4=z['all_q4'],all_q6=z['all_q6']))
(p/'rank_result.json').write_text(json.dumps(dict(status='EXACT_CACHED_GRAM_RANK_ONLY_NO_NEW_PHYSICAL_CONTRACTIONS',results=out,seconds=time.time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
print([(x['shape'],x['full_rank']) for x in out])
