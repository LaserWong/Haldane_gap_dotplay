"""Rigorous periodic MPS energy bounds from exact integer SU2 blocks, using Arb.
Prerequisite build_exact_mps.py verifies all highest-weight intertwining identities exactly.
No floating numerical eigensolver enters certification.
"""
import sys,json,time,argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'deps'))
from flint import arb,arb_mat,ctx
p=argparse.ArgumentParser();p.add_argument('--prefix',required=True);p.add_argument('--Ns',nargs='+',type=int,default=[128,256,512]);p.add_argument('--prec',type=int,default=256);p.add_argument('--a',default='4.76105');args=p.parse_args();ctx.prec=args.prec;ctx.threads=1
src=ROOT/(args.prefix+'_exact_blocks.txt');tokens=iter(src.read_text().split());nb=int(next(tokens));blocks=[];scale=0
for _ in range(nb):
 J=int(next(tokens));n=int(next(tokens));T=[[int(next(tokens)) for j in range(n)]for i in range(n)];O=[[int(next(tokens))for j in range(n)]for i in range(n)];scale=max(scale,max(abs(z).bit_length() for row in T for z in row));blocks.append((J,T,O))
scale=2**scale;U=[arb(0) for N in args.Ns];V=[arb(0)for N in args.Ns];tim=time.time()
for J,T,O in blocks:
 T=arb_mat(T)/scale;O=arb_mat(O)/(scale*scale);TT=T*T
 for k,N in enumerate(args.Ns):
  P=T**(N-2);U[k]+=(2*J+1)*(P*O).trace();V[k]+=(2*J+1)*(P*TT).trace()
 print('J',J,'dim',T.nrows(),'seconds',time.time()-tim,flush=True)
results=[]
for N,u,v in zip(args.Ns,U,V):
 energy=u/v;threshold=arb(args.a);passed=v>0 and energy < -threshold
 rec={'N':N,'energy_interval':energy.str(40),'norm_positive':bool(v>0),'threshold_a':args.a,'energy_less_than_minus_a':bool(passed),'precision_bits':args.prec};results.append(rec);print(rec,flush=True)
out={'method':'Arb ball matrix powers from exact integer highest-weight blocks','blocks_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'tensor_sha256':hashlib.sha256((ROOT/(args.prefix+'_integer_tensor.json')).read_bytes()).hexdigest(),'seconds':time.time()-tim,'results':results}
(ROOT/(args.prefix+'_arb_certificate.json')).write_text(json.dumps(out,indent=2))
if not all(r['energy_less_than_minus_a'] for r in results):sys.exit(1)
