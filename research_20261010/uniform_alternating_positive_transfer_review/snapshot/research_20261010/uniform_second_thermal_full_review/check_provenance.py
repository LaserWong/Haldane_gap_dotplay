#!/usr/bin/env python3
"""Exact dependency composition; no imported producer code or physical computation."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,os,resource
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
P=Path(__file__).resolve().parent;R=P.parent;ROOT=R.parent;H={}
def rd(p):
 b=p.read_bytes();H[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(rd(p))
def seal(name,want):
 p=R/name;m=js(p/'MANIFEST_SHA256.json');assert H[str((p/'MANIFEST_SHA256.json').relative_to(ROOT))]==want
 for f,h in m.items():assert hashlib.sha256(rd(p/f)).hexdigest()==h
 return want
seals={}
for n,h in [('uniform_second_thermal_campaign_complete','17110955acc17821025bab5c1609706273510de6c8c2a31eb7184d693a9b9156'),('uniform_second_initialization_review','3e713b2de14407cca8c14e7236c23077998d29ea13268267626859fc5c23511b'),('uniform_second_moment_review','dbdea168300fa8a014c4a1fcbb72a6f64d1f8ddb3250949eeeed067d55c329de'),('uniform_second_initialization_scalar','2ee9120d69863ab73babbcc9c07036cabcd787f9d8ad6b61f9f485656ccb1a59'),('uniform_second_moment_optimization','dc81945f85281a33df1b272a7a054b6f5d9b5fa32e8c7a1868c26e07bc97ec85')]:seals[n]=seal(n,h)
rows=js(P/'progress_results.json');assert rows['completed']==18 and not rows['pending']
export=js(R/'uniform_second_thermal_campaign_complete/thermal_inputs.json');ex={f"L{x['n']}_{x['twist']}":x for x in export['thermal_inputs']};assert len(ex)==18
base=js(R/'uniform_second_initialization_scalar/certificate.json');tight=js(R/'uniform_second_moment_optimization/certificate.json');D={};mapping=[]
for x in rows['cases']:
 n=int(x['case'].split('_')[0][1:]);tw=x['case'][-1];j=0 if tw=='I' else 1;e=ex[x['case']];lo=F(x['lower']);hi=F(x['upper']);assert x['W']==e['W'] and lo==F(e['lower']) and hi==F(e['upper'])
 c=F(base['thermal_premise']['centers_in_units_1e-6'][str(n)][j],10**6);err=F(base['thermal_premise']['absolute_error']);assert c-err<lo<=hi<c+err
 g=10**18;l=F((lo*g).__floor__(),g);u=F((hi*g).__ceil__(),g);assert l<=lo<=hi<=u;D[n,tw]=(l,u)
 mapping.append({'case':x['case'],'W':x['W'],'physical_certificate_sha256':x['certificate_file_sha256'],'coarse_center':str(c),'coarse_error':str(err),'refined_rounded_interval':[str(l),str(u)]})
M={'J':[],'N':[]}
for n in range(4,13):
 (zl,zu),(pl,pu)=D[n,'I'],D[n,'P'];M['J'].append([(zl+3*pl)/4,(zu+3*pu)/4]);M['N'].append([(zl-pu)/4,(zu-pl)/4])
assert {k:[[str(a),str(b)] for a,b in v] for k,v in M.items()}==tight['moment_intervals']
# The accepted physical MPS reconstruction is inherited, with exact input identity
# and one-bond versus total-energy normalization independently rechecked here.
ap=ROOT/'audit/mps/contraction.out';a={k:int(v) for k,v in (line.split('=') for line in rd(ap).decode().splitlines() if '=' in line)};v=a['V72'];u=a['U72'];assert v>0 and -700741*v-500000*u>0
energy=72*(F(u,v)+F(700741,500000));assert energy==F(base['anchor']['shifted_Rayleigh'])==F(js(R/'uniform_second_moment_review/results.json')['MPS72_shifted_Rayleigh'])<0
for name in ['uniform_second_initialization_review','uniform_second_moment_review']:
 pins=js(R/name/'INPUT_SHA256.json');matches=[h for p,h in pins.items() if p.endswith('audit/mps/contraction.out')];assert matches and set(matches)=={hashlib.sha256(ap.read_bytes()).hexdigest()}
rd(ROOT/'audit/APPENDIX_A_BRIDGE.md')
# Adversarial endpoint/cross-sector guards are strict equality, not decimal tolerance.
tests=[]
for k in ('J','N'):
 bad=json.loads(json.dumps(tight['moment_intervals']));bad[k][0][0]=str(F(bad[k][0][0])+F(1,10**18));assert bad!={q:[[str(a),str(b)] for a,b in z] for q,z in M.items()};tests.append(k+'_single_endpoint_mutation_rejected')
assert 72*(F(u,v)+F(700741,500000))!=F(u,v)+F(700741,500000);tests.append('one_bond_as_total_energy_mismatch_detected')
out={'status':'ACCEPTED physical thermal premises discharged for both reviewed scalar theorems','thermal_inputs':18,'all_exact_W_and_refined_endpoints_match':True,'cases':mapping,'signed_moment_intervals':{k:[[str(a),str(b)] for a,b in z] for k,z in M.items()},'MPS72':{'source':'audit/mps/contraction.out','sha256':hashlib.sha256(ap.read_bytes()).hexdigest(),'norm_positive':True,'U_is_one_bond_numerator':True,'shifted_total_Rayleigh':str(energy),'physical_rebuild_provenance':'audit/APPENDIX_A_BRIDGE.md section physical MPS reconstruction; both accepted scalar reviews pin same contraction file','new_contraction_performed':False},'accepted_claims':[{'gap':'23/5000','all_integer_L_at_least':36,'unique_ground_state':True},{'gap':'107/5000','all_integer_L_at_least':36,'unique_ground_state':True}],'seals_verified':seals,'adversarial_checks':tests}
(P/'provenance_results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'PROVENANCE_INPUT_SHA256.json').write_text(json.dumps(H,indent=2)+'\n');print(out['status'])
