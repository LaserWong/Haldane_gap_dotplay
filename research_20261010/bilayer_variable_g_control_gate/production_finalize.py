"""Final complete-coverage and accepted-low-moment gate; never accepts sample sums."""
from fractions import Fraction as F
import pencil24

def assemble(sectors,expected_controls,origin_reduced=True):
 assert expected_controls['schema']=='accepted-fixed-witness-m012-v1'
 assert expected_controls['T_Q']==200 and expected_controls['T_A']==11
 # The caller must obtain sectors through the checked complete-coverage finalizer.
 p=pencil24.pencil(sectors,11,100,origin_reduced)
 actual=p['G_numerators'];expected=[str(int(expected_controls[k])) for k in ['m0','m1','m2']]
 assert actual==expected,'accepted_full_m0_m1_m2_mismatch'
 return {'schema':pencil24.SCHEMA,'accepted_m012_matched':True,'pencil_at_11_over_100':p}

# Production integration must use the frozen controller's finalize() first with
# exact expected sector coverage {0:1,2:496,4:4495,6:169911}; its output is passed
# here. Expected controls and their witness/rule identity must be externally
# verified and hash-pinned in the production job before launch.

def finalize_job():
 import os,fcntl,json
 import production_controller as c
 c.verify_inputs();lock=open(c.P/'LOCK','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 try:
  ledger=c.read(c.P/'BUDGET_LEDGER.json');c.validate_budget(ledger)
  for rec in ledger['attempts']:
   if rec['state']=='complete':c._adopt_completed(c.P/'runs'/rec['name'])
  dirs=[d for d in (c.P/'committed').iterdir() if d.is_dir()];assert len(dirs)==1,'mixed_job_identities'
  job=dirs[0].name;sectors=c.finalize(dirs[0],job,{0:1,2:496,4:4495,6:169911})
  expected=c.read(c.P/'EXPECTED_M012.json');ids=c.identities()
  assert expected['witness_sha256']==ids[str(c.SOURCE.parent/'bilayer_whole_m4_pipeline/witness57.txt')]
  assert expected['geometry_sha256']==ids[str(c.SOURCE.parent/'bilayer_whole_m4_pipeline/geometry_8x4.txt')]
  result=assemble(sectors,expected,True);v=result['pencil_at_11_over_100'];mat=pencil24.validate_export(v)
  m3=200*mat['K'][2];m4=40000*mat['J'][2];assert m3.denominator==m4.denominator==1
  result.update(job=job,complete_coverage={0:1,2:496,4:4495,6:169911},m3=str(int(m3)),m4=str(int(m4)),sector_accumulators={q:list(map(str,a)) for q,a in sectors.items()})
  c.atomic(c.P/'FULL_MOMENTS.json',result);return result
 finally:lock.close()
