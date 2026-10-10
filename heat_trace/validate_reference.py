#!/usr/bin/env python3
"""Independent original dense-vs-streamed bitwise comparison on small cases.

The archived source is read, never edited. Its function is instrumented in
memory solely to return its integer total before the printed scalar enclosure.
"""
import hashlib,json,resource,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=ROOT.parent/'upstream/extracted/cases/haldane_reference_audit/thermal_small_exact.py'
if not src.exists():src=ROOT/'reference_sources/cases/haldane_reference_audit/thermal_small_exact.py'
text=src.read_text();needle="    b=F(21,2) if isa else F(49,4)"
assert text.count(needle)==1
scope={'__name__':'reference_in_memory'}
exec(compile(text.replace(needle,'    return total\n'+needle),str(src),'exec'),scope)
results=[]
for twist in ('I','P','C'):
    start=time.monotonic();total=scope['thermal'](6,twist,'A');elapsed=time.monotonic()-start
    streamed=json.loads((ROOT/'results'/f'A_L6_{twist}_none/certificate.json').read_text())
    assert total==int(streamed['total_squared_integer_norm'])
    row={'L':6,'twist':twist,'reference_total':str(total),'bitwise_equal':True,'reference_seconds':elapsed}
    results.append(row);print(json.dumps(row),flush=True)
report={'scope':'Three Appendix A L6 physical all-column reconstructions; not Appendix B',
        'original_source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'results':results,
        'max_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(ROOT/'reference_validation.json').write_text(json.dumps(report,indent=2)+'\n')
