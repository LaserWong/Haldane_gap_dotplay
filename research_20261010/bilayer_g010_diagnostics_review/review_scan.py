"""Independent floating sensitivity replay: explicitly not a physical certificate."""
import os,sys,resource,json,math,copy,time
from pathlib import Path
from fractions import Fraction as F
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
sys.dont_write_bytecode=True
cpu=os.sched_getaffinity(0);os.sched_setaffinity(0,{7 if 7 in cpu else min(cpu)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
ROOT=Path(__file__).resolve().parent.parent;SRC=ROOT/'bilayer_g010_diagnostics'
def load(p):return json.loads(p.read_text())
def G(x):return 1-(1-x)**2/(2*x*x)
def prod(x):return x[0]**4*x[1]**2*x[2]
def transport(x):
    a,b,c=x;return [a*math.sqrt(b),a*a*b*math.sqrt(c),a**4*b*b*c]
def trace(r,t):
    shift=float(F(r['blocks'][0]['eigen_upper'][0]));gr=math.exp(-t*(float(F(r['blocks'][0]['eigen_lower'][0]))-shift))
    lo=sum(b['multiplicity']*sum(math.exp(-t*(float(F(e))-shift)) for e in b['eigen_upper']) for b in r['blocks'])
    odd=sum(b['multiplicity']*sum(math.exp(-t*(float(F(e))-shift)) for e in b['eigen_lower']) for b in r['blocks'][1:])
    tail=sum(b['multiplicity']*math.exp(-t*(float(F(b['lower']))-shift)) for b in r['number_sector_bins']['bins'][2:])
    return lo,gr+odd+tail,gr,odd,tail

def scan(recs):
    e=[float(F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0])) for r in recs];success=[];best=None
    for bi in range(100,401):
        beta=bi/20;q0=trace(recs[0],beta);q1=trace(recs[0],2*beta);q2=trace(recs[1],2*beta);q3=trace(recs[2],2*beta)
        j1=math.exp(-2*beta*e[2]+8*beta*e[0])*q3[0]/q0[1]**8
        j2=math.exp(-4*beta*e[2]+16*beta*e[0])*q3[0]**2/q1[1]**8
        c0=math.exp(-2*beta*e[2]+4*beta*e[1])*q3[0]/q2[1]**2
        raw=[]
        for k in range(3):
            arg=j1 if k==0 else j2*raw[0] if k==1 else c0**4*raw[0]**2*raw[1]
            raw.append(G(arg))
            if raw[-1]<=0:break
        defects=[];canonical=transport(raw) if len(raw)==3 and min(raw)>0 else None
        if canonical is not None:
            joint=prod(raw)
            for cycle in range(11):
                if raw is not None:
                    tr=transport(raw);canonical=tr if canonical is None else [max(x,y) for x,y in zip(canonical,tr)];joint=max(joint,prod(raw))
                if canonical is None:break
                joint=max(joint,prod(canonical));u=max(1-x for x in canonical);defects.append(u)
                if u<=.002:
                    success.append(dict(beta=beta,score=math.log(1/(32*u))/(2*beta*2**cycle)));break
                a,b,c=canonical;d=G(max(prod(canonical),joint));nxt=None
                if d>0:
                    ee=G(max(b**4*c**2,joint**2)*d)
                    if ee>0:
                        f=G(max(c,joint)**4*d*d*ee)
                        if f>0:nxt=[d,ee,f]
                if raw is not None:
                    for _ in range(3):
                        t=G(prod(raw))
                        if t<=0:raw=None;break
                        raw=raw[1:]+[t]
                canonical=nxt;joint=prod(nxt) if nxt is not None else 0.
        row=dict(beta=beta,min_defect=min(defects,default=1))
        if best is None or row['min_defect']<best['min_defect']:best=row
    return dict(successes=len(success),best=max(success,key=lambda x:x['score']) if success else None,best_partial=best)
