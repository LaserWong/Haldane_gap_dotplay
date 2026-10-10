import audit as A
import json,shutil

def main():
 source=A.BASE/'chain_numerator_krylov_025';expected='cb2e5e34bf4f4cfbadcb2473109fd2f17f86ae46ae83366230865084932173d3';assert A.sha(source/'FROZEN_MANIFEST.json')==expected;records={}
 files=json.loads((source/'FROZEN_MANIFEST.json').read_text())
 for n,h in files.items():
  assert A.sha(source/n)==h;dest=A.SNAP/n
  if dest.exists():assert A.sha(dest)==h
  else:dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/n,dest)
 records['producer']=dict(sha256=expected,files=len(files))
 for folder,digest in [('chain_frontier_rank195_review','1365bd8c7fe06acf5c4c8bdaf264d1638c17bad5df72c8d753a8ee6ac615c959'),('chain_frontier_above_02_review','20d6cda2475a81b2ceca9a05e1c3f838bb44df07a400342db5d4eb3f36917e52')]:
  root=A.BASE/folder;assert A.sha(root/'MANIFEST_SHA256.json')==digest;ff=json.loads((root/'MANIFEST_SHA256.json').read_text())
  for n,h in ff.items():assert A.sha(root/n)==h,(folder,n)
  records[folder]=dict(sha256=digest,files=len(ff))
 ext=json.loads((A.SNAP/'EXTERNAL_INPUT_SHA256.json').read_text())
 for n,h in ext.items():assert A.sha(A.ROOT/n)==h,('external',n)
 # The all-temperature implication is accepted only with this exact prior target and domain.
 prior=json.loads((A.BASE/'chain_frontier_rank195_review/ACCEPTANCE.json').read_text());assert prior['necessary_numerator_target']['delta_must_be_less_than']=='19/1250' and prior['denominator_independent_obstruction']['temperature_scope']=='All beta>=0'
 records['external_files_verified']=len(ext);A.save('PROVENANCE.json',records);print('PROVENANCE PASS',flush=True)
if __name__=='__main__':main()
