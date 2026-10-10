"""Producer-assisted proposals followed by independent audit, new outputs only.
Floating scans select beta; exact data, interval tails and independent checks
are required before a positive result is labeled certified.
"""
import os,sys
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,time
BASE=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'low_energy'));sys.path.insert(0,str(OUT))
import fully_frustrated as producer
import dimer_subspace
from audit_ff import audit,local_psd
GENERATED=OUT/'epsilon_scan';GENERATED.mkdir(exist_ok=True)
producer.OUT=GENERATED;dimer_subspace.OUT=GENERATED

def float_seed(records,beta):
    U=[float(F(r['ground_upper'])) for r in records];q=[]
    for r in records:
        ref=r['reference_certificate'];a=float(F(ref['a']));B=float(F(ref['B']));hi=float(F(r['ground_upper']));lo=float(F(r['ground_lower']));E00=float(F(r['E00']))
        tail=sum(row['multiplicity']*math.exp(-beta*(E00+float(F(row['energy_lower']))-4*a*row['q']-B-hi)) for row in ref['bins'] if row['q'])
        q.append(math.exp(beta*(hi-lo))+tail)
    G=lambda x:1-(1-x)**2/(2*x*x) if x>0 else -1
    A=G(math.exp(-beta*(2*U[2]-8*U[0]))/q[0]**8)
    if A<=0:return None
    B=G(math.exp(-beta*(4*U[2]-8*U[1]))/q[1]**8*A)
    if B<=0:return None
    C=G(q[2]**-8*A*A*B)
    if C<=0:return None
    n=4;b=2*beta
    for j in range(64):
        u=max(1-A,1-B,1-C)
        if u<=.002:return dict(beta=beta,n=n,gap=math.log(1/(32*u))/b if u else float('inf'))
        for _ in range(3):
            new=G(A**4*B**2*C)
            if new<=0:return None
            A,B,C=B,C,new
        n*=2;b*=2
    return None

def improved_bridge(eps,n):
    # Exact local comparison with q-sector lower bound 1-16a for L>=3.
    if n<=3:return {'bound':str(F(2,5)-12*eps),'a':'0','b':None}
    N=(n-1)**2
    ax=float(eps)*(0.5+math.sqrt(3)*(N-8)/(8*math.sqrt(N-4)))
    a=F(round(max(0,ax)*10**9),10**9)
    if a>=F(1,16):return {'bound':None,'reason':'a outside q-sector bridge range'}
    loc=producer.local_bound(F(1,2),eps,a,'bilayer');b=F(loc['b']);psd=local_psd(a,b,eps)
    assert psd['inertia']==[0,0,16]
    bound=min(F(2,5)-12*eps,1-16*a-2*N*b)
    return {'bound':str(bound),'a':str(a),'b':str(b),'worst_L':n-1,'local_exact_PSD':True,'local_certificate':loc}

def run(values):
    summary=json.loads((OUT/'epsilon_scan_summary.json').read_text()) if (OUT/'epsilon_scan_summary.json').exists() else []
    bins={shape:producer.occupancy_bins(*shape,F(3,10)) for shape in [(2,2),(4,2),(4,4)]}
    for eps in map(F,values):
        t=time.monotonic();records=[]
        for nx,ny in [(2,2),(4,2),(4,4)]:
            tag=f'ff_{nx}x{ny}_eps{eps}_q2'.replace('/','d');p=GENERATED/(tag+'_ground.json')
            if p.exists():r=json.loads(p.read_text())
            else:
                ref=producer.optimize_comparison(nx*ny,eps,bins[nx,ny])
                r=dimer_subspace.certify_sparse(F(1,2),nx*ny,producer.weak_bonds(nx,ny,F(3,10),eps),tag=tag,reference_certificate=ref)
            r.update(nx=nx,ny=ny);records.append(r)
        grid=[float_seed(records,k/2) for k in range(24,241)]
        good=[r for r in grid if r];selected=set()
        if good:
            selected.add(max(good,key=lambda r:r['gap'])['beta'])
            for n in sorted({r['n'] for r in good}):selected.add(max((r for r in good if r['n']==n),key=lambda r:r['gap'])['beta'])
        else:selected={16,24,32,48,64,96,120}
        seeds=[producer.seed3(records,F(beta)) for beta in sorted(selected)]
        p=GENERATED/(f'ff_eps{eps}_selected_seeds.json'.replace('/','d'))
        p.write_text(json.dumps(dict(J='3/10',epsilon=str(eps),perturbation='straight J+epsilon, crossed J; unit rungs',ground_certificates=records,seeds=seeds,float_scan={'beta_min':12,'beta_max':120,'beta_step':.5,'successful_beta_count':len(good),'best':max(good,key=lambda r:r['gap']) if good else None},seconds=time.monotonic()-t),indent=2))
        verified=audit(p)
        successful=[]
        for seed in verified['seed_checks']:
            if seed['accepted']:
                bridge=improved_bridge(eps,seed['n']);bound=F(bridge['bound']) if bridge['bound'] else F(-1)
                successful.append(dict(beta=seed['beta'],n=seed['n'],bootstrap_gap=seed['gap_lower'],bridge=bridge,all_sizes_gap=str(min(F(seed['gap_lower']),bound)) if bound>0 else None))
        best=max((r for r in successful if r['all_sizes_gap']),key=lambda r:F(r['all_sizes_gap']),default=None)
        row=dict(epsilon=str(eps),audited_selected_seed_file=p.name,float_successful_beta_count=len(good),float_beta_grid=[12,120,.5],exact_successes=successful,best_all_sizes=best,seconds=time.monotonic()-t)
        summary=[old for old in summary if old['epsilon']!=row['epsilon']]+[row];summary.sort(key=lambda v:F(v['epsilon']));(OUT/'epsilon_scan_summary.json').write_text(json.dumps(summary,indent=2));print('SCAN_SUMMARY',json.dumps(row),flush=True)
    return summary
if __name__=='__main__':run(sys.argv[1:] or ['3/500','3/400','1/100','1/80','3/200','1/50'])
