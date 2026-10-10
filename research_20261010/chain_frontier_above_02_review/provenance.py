import audit as A
import json,shutil

def main():
 records={}
 assert A.sha(A.SOURCE/'FROZEN_MANIFEST.json')=='f3e38ff6b3106078c1a4109db83722e1220e5214fc3e6b3c9aaea5920e1074bc'
 assert A.sha(A.SOURCE/'PHYSICAL_FREEZE.json')=='dfbe82c36175393074495d592f8284c11ff8d4f67d493e38fef405717dd4d305'
 assert A.sha(A.SOURCE/'SCALAR_FREEZE.json')=='e1128f4fc6d779472ec62794b327425ef1f8e3f699a63c8dd5f0ba5be0d4300d'
 for folder,manifest in [('chain_low_band_review','MANIFEST_SHA256.json'),('joint_ratio_review','CHAIN_REVIEW_MANIFEST.json'),('joint_ratio_review','LEMMA_REVIEW_MANIFEST.json')]:
  root=A.BASE/folder;data=json.loads((root/manifest).read_text())
  for name,digest in data.items():assert A.sha(root/name)==digest,(folder,name)
  records[folder+'/'+manifest]=dict(sha256=A.sha(root/manifest),files=len(data))
 assert A.sha(A.BASE/'chain_frontier_review/independent_core.py')=='30c997e6e56135af60cd989ab22e31a8957346dc3ff2235ae8ac6b2c62916a19'
 for manifest in ['PHYSICAL_FREEZE.json','FROZEN_MANIFEST.json']:
  p=A.SOURCE/manifest;data=json.loads(p.read_text());records['producer/'+manifest]=dict(sha256=A.sha(p),files=len(data))
  for name,digest in data.items():
   src=A.SOURCE/name;assert A.sha(src)==digest,name;dest=A.SNAP/name;dest.parent.mkdir(parents=True,exist_ok=True)
   if dest.exists():assert A.sha(dest)==digest,('snapshot conflict',name)
   else:shutil.copy2(src,dest)
  shutil.copy2(p,A.HERE/('PRODUCER_'+manifest))
 ext=json.loads((A.SNAP/'EXTERNAL_INPUT_SHA256.json').read_text())
 for name,digest in ext.items():assert A.sha(A.ROOT/name)==digest,('external input',name)
 records['external_input_count']=len(ext)
 A.save('PROVENANCE.json',records);print('PROVENANCE PASS',flush=True)
if __name__=='__main__':main()
