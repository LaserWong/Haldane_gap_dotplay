import audit as A
import json,shutil

def main():
 source=A.BASE/'chain_frontier_rank195';records={}
 expected={'PHYSICAL_FREEZE.json':'53d6f33f3f7ad30dabe11fdd98fe9a4e0ffd28546c76fb383a91be84c6ea744a','FROZEN_MANIFEST.json':'fc71128d5b7901c75e3c5322c23bf4cc428896b82d97518a78da3052ca8cb8e5'}
 for manifest,digest in expected.items():
  f=source/manifest;assert A.sha(f)==digest;files=json.loads(f.read_text())
  for name,h in files.items():
   p=source/name;assert A.sha(p)==h;dst=A.SNAP/name;dst.parent.mkdir(parents=True,exist_ok=True)
   if dst.exists():assert A.sha(dst)==h
   else:shutil.copy2(p,dst)
  records['producer/'+manifest]=dict(sha256=digest,files=len(files))
 for folder,manifest in [('chain_frontier_above_02_review','MANIFEST_SHA256.json'),('chain_low_band_review','MANIFEST_SHA256.json'),('joint_ratio_review','CHAIN_REVIEW_MANIFEST.json'),('joint_ratio_review','LEMMA_REVIEW_MANIFEST.json')]:
  root=A.BASE/folder;files=json.loads((root/manifest).read_text())
  for name,h in files.items():assert A.sha(root/name)==h,(folder,name)
  records[folder+'/'+manifest]=dict(sha256=A.sha(root/manifest),files=len(files))
 assert records['chain_frontier_above_02_review/MANIFEST_SHA256.json']['sha256']=='20d6cda2475a81b2ceca9a05e1c3f838bb44df07a400342db5d4eb3f36917e52'
 assert A.sha(A.BASE/'chain_frontier_review/independent_core.py')=='30c997e6e56135af60cd989ab22e31a8957346dc3ff2235ae8ac6b2c62916a19'
 external=json.loads((A.SNAP/'EXTERNAL_INPUT_SHA256.json').read_text())
 for name,h in external.items():assert A.sha(A.ROOT/name)==h,('external',name)
 records['external_files_verified']=len(external);A.save('PROVENANCE.json',records);print('PROVENANCE PASS',flush=True)
if __name__=='__main__':main()
