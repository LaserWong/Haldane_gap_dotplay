# SANITY ONLY (float64 dense ED, not rigorous, not part of the proof):
# Z_L^g(49/4) = Tr exp[-beta(H_L^g + aL)], g in {I,P}; P = pi-rotation (about z) on the closing bond,
# i.e. closing-bond flip terms get sign -1. Compared with the repo's refined intervals.
import numpy as np, itertools, json
from fractions import Fraction as Fr
beta=49/4; a=700741/500000
d=json.load(open('/workspace/repos/Haldane_gap_dotplay/research_20261010/uniform_second_thermal_full_review/provenance_results.json'))
iv={c['case']:[float(Fr(x)) for x in c['refined_rounded_interval']] for c in d['cases']}
def Z(L,tw):
    tot=0.0
    confs=list(itertools.product((1,0,-1),repeat=L))
    byM={}
    for c in confs: byM.setdefault(sum(c),[]).append(c)
    for M,cs in byM.items():
        idx={c:i for i,c in enumerate(cs)}; n=len(cs); H=np.zeros((n,n))
        for c in cs:
            i=idx[c]
            for j in range(L):
                k=(j+1)%L; sgn=-1.0 if (tw=='P' and k==0) else 1.0
                H[i,i]+=c[j]*c[k]
                for dj in (1,-1):   # S+_j S-_k /2 and S-_j S+_k /2, spin-1 ladder elements sqrt2
                    nj, nk = c[j]+dj, c[k]-dj
                    if abs(nj)<=1 and abs(nk)<=1:
                        t=list(c); t[j]=nj; t[k]=nk
                        H[idx[tuple(t)],i]+=sgn*1.0
        assert np.allclose(H,H.T)
        ev=np.linalg.eigvalsh(H)
        tot+=np.exp(-beta*(ev+a*L)).sum()
    return tot
out={}
for L in range(4,11):
    for tw in 'IP':
        z=Z(L,tw); lo,hi=iv[f'L{L}_{tw}']
        rel=max(lo-z,z-hi,0)/z
        out[f'L{L}_{tw}']=z
        print(f'L{L}_{tw} float {z:.15g} repo [{lo:.15g},{hi:.15g}] inside={lo<=z<=hi} outside_rel={rel:.1e}',flush=True)
json.dump(out,open('sanity_thermal_float.json','w'),indent=1)
