#!/usr/bin/env python3
import json,math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent;Q=2**56

def ceilsqrt(n):r=math.isqrt(n);return r+(r*r<n)
def expbounds(x,K=160):
    term=s=F(1)
    for k in range(1,K+1):term*=x/k;s+=term
    assert x<K+2
    return s,s+term*x/(K+1)/(1-x/(K+2))
def main():
    work=json.loads((ROOT/'results/exact_work_counts.json').read_text());coef=json.loads((ROOT/'results/coefficient_audit.json').read_text());A=F(coef['chebyshev']['weighted_recurrence_error']);out={}
    for n in [9,10]:
        W=work[str(n)];r0=W['rows'][0];e2=0
        for r in W['rows']:
            eta=(5*ceilsqrt(r['dimension'])+1)//2
            E=75+math.ceil(eta*(A+137));r['column_error_numerator']=E
            e2+=r['weight_sum']*E*E
        e=ceilsqrt(e2);x=8*n*(F(39,8)-F(5951,1250));_,u=expbounds(x)
        # Outward upper on exp(x/2), not a floating square root.
        _,u2=expbounds(x/2);scaled=F(e+1,Q)*u2
        baselines={}
        for tw in ['I','C']:
            p=ROOT/f'results/benchmark_L{n}_{tw}_M0_chebyshev_r0.json'
            if p.exists():
                b=json.loads(p.read_text());hours=b['compute_seconds']/r0['stored_edges']*W['total_column_edges']/3600
                baselines[tw]={'seconds_per_M0_column':b['compute_seconds'],'full_sector_sum_core_hours_estimate':hours,'M0_through_absM4_core_hours_estimate':hours*W['low_M_0_to_4_column_edges']/W['total_column_edges'],'max_rss_mib':b['max_rss_kib']/1024}
        out[str(n)]={'exact_work':W,'frobenius_error_numerator':e,'unscaled_norm_error_display':float(F(e,Q)),'thermal_norm_error_upper':str(scaled),'thermal_norm_error_upper_display':float(scaled),'conditional_trace_error_upper_at_Z_le_100':str((20+scaled)*scaled),'conditional_trace_error_upper_at_Z_le_100_display':float((20+scaled)*scaled),'baseline_cost':baselines,'all_IPC_core_hours_estimate':2*baselines['I']['full_sector_sum_core_hours_estimate']+baselines['C']['full_sector_sum_core_hours_estimate'] if len(baselines)==2 else None}
    (ROOT/'results/cost_error_budget.json').write_text(json.dumps(out,indent=2)+'\n')
    for n,r in out.items():print(n,'norm error',r['thermal_norm_error_upper_display'],'conditional trace error',r['conditional_trace_error_upper_at_Z_le_100_display'],'IPC hours',r['all_IPC_core_hours_estimate'])
if __name__=='__main__':main()
