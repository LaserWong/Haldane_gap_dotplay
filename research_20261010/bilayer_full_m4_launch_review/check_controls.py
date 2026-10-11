from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
P=Path(__file__).resolve().parent;R=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
auditdir=R/'bilayer_complete_split_H2_8x4_review';audit=auditdir/'audit.json';manifest=auditdir/'MANIFEST_SHA256.json';witness=R/'bilayer_whole_m4_pipeline/witness57.txt';geometry=R/'bilayer_whole_m4_pipeline/geometry_8x4.txt';expected=R/'bilayer_full_m4_production_run/EXPECTED_M012.json'
assert sha(manifest)=='874c87f1ff9b4b58f795ef5e01aad45ff4f22e560e4721c7a933ed27380166a5'
assert sha(audit)==load(manifest)['audit.json']=='e357ac47fa68cdaeedac626596481ddc235ddd9caf24afb92f48d9b050d303ac'
assert sha(witness)=='fae87e68b4bfb670b23c0887d528bef018b1ecbf1aafe3fc3e2b2e756e92bba2'
assert sha(geometry)=='571b6f67ba7b181f784ead34548f01c69f2d5e933774fc3bf91730ed15e4d969'
assert sha(expected)=='f528834efae7b875b4dfa665ab991f4bfd7db73d54507ac681c8402e1a6f19ec'
a=load(audit);c=list(map(int,witness.read_text().split()));assert len(c)==a['dimension']==57 and a['full_q8_retained_in_MM'] and a['geometry']==[8,4]
arrays=[a['gram']]+a['H_coefficients']+a['H2_coefficients'];assert len(arrays)==6
# Symmetric upper-triangle quadratic form, independently implemented without producer helpers.
def quadratic(mat):
 assert len(mat)==57 and all(len(row)==57 for row in mat)
 total=F(0)
 for i in range(57):
  total+=c[i]*c[i]*F(mat[i][i])
  for j in range(i):
   assert F(mat[i][j])==F(mat[j][i]);total+=2*c[i]*c[j]*F(mat[i][j])
 return total
forms=list(map(quadratic,arrays));g=F(11,100)
m=[forms[0],200*(forms[1]+g*forms[2]),40000*(forms[3]+g*forms[4]+g*g*forms[5])]
assert all(x.denominator==1 for x in m);v=load(expected);assert [str(int(x)) for x in m]==[v[k] for k in ['m0','m1','m2']]
assert (v['T_Q'],v['T_A'],v['g_num'],v['g_den'],v['dimension'])==(200,11,11,100,57)
assert (v['source_audit_sha256'],v['source_review_manifest_sha256'],v['witness_sha256'],v['geometry_sha256'])==(sha(audit),sha(manifest),sha(witness),sha(geometry))
prior=next(x for x in load(R/'bilayer_symmetry_intermediate_points/fixed011_moment_reference.json')['moments'] if x['N']==32)
assert prior['coefficients']==c and F(prior['norm'])==m[0]
assert 200*m[0]*(F(prior['rho'][0])+g*F(prior['rho'][1]))==m[1]
assert 40000*m[0]*sum(g**i*F(x) for i,x in enumerate(prior['second']))==m[2]
report=dict(status='PASS_ACCEPTED57D_FIXED_WITNESS_M012',moments=list(map(str,m)),quadratic_forms=list(map(str,forms)),source_hashes={str(x):sha(x) for x in [manifest,audit,witness,geometry,expected]},independent_scalar_reference_agrees=True,full_q8=True,no_physical_sweep=True)
(P/'CONTROLS_CHECK.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