def main():
    start=time.monotonic();shapes=['4x4','8x4','8x8'];base=[load(ROOT/'low_band/combined_ground_bounds/combined'/f'patch_{s}_g1d10.json') for s in shapes];u=load(ROOT/'low_band/third_moment_exact/enlarged_8x8_g1d10.json')['shifted_rayleigh_upper'];base[2]['blocks']=base[2]['blocks'][:1];base[2]['blocks'][0]['eigen_upper']=[u]
    cases={'baseline':base}
    for name in ['ground_lower_to_saved_upper','odd_lower_to_saved_upper','tail_deleted','all_denominator_uncertainty_deleted']:
        r=copy.deepcopy(base)
        for p in r[:2]:
            if name in ['ground_lower_to_saved_upper','all_denominator_uncertainty_deleted']:p['blocks'][0]['eigen_lower']=p['blocks'][0]['eigen_upper'][:]
            if name in ['odd_lower_to_saved_upper','all_denominator_uncertainty_deleted']:p['blocks'][1]['eigen_lower']=p['blocks'][1]['eigen_upper'][:]
            if name in ['tail_deleted','all_denominator_uncertainty_deleted']:p['number_sector_bins']['bins']=p['number_sector_bins']['bins'][:2]
        cases[name]=r
    for delta in ['0.0005','0.001','0.002','0.003','0.004','0.005','0.01']:
        r=copy.deepcopy(base);r[2]['blocks'][0]['eigen_upper']=[str(F(u)-F(delta))];cases['numerator_minus_'+delta]=r
    for i,s in enumerate(shapes[:2]):
        for f in ['0.1','0.25','0.5','0.75','1.0']:
            r=copy.deepcopy(base);lo=F(r[i]['blocks'][0]['eigen_lower'][0]);up=F(r[i]['blocks'][0]['eigen_upper'][0]);r[i]['blocks'][0]['eigen_lower']=[str(lo+F(f)*(up-lo))];cases[f'ground_{s}_width_reduced_{f}']=r
    r=copy.deepcopy(base)
    for i,s in enumerate(shapes[:2]):r[i]['blocks'][0]['eigen_lower']=load(SRC/f'patch_{s}_g1d10.json')['blocks'][0]['eigen_lower']
    cases['rigorous_weighted_ground_candidate']=r;expected={**load(SRC/'diagnostics.json'),**load(SRC/'followup_diagnostics.json')};out={}
    for name,r in cases.items():
        row=scan(r);ex=expected[name];assert row['successes']==ex['successes'],(name,row,ex)
        assert row['best_partial']['beta']==ex['best_partial']['beta'];assert abs(row['best_partial']['min_defect']-ex['best_partial']['min_defect'])<1e-10
        if row['best']:assert row['best']['beta']==ex['best']['beta'] and abs(row['best']['score']-ex['best']['score'])<1e-10
        out[name]=row;print(name,row,flush=True)
    decomp=[]
    for row in expected['trace_decomposition']:
        beta=row['beta'];fresh=[]
        for i,t in [(0,beta),(0,2*beta),(1,2*beta)]:
            _,total,gr,od,tail=trace(base[i],t);fresh.append(dict(N=base[i]['N'],physical_beta=t,ground=gr,odd=od,tail=tail,total_upper=total))
        for x,y in zip(fresh,row['patches']):
            for k in x:assert abs(x[k]-y[k])<1e-10
        decomp.append(dict(beta=beta,patches=fresh))
    return dict(status='PASS_independent_conditional_float_scan',cases=out,trace_decomposition=decomp,grid='301 beta points from 5 to 20 inclusive, step .05; initial row plus at most 10 advances',physical_certificate=False,all_beta_exclusion=False,seconds=time.monotonic()-start)
if __name__=='__main__':
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('scan_result.json');out.write_text(json.dumps(main(),indent=2)+'\n')
