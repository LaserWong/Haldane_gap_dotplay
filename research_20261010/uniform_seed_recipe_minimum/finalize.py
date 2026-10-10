#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[1];d=json.loads((P/'results.json').read_text());B=10**24
up=lambda x:F(-(-x.numerator*B//x.denominator),B)
G=lambda z:1-(1-z)**2/(2*z*z)
expected={(n,ell) for n in (48,50) for ell in range(10,n+1,2)}
assert d['selected_n']==[48,50] and d['selected_ell'] is None and {(v['n'],v['ell']) for v in d['families']}==expected and len(d['families'])==len(expected)
leaves_count=0;max_round=0;failtypes={}
for rec in d['families']:
 leaves=rec['closed_interval_leaves'];assert F(leaves[0]['r_lower'])==1 and F(leaves[-1]['r_upper'])==16 and all(a['r_upper']==b['r_lower'] for a,b in zip(leaves,leaves[1:]));assert F(rec['cold_D_over_t_lower'])>4 and F(rec['cold_S_upper'])==F(1,16) and G(F(1,256))<0
 for leaf in leaves:
  s,t=F(leaf['S_upper']),F(leaf['T_upper']);assert 0<s<=1 and 0<t<=1;hist=leaf['failure']['history'];assert hist
  for j,h in enumerate(hist):
   if j%2==0:
    assert min(s,t)<F(99,100);kind='spatial';arg=s*s*t;out=up(G(arg));s=out
   else:kind='thermal';arg=t*t*s;out=up(G(arg));t=out
   assert 0<arg<=1 and kind==h['kind'] and str(arg)==h['argument_upper'] and str(out)==h['output_upper']
   assert (out<=0)==(j==len(hist)-1)
  assert leaf['failure']['kind']==hist[-1]['kind'] and leaf['failure']['round']==(len(hist)+1)//2
  max_round=max(max_round,leaf['failure']['round']);failtypes[leaf['failure']['kind']]=failtypes.get(leaf['failure']['kind'],0)+1;leaves_count+=1
assert leaves_count==d['leaf_count']
rev=P.parent/'uniform_anchor96_100_review';raw=(rev/'MANIFEST_SHA256.json').read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='99317ea99db7892f33852e6a0b12b9aa4d3825527852ff605d7d86f22d3f22d7';mf=json.loads(raw);assert all(hashlib.sha256((rev/name).read_bytes()).hexdigest()==h for name,h in mf.items());v=json.loads((rev/'CLAIM_VERDICTS.json').read_text());assert v['status']=='ACCEPTED independent physical anchors only' and v['lengths']==[96,100]
d['anchor_review_status']='ACCEPTED in separate uniform_anchor96_100_review';d['anchor_review_manifest_sha256']=sha;d['scalar_review_status']='PRODUCER COMPLETE; independent scalar review pending';d['terminal_failure_summary']={'all_leaf_paths_end_with_nonpositive_G':True,'finite_round_cap_failures_accepted':0,'target_entry_paths_accepted_as_failures':0,'maximum_recorded_failure_round':max_round,'failure_types':failtypes}
(P/'results.json').write_text(json.dumps(d,indent=2)+'\n');inputs=json.loads((P/'INPUT_SHA256.json').read_text());inputs[str((rev/'MANIFEST_SHA256.json').relative_to(ROOT))]=sha;inputs[str((rev/'CLAIM_VERDICTS.json').relative_to(ROOT))]=hashlib.sha256((rev/'CLAIM_VERDICTS.json').read_bytes()).hexdigest();(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
summary={'status':'PASS exact saved-history verification; new scalar exclusion pending independent review','families':len(expected),'closed_interval_leaves':leaves_count,**d['terminal_failure_summary'],'cpu_seconds_main_certificate':d['cpu_seconds'],'anchor_review_manifest_sha256':sha}
(P/'FINAL_CHECK.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
