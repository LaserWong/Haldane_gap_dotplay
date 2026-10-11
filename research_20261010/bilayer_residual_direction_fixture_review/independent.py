import os,resource,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(min(30,resource.getrlimit(resource.RLIMIT_CPU)[0]) if resource.getrlimit(resource.RLIMIT_CPU)[0]>0 else 30,resource.getrlimit(resource.RLIMIT_CPU)[1]));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2));sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,itertools,json,time,hashlib
P=Path(__file__).resolve().parent;S=P/'snapshot';start=time.process_time()
spec=importlib.util.spec_from_file_location('cartesian',S/'accepted_cartesian.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
def main():
 assert hashlib.sha256((S/'CARTESIAN_MANIFEST.json').read_bytes()).hexdigest()=='47d717c90a183afde52fcf9b6dcd92fa246d9fa7619821af8fd703dd8310a589'
 assert hashlib.sha256((S/'accepted_cartesian.py').read_bytes()).hexdigest()==json.loads((S/'CARTESIAN_MANIFEST.json').read_text())['independent.py']
 assert C.local_physical_check();h=C.Model(4,2);classes={};orbs=[]
 for i,j in itertools.combinations(range(8),2):
  x,y=divmod(i,2);a,b=divmod(j,2);key=(min((x-a)%4,(a-x)%4),min((y-b)%2,(b-y)%2))
  if key not in classes:classes[key]=len(orbs);orbs.append([])
  orbs[classes[key]].append((i,j))
 assert len(orbs)==5
 B=[]
 for pairs in orbs:
  v={}
  for i,j in pairs:
   for c in (1,2,3):v[(c<<(2*i))|(c<<(2*j))]=1
  B.append(v)
 L=[h.op(b,'up') for b in B];R=[h.op(v,'D') for v in L];M=[h.op(v,'up') for v in L]
 T=C.add(*[(j+1,h.op(R[j],'up')) for j in range(5)],*[(((-1)**j)*(j+2),h.op(M[j],'D')) for j in range(5)])
 CT=h.op(T,'down');DT=h.op(T,'D');KT=C.add((1,h.op(h.op(T,'up'),'down')),(-1,h.op(CT,'up')));HT=h.H(T)
 export={}
 for line in (P/'small.vectors.txt').read_text().splitlines():
  a,*v=map(int,line.split());export[a]=v
 for state in set(export)|set(T)|set(CT)|set(DT)|set(KT):assert export.get(state,[0]*4)==[v.get(state,0) for v in (T,CT,DT,KT)]
 basis=[{0:1}]+B+L+R+M+[T];grades=[0]+[2]*5+[4]*10+[6]*6
 G=[];HH=[];JJ=[];A=[];A2=[];AT=C.add((1,HT),(-1200,T));assert all(v%11==0 for v in AT.values());AT={s:v//11 for s,v in AT.items()}
 for phi,q in zip(basis,grades):
  assert h.op(phi,'Q')=={s:q*v for s,v in phi.items()} if q else h.op(phi,'Q')=={}
  hp=h.H(phi);ap=C.add((1,hp),(-200*q,phi));assert all(v%11==0 for v in ap.values());ap={s:v//11 for s,v in ap.items()}
  G.append(C.inner(T,phi));HH.append(C.inner(T,hp));JJ.append(C.inner(HT,hp));A.append(C.inner(T,ap));A2.append(C.inner(AT,ap))
 for j,q in enumerate(grades):
  assert HH[j]==1200*G[j]+11*A[j]
  assert JJ[j]==1440000*G[j]+2200*(6+q)*A[j]+121*A2[j]
 prod=json.loads((S/'producer/fixture_4x2.json').read_text());fresh=json.loads((P/'small.json').read_text())
 for row,key in [(G,'G'),(HH,'H200'),(JJ,'H200_squared')]:assert row==list(map(int,prod[key]))==list(map(int,fresh[key]))
 norms=dict(T_norm=C.inner(T,T),CT_norm=C.inner(CT,CT),T_K_T=C.inner(T,KT),q8_creation_norm=C.inner(h.op(T,'up'),h.op(T,'up')))
 assert norms['q8_creation_norm']==norms['CT_norm']+norms['T_K_T']>0 and norms['T_K_T']<0
 for k,v in norms.items():assert v==int(prod[k])==int(fresh[k])
 out=dict(status='PASS_INDEPENDENT_FULL_CARTESIAN_T_AND_CROSS_MOMENTS',full_Hilbert_dimension=4**8,all_states_compared=True,vector_nonzero_counts={k:len(v) for k,v in [('T',T),('CT',CT),('DT',DT),('KT',KT)]},new_row_dimension=len(G),G=list(map(str,G)),H200=list(map(str,HH)),H200_squared=list(map(str,JJ)),A=list(map(str,A)),A_squared=list(map(str,A2)),coupling_polynomial_recovered_by_occupation=True,norms={k:str(v) for k,v in norms.items()},cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (P/'independent.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['cpu_seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
