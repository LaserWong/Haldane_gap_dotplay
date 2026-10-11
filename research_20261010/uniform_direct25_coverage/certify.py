#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json,hashlib,time,resource,os
from fractions import Fraction as F
P=Path(__file__).resolve().parent;ROOT=P.parents[1];os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_CPU,(30,30));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));start=time.process_time()
src=P.parent/'uniform_n24_second_coverage/certify.py';spec=importlib.util.spec_from_file_location('arithmetic',src);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
ints={k:int(v) for line in read(P/'anchor25.out').decode().splitlines() for k,v in [line.split('=')]};N=ints['N0_25'];H=ints['H0_25'];assert N>0;R=F(H,N)+25*F(700741,500000);beta=F(49,4)
Q24=c.sector('J',24)+3*c.sector('N',24);Q26=c.sector('J',26)+3*c.sector('N',26);assert Q24>0 and Q26>0
numerator=c.expi(-2*beta*R)[0];denominator=Q24*Q26;C=c.down(numerator/denominator);gap=F(23,10000);margin=C-c.expi(beta*gap)[1]*(1-C);passed=C>F(1,2) and margin>0
for d,h in [('uniform_n24_second_coverage','ef04180cedde73a09aa627c3dc75c2730472c9f425fd29bcec376678fea00240'),('uniform_n26_second_coverage','c723bca65e315ad2c2d296a9b0cc6cf51dc67240749bd06ee812b49ec8a9e609')]:
 assert hashlib.sha256(read(P.parent/d/'MANIFEST_SHA256.json')).hexdigest()==h
q=json.loads(read(P.parent/'uniform_n24_second_coverage/length_resolved_certificate.json'));r=next(x for x in q['rows'] if x['L']==24);assert r['passed'] and F(r['gap'])>=gap
q=json.loads(read(P.parent/'uniform_n26_second_coverage/length_resolved_certificate.json'));assert q['combined_claim']['all_integer_L_at_least']==26 and F(q['combined_claim']['gap'])>=gap
for path in [src,P/'contract25.cpp',ROOT/'audit/mps/mps_blocks.txt',P.parent/'uniform_smaller_second_initialization/long_certificate.json',P.parent/'uniform_second_moment_optimization/certificate.json']:read(path)
claim={'all_integer_L_at_least':24,'gap':str(gap),'unique_ground_state':True,'bootstrap_initialization':30,'coverage_onset':24,'union':['isolated24 frozen parity certificate','direct thermal25 certificate','26..infinity accepted coverage']} if passed else None
out={'status':'EXACT_PRODUCER_PASS_REVIEW_REQUIRED' if passed else 'BOUNDED_METHOD_FAILURE','physical_L':25,'beta':str(beta),'shifted_total_Rayleigh':str(R),'norm_positive':True,'Q24':str(Q24),'Q26':str(Q26),'Z25_squared_upper':str(denominator),'Z25_2beta_lower':str(numerator),'purity_lower':str(C),'gap':str(gap),'exponential_margin':str(margin),'combined_claim':claim,'resources':{'cpu_seconds':time.process_time()-start,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'certificate.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n');print(out['status'],'R25',float(R),'C25',float(C),'margin',float(margin));print(claim);print(out['resources'])
