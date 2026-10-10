#!/usr/bin/env python3
import subprocess,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    t=time.monotonic();results=[]
    for n,m in [(3,0),(4,0),(4,-1)]:
      for tw in ['I','P','C']:
        args=[str(n),tw,str(m),'0','9',str(ROOT/'coefficients_chebyshev_Q56.txt'),'dump']
        original=subprocess.check_output([str(ROOT/'heat_columns_ubsan')]+args,stderr=subprocess.DEVNULL)
        for b in [1,2,4,8]:
            new=subprocess.check_output([str(ROOT/'heat_compressed_ubsan')]+args+[str(b)],stderr=subprocess.DEVNULL)
            assert original==new,(n,m,tw,b)
            results.append({'L':n,'M':m,'twist':tw,'block_columns':b,'all_emitted_coordinates_bitwise_identical':True,'ubsan_pass':True})
    out={'checks':results,'seconds':time.monotonic()-t,'interpretation':'Includes mixed seed parities, more than one batch, short final batches, and N1/N2 kernels. Earlier Python-bigint audit independently verifies the reference.'}
    (ROOT/'results/compressed_validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
