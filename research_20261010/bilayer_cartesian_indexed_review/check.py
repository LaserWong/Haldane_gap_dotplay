from pathlib import Path
from collections import defaultdict,Counter
import json,struct,math
p=Path(__file__).parent;s=p.parent/'bilayer_cartesian_indexed_sample'
# All arithmetic below is integer (complex values have integral components of magnitude far below 2**53).
r=[[0,1,-1,0],[-1,0,0,1],[1j,0,0,1j],[0,1,1,0]]
B=[[r[a][x]*r[b][y] for y in range(4) for x in range(4)] for b in range(4) for a in range(4)]
t=list(map(int,(p/'edge_table.txt').read_text().split()))
for col in range(16):
 z=[0]*16
 for i,v in enumerate(B[col]):
  for a,b in [(0,2),(1,3)]:z[i^((((i>>a)^(i>>b))&1)*((1<<a)|(1<<b)))]+=v
  z[i]-=v
 for row in range(16):
  got=sum(complex(B[row][i]).conjugate()*z[i] for i in range(16))
  want=4*sum(t[op*256+col*16+row] for op in range(3));assert got==want
for fam in 'NFL':
 blocks=defaultdict(dict)
 for mask,a,b,c in struct.iter_unpack('<IHHi',(s/f'run/rules_{fam}.bin').read_bytes()):blocks[mask][a,b]=c
 hist=Counter()
 for mask,m in blocks.items():
  sites=[i for i in range(32) if mask>>i&1];summed=defaultdict(int);stabs=[]
  for tr in range(32):
   shifted=[((i//4+tr//4)%8)*4+(i%4+tr%4)%4 for i in sites]
   if set(shifted)==set(sites):stabs.append([sites.index(i) for i in shifted])
  hist[len(stabs)]+=1
  if fam!='N':
   for perm in stabs:
    def shift(x):return sum(((x>>(2*i))&3)<<(2*j) for i,j in enumerate(perm))
    for (a,b),c in m.items():summed[shift(a),shift(b)]+=c
   assert all(summed.get((b,a),0)==c for (a,b),c in summed.items())
 print(fam,'stabilizers',dict(hist),'Hermiticity checked' if fam!='N' else '')
ref=list(map(int,(s/'reference_coefficients.txt').read_text().split()));w=json.loads((p.parent/'bilayer_split_pencil_optimization/result.json').read_text())['results'][0]
assert w['shape']==[8,4] and w['g']=='11/100' and ref[14:]==w['integer_coefficients'][-14:]
for n in (4,5):
 for k in ('fixture','terms'):
  f=f'{k}_{n}x2.json';a=json.loads((s/'run'/f).read_text());b=json.loads((p/'fixtures'/f).read_text());a.pop('peak_sparse_states',None);b.pop('peak_sparse_states',None);assert a==b
rows=[json.loads(x) for x in (s/'run/sample.jsonl').read_text().splitlines()]
for fam in 'NFL':
 rr=[x for x in rows if x['family']==fam];assert len(rr)==512 and len({x['mask'] for x in rr})==512
 for j,x in enumerate(rr):
  sites=[i for i in range(32) if x['mask']>>i&1];assert len(sites)==6 and sites[0]==0
  assert sum(math.comb(a-1,k) for k,a in enumerate(sites[1:],1))==j*169910//511
 assert Counter(x['occupied_edges'] for x in rr)=={0:55,1:131,2:176,3:111,4:28,5:9,6:1,7:1}
summary=json.loads((s/'run/summary.json').read_text());projection=sum(x['sample_cpu_seconds'] for x in summary['families'])/512*169911
print('All exact edge entries, 15-term fixtures, witness bindings and dispersed sample ranks PASS; empirical projection',projection)
raw=sum(math.comb(5,q)**2*math.prod(range(1,2*q,2)) for q in range(6));assert raw==5396
assert 12816*16*3**15<2**42
print('Brauer proposal key ceiling and conservative integer bound verified; no diagram compiler or action executed.')
