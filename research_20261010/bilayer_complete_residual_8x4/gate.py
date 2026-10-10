import json,math,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent;r=json.loads((p/'benchmark_8x4_1000.json').read_text())
projection=r['cache_seconds']+r['q4_seconds']*r['q4_total']/r['q4_processed']+r['q6_seconds']*r['q6_total']/r['q6_processed']
safe=projection*10
out=dict(benchmark=r,linear_seconds=projection,tenfold_seconds=safe,cpu_budget_seconds=600,memory_budget_kib=700*1024,address_space_limit_bytes=1024**3,gate_passed=safe<600 and r['peak_rss_kib']<700*1024,no_q8_enumeration=True,source_sha256=hashlib.sha256((p/'residual_scalar.cpp').read_bytes()).hexdigest())
(p/'benchmark_gate.json').write_text(json.dumps(out,indent=2)+'\n');assert out['gate_passed'];print(json.dumps(out,indent=2))
