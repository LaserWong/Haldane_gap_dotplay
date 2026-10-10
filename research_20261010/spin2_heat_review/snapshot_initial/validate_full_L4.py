#!/usr/bin/env python3
"""All-column/orbit small-chain trace against independent archived GMP method."""
import json,subprocess,time,math,os,resource
from fractions import Fraction as F
from pathlib import Path
from report_budget import expbounds,ceilsqrt
from count_work import counts
ROOT=Path(__file__).resolve().parent;Q=2**56

def limits():resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3));resource.setrlimit(resource.RLIMIT_CPU,(590,600))
def main():
    begin=time.monotonic();out=[];C=json.loads((ROOT/'results/coefficient_audit.json').read_text());A=F(C['chebyshev']['weighted_recurrence_error']);work=counts(4)
    exe=ROOT/'original_dependencies/exact_thermal4'
    subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'original_dependencies/exact_thermal4.cpp'),'-lgmpxx','-lgmp','-o',str(exe)],check=True)
    for tw in ['I','P','C']:
        N=0;e2=0;reps=0
        for r in work['rows']:
            m=r['M'];cmd=[str(ROOT/'heat_compressed'), '4',tw,str(m),'0',str(r['representatives']),str(ROOT/'coefficients_chebyshev_Q56.txt'),'compute','4']
            p=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=600,preexec_fn=limits)
            (ROOT/f'logs/L4_{tw}_M{m}.stdout').write_text(p.stdout)
            lines=p.stdout.splitlines();meta=lines[0].split();assert int(meta[4])==r['dimension'] and int(meta[5])==r['representatives']
            weight=0
            for line in lines[1:]:
                code,mult,n0,n1=map(int,line.split());assert n1==0 and n0>=0;N+=mult*n0;weight+=mult;reps+=1
            assert weight==r['weight_sum']
            eta=(5*ceilsqrt(r['dimension'])+1)//2;E=75+math.ceil(eta*(A+137));e2+=weight*E*E
        e=ceilsqrt(e2);r=math.isqrt(N);lo=F(max(0,r-e)**2,Q*Q);hi=F((r+1+e)**2,Q*Q)
        # Original H4 computes the same shift b=5 and beta=8 directly by GMP Horner.
        logfile=ROOT/f'logs/original_GMP_L4_{tw}.stdout';errfile=ROOT/f'logs/original_GMP_L4_{tw}.stderr';t=time.monotonic()
        if not logfile.exists():
            with logfile.open('w') as so,errfile.open('w') as se:
                subprocess.run([str(exe),str(ROOT/f'original_dependencies/thermal4_{tw}.txt')],stdout=so,stderr=se,check=True,timeout=600,preexec_fn=limits)
        text=logfile.read_text();v=dict(line.split('=',1) for line in text.splitlines());old=F(int(v['numerator']),int(v['denominator']))
        J=640;mu=144;S=sum((F(mu**j,math.factorial(j)) for j in range(J+1)),F(0));tau=F(mu**(J+1),math.factorial(J+1))/(1-F(mu,J+2))/S;old_err=2*5**4*tau
        assert lo<old-old_err<old+old_err<hi
        # The newly run GMP rational must equal the archived exact result bitwise.
        archived=dict(line.split('=',1) for line in (ROOT/f'original_dependencies/thermal4_{tw}_exact.txt').read_text().splitlines() if '=' in line)
        assert v['numerator']==archived['numerator'] and v['denominator']==archived['denominator']
        x=8*4*(F(5)-F(5951,1250));sl,su=expbounds(x)
        out.append({'L':4,'twist':tw,'representatives':reps,'integer_norm':str(N),'frobenius_error_numerator':e,'b5_trace_lower':str(lo),'b5_trace_upper':str(hi),'a5951_1250_lower':str(sl*lo),'a5951_1250_upper':str(su*hi),'physical_trace_display':[float(sl*lo),float(su*hi)],'fresh_GMP_matches_archive':True,'independent_GMP_interval_strictly_inside_streamed_interval':True,'GMP_wall_seconds':time.monotonic()-t})
        print(tw,out[-1]['physical_trace_display'],out[-1]['GMP_wall_seconds'],flush=True)
    (ROOT/'results/full_L4_validation.json').write_text(json.dumps({'checks':out,'seconds':time.monotonic()-begin,'no_eigensolver':True},indent=2)+'\n')
if __name__=='__main__':main()
