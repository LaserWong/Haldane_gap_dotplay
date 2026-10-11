#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,hashlib,time,resource
P=Path(__file__).resolve().parent;ROOT=P.parents[1];start=time.process_time();src=P.parent/'uniform_n24_second_coverage/certify.py';spec=importlib.util.spec_from_file_location('arithmetic',src);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def pin(name,expected):
 assert hashlib.sha256(read(P.parent/name/'MANIFEST_SHA256.json')).hexdigest()==expected
pin('uniform_smaller_second_initialization','fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84');pin('uniform_smaller_second_initialization_review','54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f');pin('uniform_small_lengths_completion','71606fa80898fb73b6f0fffb359480a1d3e716d98c47791d16d3470618c4af08')
ints={k:int(v) for line in read(P/'anchors.out').decode().splitlines() for k,v in [line.split('=')]};gap=F(31,1250);beta=F(49,4);e=c.expi(beta*gap)[1];rows=[]
def Q(n):
 assert n%2==0;return c.sector('J',n)+3*c.sector('N',n)
for L in range(26,34):
 N=ints[f'N0_{L}'];H=ints[f'H0_{L}'];assert N>0;R=F(H,N)+L*F(700741,500000)
 if L%2:den=Q(L-1)*Q(L+1);method='CAUCHY_SCHWARZ_EVEN_NEIGHBORS';trace_inputs={str(L-1):str(Q(L-1)),str(L+1):str(Q(L+1))}
 else:den=Q(L)**2;method='EVEN_MOMENT_UPPER';trace_inputs={str(L):str(Q(L))}
 assert den>0;num=c.expi(-2*beta*R)[0];C=c.down(num/den);assert C<=1;margin=C-e*(1-C);passed=C>F(1,2) and margin>0
 rows.append({'L':L,'norm_positive':True,'shifted_total_Rayleigh':str(R),'trace_method':method,'trace_inputs':trace_inputs,'trace_squared_upper':str(den),'numerator_lower':str(num),'purity_lower':str(C),'gap':str(gap),'margin':str(margin),'passed':passed});print(L,'R',float(R),'C',float(C),'margin',float(margin),'PASS' if passed else 'FAILED_BOUND',flush=True)
prefix=json.loads(read(P/'cached_prefix.json'));assert len(prefix['rows'])==22 and {x['L'] for x in prefix['rows']}==set(range(4,26))
for r in prefix['rows']:
 C=F(r['purity']);assert F(r['gap'])==gap and r['passed'] and F(r['margin'])==C-e*(1-C) and F(r['margin'])>0
old=json.loads(read(P.parent/'uniform_smaller_second_initialization/certificate.json'));seed=next(x for x in old['rows'] if x['n']==34);assert seed['status']=='PASS_PRODUCER' and F(seed['gap'])==gap and seed['all_integer_L_at_least']==34
small=json.loads(read(P.parent/'uniform_small_lengths_completion/certificate.json'));analytic=small['analytic_small_lengths'];assert F(analytic['2']['gap'])>=gap and F(analytic['3']['gap'])>=gap and analytic['2']['ground_multiplicity']==analytic['3']['ground_multiplicity']==1
holes=[r['L'] for r in rows if not r['passed']];guard=json.loads(read(P/'guard_resources.json'));assert guard['exit_code']==0 and not guard['wall_watchdog_fired'] and guard['wall_seconds']<25 and guard['wait4_total_cpu_seconds']<=30 and guard['wait4_maxrss_kib']<=100*1024
for dep in [src,P/'contract_prefix.cpp',P/'run_guarded.py',P.parent/'uniform_smaller_second_initialization/long_certificate.json',P.parent/'uniform_second_moment_optimization/certificate.json',ROOT/'audit/mps/mps_blocks.txt',ROOT/'audit/APPENDIX_A_BRIDGE.md']:read(dep)
claim={'all_integer_L_at_least':2,'gap':str(gap),'unique_ground_state':True,'coverage_onset':2,'bootstrap_initialization_used_for_this_stronger_gap':34,'smallest_separately_certified_initialization':30,'union':['analytic2,3','cached direct/parity4..25 rechecked at.0248','own direct thermal26..33','accepted n34 tail.0248']} if not holes else None
out={'status':'EXACT_PRODUCER_ALL_SIZE_STRENGTHENING_PASS_REVIEW_REQUIRED' if not holes else 'PARTIAL_FAILED_BOUNDS','beta':str(beta),'gap':str(gap),'new_rows':rows,'cached_prefix_passed':True,'failed_bound_lengths':holes,'combined_claim':claim,'resources':{'cpu_seconds':time.process_time()-start,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'certificate.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n');print(out['status'],claim);print(out['resources'])
