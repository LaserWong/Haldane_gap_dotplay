import os,json,sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paths import audit_copy
os.environ['AUDIT_DIGITS']='140'
D=str(audit_copy() / 'research_20261010') + '/'
src=open(D+'uniform_smaller_second_initialization_review/audit_scalar.py').read()
exec(src.split("producer_hash=")[0].replace("os.sched_setaffinity(0,{0});","").replace("P=Path(__file__).resolve().parent","P=Path('"+D+"uniform_smaller_second_initialization_review')"))
from fractions import Fraction as F
tag=os.environ['TAG'];gap=F(os.environ['GAP']);beta=F(49,4);E=exp_upper(beta*gap)
A=D+'uniform_gap_0248_all_sizes/'
c=json.load(open(A+'certificate.json'));c['gap']=str(gap);c['combined_claim']['gap']=str(gap)
for r in c['new_rows']:
  cc=F(r['purity_lower']);m=down(cc-E*(1-cc));assert m>0;r['gap']=str(gap);r['margin']=str(m)
p=json.load(open(A+'cached_prefix.json'))
for r in p['rows']:
  cc=F(r['purity']);m=down(cc-E*(1-cc));assert m>0;r['gap']=str(gap);r['margin']=str(m)
json.dump(c,open(A+f'certificate_{tag}.json','w'),indent=1);json.dump(p,open(A+f'cached_prefix_{tag}.json','w'),indent=1);print('ok',tag)
