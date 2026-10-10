#!/usr/bin/env python3
import json,hashlib,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    work=json.loads((ROOT/'results/exact_work_counts.json').read_text());out={}
    for n in [9,10]:
        W=work[str(n)];rates={};detail=[]
        for tw in ['I','C']:
            rates[tw]=[]
            for m in ([0] if n==9 else [0,-4]):
                p=ROOT/f'results/benchmark_L{n}_{tw}_M{m}_chebyshev_r0_compressed_b4_c4_fast.json';r=json.loads(p.read_text());row=W['rows'][abs(m)]
                assert r['dimension']==row['dimension'] and r['nnz']==row['stored_edges'] and r['block_reps']==row['representatives']
                sec=r['compute_seconds']/r['identity']['count'];rate=sec/r['nnz'];rates[tw].append(rate)
                detail.append({'twist':tw,'M':m,'seconds_per_column':sec,'cpu_seconds_per_column':r['compute_cpu_seconds']/r['identity']['count'],'seconds_per_stored_edge_per_column':rate,'peak_rss_mib':r['max_rss_kib']/1024,'source_record':str(p.relative_to(ROOT))})
        all_edges=W['total_column_edges'];low_edges=W['low_M_0_to_4_column_edges']
        pair={tw:[min(v)*all_edges/3600,max(v)*all_edges/3600] for tw,v in rates.items()}
        ipc=[2*pair['I'][i]+pair['C'][i] for i in range(2)];ip=[2*pair['I'][i] for i in range(2)]
        out[str(n)]={'L':n,'exact_representatives':W['total_representatives'],'exact_column_edge_products':all_edges,'M0_through_absM4_work_fraction':low_edges/all_edges,'samples':detail,'I_or_P_core_hours_range':pair['I'],'C_core_hours_range':pair['C'],'IPC_core_hours_range':ipc,'IP_only_core_hours_range':ip,'IPC_low_M_core_hours_range':[h*low_edges/all_edges for h in ipc],'IP_only_low_M_core_hours_range':[h*low_edges/all_edges for h in ip],'interpretation':'Rate range from sampled magnetizations, not a confidence interval. P assumed same work rate as I. Excludes graph setup and checkpoint I/O; assumes graphs reused for sizeable chunks. Partial last SIMD batches add a negligible but unmodeled overhead.'}
        if n==9:
            speed={}
            for tw in ['I','C']:
                base=json.loads((ROOT/f'results/benchmark_L9_{tw}_M0_chebyshev_r0_native.json').read_text());new=next(x for x in detail if x['twist']==tw)
                speed[tw]=base['compute_seconds']/new['seconds_per_column']
            out[str(n)]['same_native_compile_speedup_vs_uncompressed']=speed
    result={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'No full L9/L10 run; extrapolated finite-trace costs only','by_length':out,'allocation_recommendation':'Do not start: L10 critical path exceeds the remaining two-core window and the updated optimistic scalar screen has no accepted seed.'}
    (ROOT/'results/optimized_cost_model.json').write_text(json.dumps(result,indent=2)+'\n')
    for n,r in out.items():print(n,'IPC',r['IPC_core_hours_range'],'IP low M',r['IP_only_low_M_core_hours_range'])
if __name__=='__main__':main()
