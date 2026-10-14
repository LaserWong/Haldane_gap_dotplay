"""Reproduce numerical TFI seed survey and independent ED audit; no certificates."""
import json
import math
from pathlib import Path
import numpy as np
import mpmath as mp
from gapflow.quantum_ising import canonical_seed, log_partition, log_partition_mp, replay_candidate


def ed_levels(L,J,h):
    H=np.zeros((2**L,2**L))
    for s in range(2**L):
        H[s,s]=-J*sum((1-2*((s>>i)&1))*(1-2*((s>>((i+1)%L))&1)) for i in range(L))
        for i in range(L): H[s,s^(1<<i)]-=h
    return np.linalg.eigvalsh(H)


def main():
    rows=[]
    for h in ('0.5','1','1.5','2'):
        for n in (2,4,8,16):
            for beta in ('0.125','0.25','0.5','1','2','4','8','16','32','64','128'):
                row=canonical_seed(n,beta,h=h,dps=80)
                check=canonical_seed(n,beta,h=h,dps=120)
                row['precision_check_digits']=120
                with mp.workdps(130):
                    row['max_purity_difference_80_vs_120']=str(max(abs(mp.mpf(a['candidate'])-mp.mpf(b['candidate'])) for a,b in zip(row['edges'],check['edges'])))
                row['scalar_candidate_replay']=replay_candidate(row)
                rows.append(row)
    target=Path('benchmarks')
    (target/'quantum_ising_seeds.json').write_text(json.dumps({'status':'NUMERICAL_CANDIDATES_ONLY','rows':rows},indent=2)+'\n')
    audit=[]
    for L in range(2,9):
        for J,h in [(1,.5),(1,1),(1,1.5),(1,2),(1,-1.5),(0,.7),(1,0),(0,0)]:
            E=ed_levels(L,J,h)
            for beta in (0,.1,1,8):
                expected=-beta*E[0]+math.log(float(np.exp(-beta*(E-E[0])).sum()))
                actual=log_partition(L,beta,J,h)
                audit.append({'L':L,'J':J,'h':h,'beta':beta,'logZ_ED':expected,'logZ_JW':actual,'absolute_log_error':abs(actual-expected)})
    (target/'quantum_ising_ed_audit.json').write_text(json.dumps({'status':'NUMERICAL_VALIDATION_NOT_PROOF','max_absolute_log_error':max(r['absolute_log_error'] for r in audit),'rows':audit},indent=2)+'\n')
    for h in ('0.5','1','1.5','2'):
        for n in (2,4,8,16):
            options=[r for r in rows if r['h']==h and r['n']==n]
            best=min(options,key=lambda r:float(r['u_candidate']))
            print(h,n,'best beta',best['beta'],'u',best['u_candidate'][:24],'gap',best['gap_candidate'])
    print('ED max log error',max(r['absolute_log_error'] for r in audit))

if __name__=='__main__': main()
