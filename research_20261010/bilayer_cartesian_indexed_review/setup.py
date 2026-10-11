from pathlib import Path
import json,hashlib
p=Path(__file__).parent;s=p.parent/'bilayer_cartesian_indexed_sample';old=p.parent/'bilayer_connected_rule_compiler_review'
assert hashlib.sha256((s/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='760ab0e980cc40bd96028da1bc626353c44f463148d5dd2bc6cef81db566d1bd'
for f,h in json.loads((s/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((s/f).read_bytes()).hexdigest()==h,f
for f,h in json.loads((s/'INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((s.parent/f).read_bytes()).hexdigest()==h,f
# Independent exact Cartesian table.
t=[]
for op in range(3):
 for src in range(16):
  a,b=src%4,src//4;v=[0]*16
  if op==0:
   if a and a==b:v[0]=1
  elif op==1:
   if not a and not b:
    for c in range(1,4):v[5*c]=1
  elif bool(a)!=bool(b):v[b+4*a]=1
  elif a and b:
   v[b+4*a]+=1
   if a==b:
    for c in range(1,4):v[5*c]-=1
  t+=v
(p/'edge_table.txt').write_text(' '.join(map(str,t)))
(p/'independent.cpp').write_bytes((old/'independent.cpp').read_bytes())
(p/'cartesian_fixture.cpp').write_bytes((old/'cartesian_fixture.cpp').read_bytes())
x=(s/'benchmark.cpp').read_text().replace('#include "validate.cpp"',f'#include "{s}/validate.cpp"').replace('int main(int argc,char**argv)','int producer_main(int argc,char**argv)')
(p/'producer_adapter.cpp').write_text(x)
print('All current manifest and input hashes PASS')
