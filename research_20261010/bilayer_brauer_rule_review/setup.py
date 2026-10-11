from pathlib import Path
import json,hashlib
p=Path(__file__).parent;s=p.parent/'bilayer_brauer_rule_compiler';prev=p.parent/'bilayer_cartesian_indexed_review'
assert hashlib.sha256((s/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='7eeb2e2c2adbfe000471c64e464fbf2b74becbd218ec4e1b4e7245472f72f6ec'
for f,h in json.loads((s/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((s/f).read_bytes()).hexdigest()==h,f
for f,h in json.loads((s/'INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((s.parent/f).read_bytes()).hexdigest()==h,f
x=(s/'brauer.cpp').read_text().replace('#include "reference/cartesian_reference.cpp"',f'#include "{s}/reference/cartesian_reference.cpp"').replace('int main(int argc,char**argv)','int producer_main(int argc,char**argv)')
(p/'brauer_adapter.cpp').write_text(x)
a=(prev/'action.cpp').read_text();a=a.replace('#include "producer_adapter.cpp"','#include "brauer_adapter.cpp"');a=a[:a.index('int main(')]
(p/'action.cpp').write_text(a)
print('All source and input hashes pass.')
