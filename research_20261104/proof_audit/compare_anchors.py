import json,re
from fractions import Fraction as F
R='/workspace/repos/Haldane_gap_dotplay/research_20261010/'
files=['uniform_small_lengths_completion_review/anchors.out','uniform_direct25_coverage_review/anchor25.out','uniform_gap_0248_all_sizes/anchors.out','uniform_smaller_second_initialization/anchors.out','uniform_smaller_second_initialization/anchor60.out','uniform_n28_second_initialization_review/anchor48.out']
ref={}
for f in files:
    for line in open(R+f):
        m=re.match(r'(H0|N0)_(\d+)=(-?\d+)',line.strip())
        if m: ref.setdefault(int(m[2]),{})[m[1]]=int(m[3])
mine={int(k):(int(a),int(b)) for k,(a,b) in json.load(open('mps_anchor_values.json')).items()}
a=F(700741,500000);out={}
for L in sorted(ref):
    H,N=mine[L]; ok=(ref[L]['H0']==H and ref[L]['N0']==N)
    R_L=F(H,N)+L*a
    out[L]={'match':ok,'R_L_float':float(R_L)}
    print(L,'MATCH' if ok else 'MISMATCH',N>0,'%.10g'%float(R_L))
assert all(v['match'] for v in out.values())
json.dump(out,open('compare_anchors.json','w'),indent=1)
print('ALL',len(out),'anchors match exactly')
