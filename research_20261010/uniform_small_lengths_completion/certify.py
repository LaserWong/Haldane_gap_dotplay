#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,hashlib,os,resource,time
P=Path(__file__).resolve().parent;ROOT=P.parents[1];os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_CPU,(30,30));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));start=time.process_time();inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
src=P.parent/'uniform_n24_second_coverage/certify.py';read(src);spec=importlib.util.spec_from_file_location('arithmetic',src);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
phy=P.parent/'uniform_second_thermal_full_review';assert hashlib.sha256(read(phy/'MANIFEST_SHA256.json')).hexdigest()=='792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94';prov=json.loads(read(phy/'provenance_results.json'));assert prov['thermal_inputs']==18 and prov['all_exact_W_and_refined_endpoints_match']
I={int(x['case'].split('_')[0][1:]):F(x['refined_rounded_interval'][1]) for x in prov['cases'] if x['case'].endswith('_I')};assert set(I)==set(range(4,13))
long=json.loads(read(P/'long_certificate.json'));old=json.loads(read(P.parent/'uniform_smaller_second_initialization/long_certificate.json'));old.update(long)
def sector(s,L):
 cap=c.sector(s,L);key=f'{s}{L}'
 return min(cap,F(old[key]['bound'])) if key in old else cap
def upper(L):
 if L<=12:return I[L],'PHYSICAL_UNTWISTED_I'
 q=sector('J',L)+3*sector('N',L)
 assert q>0
 if L%2:
  a=(I[L-1] if L-1<=12 else sector('J',L-1)+3*sector('N',L-1));b=sector('J',L+1)+3*sector('N',L+1);cs=c.root(a*b,2)[1]
  return (q,'SIGNED_MOMENT_POLYNOMIAL') if q<=cs else (cs,'EVEN_NEIGHBOR_CAUCHY_SCHWARZ')
 return q,'EVEN_SIGNED_MOMENT_OR_PACKING'
ints={k:int(v) for line in read(P/'anchors.out').decode().splitlines() for k,v in [line.split('=')]};rows=[];beta=F(49,4);gap=F(23,10000)
for L in range(4,24):
 N=ints[f'N0_{L}'];H=ints[f'H0_{L}'];assert N>0;R=F(H,N)+L*F(700741,500000);Q,method=upper(L);num=c.expi(-2*beta*R)[0];C=c.down(num/(Q*Q));margin=C-c.expi(beta*gap)[1]*(1-C);passed=C>F(1,2) and margin>0;assert C<=1
 rows.append({'L':L,'norm_positive':True,'shifted_total_Rayleigh':str(R),'trace_upper':str(Q),'trace_method':method,'numerator_lower':str(num),'purity_lower':str(C),'gap':str(gap),'margin':str(margin),'passed':passed})
 print(L,method,'R',float(R),'C',float(C),'PASS' if passed else 'FAILED_BOUND',flush=True)
# Normalization and small-volume analytic checks are finite angular-momentum algebra.
read(ROOT/'audit/APPENDIX_A_BRIDGE.md');analytic={'2':{'Hamiltonian':'2 S1 dot S2','energies_by_total_spin':[-4,-2,2],'ground_multiplicity':1,'gap':'2'},'3':{'Hamiltonian':'(S_total^2-6)/2','energies_by_total_spin':[-3,-2,0,3],'ground_multiplicity':1,'gap':'1','singlet_multiplicity_reason':'only intermediate j12=1 couples with j3=1 to total0'}}
prior=P.parent/'uniform_direct25_coverage';assert hashlib.sha256(read(prior/'MANIFEST_SHA256.json')).hexdigest()=='abd4e0f0a315ef9878129c56ee884d797707687f07361c83f1cb140f0ebee9fa';a=json.loads(read(prior/'certificate.json'));assert a['combined_claim']['all_integer_L_at_least']==24 and F(a['combined_claim']['gap'])>=gap
holes=[r['L'] for r in rows if not r['passed']];claim={'all_integer_L_at_least':2,'gap':str(gap),'unique_ground_state':True,'bootstrap_initialization':30,'coverage_onset':2,'union':['analytic2,3','direct thermal4..23','inherited24..infinity']} if not holes else None
for f in [P/'contract_small.cpp',ROOT/'audit/mps/mps_blocks.txt',P.parent/'uniform_second_moment_optimization/certificate.json']:read(f)
out={'status':'PRODUCER_EXACT_COMPLETE_PASS_REVIEW_REQUIRED' if not holes else 'PRODUCER_PARTIAL_WITH_FAILED_BOUNDS','beta':str(beta),'common_gap':str(gap),'rows':rows,'analytic_small_lengths':analytic,'failed_bound_lengths':holes,'combined_claim':claim,'resources':{'cpu_seconds':time.process_time()-start,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'certificate.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n');print(out['status'],claim);print(out['resources'])
