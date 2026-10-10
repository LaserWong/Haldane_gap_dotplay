"""Continue an already certified staircase with increasing dyadic precision.
No physical input or previously frozen certificate is modified.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from low_band_certificate import ROOT
sys.path.insert(0,str(ROOT/'two_d_theory'))
from three_purity_certificate import log_lower,down

def up2(x,bits):
    d=1<<bits
    return F(-((-x.numerator*d)//x.denominator),d)

def continue_record(row,rounds=8):
    row=json.loads(json.dumps(row));old=row['bootstrap'];inp=old['input'];beta=F(inp['beta']);n=inp['n'];m=inp['m']
    q=[up2(1-F(inp[f'{x}_lower']),128) for x in 'ABC']
    boot={'input':inp,'updates':[],'status':'not_accepted','formal_proof_assistant_verified':False}
    levels=[]
    for j in range(rounds+1):
        u=max(q)
        if u<=F(1,500) and u>0:
            gap=down(log_lower(1/(32*u))/beta,digits=15)
            levels.append(dict(round=j,n=n,beta=str(beta),u=str(u),gap=str(gap),gap_display=float(gap)))
        if j==rounds:break
        bits=128*2**max(0,j-3)
        for axis in range(3):
            a,b,c=q;x=(1-a)**4*(1-b)**2*(1-c)
            assert x>0
            new=up2((1-x)**2/(2*x*x),bits)
            assert new<1
            q=q[1:]+[new]
        n*=2;m*=2;beta*=2
        boot['updates'].append(dict(round=j+1,defects=list(map(str,q)),dyadic_bits=bits))
    u=max(q);assert u<=F(1,500)
    gap=down(log_lower(1/(32*u))/beta,digits=15)
    boot.update(status='accepted_analytic_scalar_certificate',rounds=rounds,n=n,m=m,beta=str(beta),defects=list(map(str,q)),u=str(u),
        uniform_square_gap_lower=str(gap),uniform_square_gap_lower_display=float(gap),
        scope='Every integer square side L>=n, conditional on the same audited transfer/interpolation theorem. Smaller sizes require the finite-window bridge for these new states.')
    row['bootstrap']=boot;row['continued_scalar_levels']=levels
    return row

if __name__=='__main__':
    source=HERE.parent/'symmetric_correlated_beta909d100_FINAL.json';start=time.monotonic();row=continue_record(json.loads(source.read_text())[0])
    row['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest();row['source_file']=source.name
    target=HERE/'symmetric_beta909d100_eight_rounds.json';target.write_text(json.dumps([row],indent=2)+'\n')
    print(json.dumps(row['continued_scalar_levels'],indent=2));print('seconds',time.monotonic()-start)
