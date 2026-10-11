import hashlib,json,itertools,math
from pathlib import Path
P=Path(__file__).resolve().parent;S=P/'snapshot/producer'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(p,h):
 assert sha(p)==h
 for f,v in json.loads(p.read_text()).items():assert sha(p.parent/f)==v,f
verify(S/'MANIFEST_SHA256.json','6e52c8fa916af036ab3d428d3999c5dd5bdf5b9e1125f5fca917b1c7616422d4')
verify(S/'ADDENDUM_SHA256.json','dfbc24dd08d4e3699cf68afa51c0522a3439fa00dcebcffc414ca68ca0d336b3')
for f,h in json.loads((S/'INPUT_SHA256.json').read_text()).items():assert sha(P.parent/f)==h,f
for f in ['geometry_4x2.txt','geometry_8x4.txt']:assert sha(P/'snapshot'/f)==sha(P.parent/'bilayer_complete_residual_8x4'/f)
def strip(d):return {k:v for k,v in d.items() if 'seconds' not in k and k!='peak_rss_kib'}
a=json.loads((P/'sample.json').read_text());b=json.loads((S/'sample_8x4.json').read_text());assert strip(a)==strip(b)
assert a['q6_processed']==129 and a['translation_anchor_checks']==774 and a['T_nonzero_M_zero_supports']==56
ranks={sum(math.comb(x-1,i) for i,x in enumerate(st,1)) for st in itertools.combinations(range(1,32),5)}
assert ranks==set(range(math.comb(31,5)))
def match(st):
 if not st:yield ();return
 i=st[0]
 for j in st[1:]:
  for rest in match(tuple(x for x in st if x not in (i,j))):yield ((i,j),)+rest
M=list(match(tuple(range(6))));canon=lambda pairs:tuple(sorted(tuple(sorted(p)) for p in pairs));M=list(map(canon,M));pranks=[]
for p in itertools.permutations(range(6)):
 r=0
 for i in range(6):r=r*(6-i)+sum(p[j]<p[i] for j in range(i+1,6))
 pranks.append(r);mapping=[M.index(canon([(p[i],p[j]) for i,j in m])) for m in M]
 assert sorted(mapping)==list(range(15))
 inv=[p.index(i) for i in range(6)]
 for m,k in zip(M,mapping):assert canon([(inv[i],inv[j]) for i,j in M[k]])==m
assert sorted(pranks)==list(range(720))
coeff=list(map(int,(S/'reference_coefficients.txt').read_text().split()));assert len(coeff)==28 and max(map(abs,coeff))<=2**48
B=2**84;bounds={'T':B,'DT':924*B,'KT':20172*B,'CT':5760*B,'U':(1200+11*924)*B}
assert all(v<2**127 for v in bounds.values());assert 28*2**31*2**48<B
projection=lambda d:d['r_cache_cpu_seconds']+d['q4_cpu_seconds']*4495/16+d['q6_cpu_seconds']*169911/129
out={'status':'PASS_FIXTURE_AND_CACHE_LOGIC','combinadic_ranks':len(ranks),'matching_permutations':720*15,'all_deterministic_sample_fields_equal':True,'coarse_channel_upper_bounds':{k:str(v) for k,v in bounds.items()},'producer_linear_projection_seconds':projection(b),'reviewer_instrumented_projection_seconds':projection(a),'projection_is_planning_estimate_only':True,'full_production_requires_separate_sector_normalization':True}
(P/(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'audit.json')).write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
