#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,os,resource
P=Path(__file__).resolve().parent;os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
sources=json.loads((P/'SOURCES.json').read_text());hashes={}
for entry in sources['sources']:
 p=P/'sources'/Path(entry['path']).name;b=p.read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==entry['blob']
 hashes[str(p.relative_to(P))]=hashlib.sha256(b).hexdigest()
transfer=(P/'sources/transfer.tex').read_text();model=(P/'sources/model.tex').read_text();intro=(P/'sources/introduction.tex').read_text()
assert '\\qquad(n\\ge4,\\ g\\in\\mathcal G).' in transfer
assert 'Z_n(b)=\\sum_i\\lambda_i(b)^n\\quad(n\\ge4).' in transfer
assert 'H_n(I)=H_n' in model
assert '\\frac4{105}\\log\\frac{80}{79}' in intro and '\\frac{\\log20}{784}' in intro
prior={}
for folder in ['uniform_cooled_seed_review','uniform_seed_frontier_review','uniform_transfer_moment_review']:
 p=P.parent/folder;manifest=json.loads((p/'MANIFEST_SHA256.json').read_text())
 for name,h in manifest.items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h
 prior[folder]=hashlib.sha256((p/'MANIFEST_SHA256.json').read_bytes()).hexdigest()
def log_ratio(x):
 z=(x-1)/(x+1);assert 0<=z<1
 N=100;s=2*sum(z**(2*j+1)/F(2*j+1) for j in range(N))
 remainder=2*z**(2*N+1)/(F(2*N+1)*(1-z*z))
 return s,s+remainder
la,ua=log_ratio(F(80,79));first=(F(4,105)*la,F(4,105)*ua)
l2,u2=log_ratio(F(2));l125,u125=log_ratio(F(5,4));second=((4*l2+l125)/784,(4*u2+u125)/784)
new=F(51,5000);comparisons=[]
for bounds,length in [(first,60),(second,2304)]:
 lo,hi=bounds;ratio=(new/hi,new/lo)
 comparisons.append({'original_even_L_at_least':length,'original_gap_interval':[str(lo),str(hi)],'original_gap_display':float(lo),'our_gap':str(new),'ratio_interval':[str(x) for x in ratio],'ratio_display':float(ratio[0])})
out={'status':'PASS source confirms untwisted all-integer transfer identity for n>=4; all-new-scopes>=52 unaffected','source_sha256':hashes,'verified_prior_review_manifests':prior,'comparisons':comparisons,'not_original_theorem':'0.005908566393 forL>=1920 is later archived reproduction','source_scope':'Original final theorem evenL; transfer proposition allintegern>=4; new signed interpolation supplies odd extension','source_floor_correction':'This supplement relies only on n>=4, not the broader n>=2 statement in earlier local notes'}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'comparisons':[{k:v for k,v in row.items() if 'interval' not in k} for row in comparisons]},indent=2))
