import audit as A
import json

def main():
 report={}
 for folder,snapshot,expected in [('chain_numerator_pair_orbits_025',A.PAIR,'440145ba4a4b57d5202f1b6a4b914ab420520aea0465f1d58acec081c67abbd9'),('chain_numerator_pair_block_025',A.BLOCK,'68653bd8728e379ff84b0c310798ad9cd7e3b5c28d99af9b64cb12f6c467acdd')]:
  p=A.BASE/folder;assert A.A.sha(p/'FROZEN_MANIFEST.json')==expected;ff=json.loads((p/'FROZEN_MANIFEST.json').read_text())
  for n,h in ff.items():assert A.A.sha(p/n)==A.A.sha(snapshot/n)==h
  ext=json.loads((snapshot/'EXTERNAL_INPUT_SHA256.json').read_text())
  for n,h in ext.items():assert A.A.sha(p/n)==h
  report[folder]=dict(manifest_sha256=expected,files=len(ff),external_files=len(ext))
 for folder,h in [('chain_m8_numerator_review','d7a17b286228f71c655a1314fa66c6d27edb1fc52a6c32c24db82ffbbe4a50ec'),('chain_frontier_rank195_review','1365bd8c7fe06acf5c4c8bdaf264d1638c17bad5df72c8d753a8ee6ac615c959'),('chain_frontier_above_02_review','20d6cda2475a81b2ceca9a05e1c3f838bb44df07a400342db5d4eb3f36917e52')]:
  p=A.BASE/folder;assert A.A.sha(p/'MANIFEST_SHA256.json')==h;ff=json.loads((p/'MANIFEST_SHA256.json').read_text())
  for n,hh in ff.items():assert A.A.sha(p/n)==hh
  report[folder]=dict(manifest_sha256=h,files=len(ff))
 A.save('PROVENANCE.json',report);print('PROVENANCE PASS',flush=True)
if __name__=='__main__':main()
