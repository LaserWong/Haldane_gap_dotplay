from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,hashlib,time,resource
P=Path(__file__).resolve().parent;R=P.parents[1];start=time.process_time();src=P.parent/'uniform_n24_second_coverage/certify.py';spec=importlib.util.spec_from_file_location('arithmetic',src);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);gap=F(31,1250);beta=F(49,4);e=c.expi(beta*gap)[1];rows=[];inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p.relative_to(R))]=hashlib.sha256(b).hexdigest();return json.loads(b)
for name,h in [('uniform_small_lengths_completion','71606fa80898fb73b6f0fffb359480a1d3e716d98c47791d16d3470618c4af08'),('uniform_n24_second_coverage','ef04180cedde73a09aa627c3dc75c2730472c9f425fd29bcec376678fea00240'),('uniform_direct25_coverage','abd4e0f0a315ef9878129c56ee884d797707687f07361c83f1cb140f0ebee9fa')]:
 m=P.parent/name/'MANIFEST_SHA256.json';b=m.read_bytes();inputs[str(m.relative_to(R))]=hashlib.sha256(b).hexdigest();assert inputs[str(m.relative_to(R))]==h
x=read(P.parent/'uniform_small_lengths_completion/certificate.json')
for q in x['rows']:
 L=q['L'];C=F(q['purity_lower']);margin=C-e*(1-C);rows.append({'L':L,'purity':str(C),'gap':str(gap),'margin':str(margin),'passed':margin>0})
x=read(P.parent/'uniform_n24_second_coverage/length_resolved_certificate.json');q=next(v for v in x['rows'] if v['L']==24);C=F(q['purity_lower']);margin=C-e*(1-C);rows.append({'L':24,'purity':str(C),'gap':str(gap),'margin':str(margin),'passed':margin>0})
x=read(P.parent/'uniform_direct25_coverage/certificate.json');C=F(x['purity_lower']);margin=C-e*(1-C);rows.append({'L':25,'purity':str(C),'gap':str(gap),'margin':str(margin),'passed':margin>0})
out={'status':'EXACT_CACHED_PREFIX_PASS' if all(r['passed'] for r in rows) else 'FAILED_BOUND','gap':str(gap),'rows':rows,'bottleneck':min(rows,key=lambda x:F(x['purity'])),'resources':{'cpu_seconds':time.process_time()-start,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'cached_prefix.json').write_text(json.dumps(out,indent=2)+'\n');(P/'PREFIX_INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n');print(out['status'],'bottleneck',out['bottleneck']['L'],float(F(out['bottleneck']['purity'])),float(F(out['bottleneck']['margin'])));print(out['resources'])
