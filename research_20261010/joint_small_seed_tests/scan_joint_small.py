"""Bounded same-support scan with partial-order and square/full-product retention.

No physical vectors or new supports. Floating proposals are diagnostic only.
Selected points are replayed with directed rational arithmetic.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[name] = '1'
import sys, resource, json, math, hashlib, time
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations, combinations
sys.dont_write_bytecode = True
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
if hasattr(os, 'sched_setaffinity'):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
HERE = Path(__file__).resolve().parent
RES = HERE.parent
ROOT = RES.parent
sys.path.insert(0, str(RES/'low_band_review'))
from fast_exp import exp_interval
ORDERS = tuple(permutations(range(3)))
SCALE = 2**256
HASHES = {}


def read(path):
    HASHES[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())


def serial(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [serial(v) for v in x]
    return x


def down(x):
    x = F(x)
    return F(x.numerator*SCALE//x.denominator, SCALE)


def root(x):
    x = F(x)
    return F(math.isqrt(x.numerator*SCALE*SCALE//x.denominator), SCALE)


def G(z):
    assert 0 < z <= 1
    return 1-(1-z)**2/(2*z*z)


class Arithmetic:
    def __init__(self, exact):
        self.exact = exact
        self.zero = F(0) if exact else 0.0
        self.rnd = down if exact else lambda x: x
        self.sqrt = root if exact else math.sqrt


def fresh(ar):
    return {'edges': {(s,i): ar.zero for s in range(8) for i in range(3) if not s&(1<<i)},
            'squares': {(s, (1<<i)|(1<<j)): ar.zero for i,j in combinations(range(3),2)
                        for s in range(8) if not s&((1<<i)|(1<<j))},
            'joint': ar.zero}


def ladder(st, order):
    s = 0; out = []
    for i in order:
        out.append(st['edges'][s,i]); s |= 1<<i
    return out


def closure(st, ar, sweeps=16):
    """Monotone finite closure, never an assumption of an attained exact tuple."""
    e,q = st['edges'],st['squares']
    def put(d,k,v):
        v=ar.rnd(v)
        if v>d[k]: d[k]=v; return True
        return False
    count=0
    for _ in range(sweeps):
        changed=False
        for (s,mask), old in q.items():
            i,j=[k for k in range(3) if mask&(1<<k)]
            changed |= put(q,(s,mask),max(e[s,i]**2*e[s|(1<<i),j],
                                        e[s,j]**2*e[s|(1<<j),i]))
            value=q[s,mask]
            for a,b in ((i,j),(j,i)):
                changed |= put(e,(s,a),ar.sqrt(value))
                changed |= put(e,(s|(1<<a),b),value)
        k=st['joint']
        for i,j,h in ORDERS:
            k=max(k,e[0,i]**4*q[1<<i,(1<<j)|(1<<h)],
                  q[0,(1<<i)|(1<<j)]**2*e[(1<<i)|(1<<j),h])
        k=ar.rnd(k)
        if k>st['joint']: st['joint']=k;changed=True
        for i,j,h in ORDERS:
            changed |= put(q,(0,(1<<i)|(1<<j)),ar.sqrt(k))
            changed |= put(q,(1<<i,(1<<j)|(1<<h)),k)
        count+=1
        if not changed:break
    st['closure_sweeps']=count
    assert 0<=st['joint']<=1
    assert all(0<=x<=1 for x in e.values())
    return st


def advance(st, ar):
    """Every fixed-order joint update, with partial outputs retained in one cube."""
    out=fresh(ar); routes=[]
    for i,j,h in ORDERS:
        d=ar.zero; ee=ar.zero; ff=ar.zero
        z1=st['joint']
        if z1<=0:
            routes.append({'order':[i,j,h], 'arguments':[z1], 'outputs':[], 'positive_steps':0})
            continue
        d=ar.rnd(G(z1)); args=[z1]; vals=[d]
        if d>0:
            out['edges'][0,i]=max(out['edges'][0,i],d)
            z2=ar.rnd(st['squares'][1<<i,(1<<j)|(1<<h)]**2*d)
            ee=ar.rnd(G(z2));args.append(z2);vals.append(ee)
            if ee>0:
                out['edges'][1<<i,j]=max(out['edges'][1<<i,j],ee)
                z3=ar.rnd(st['edges'][(1<<i)|(1<<j),h]**4*d*d*ee)
                ff=ar.rnd(G(z3));args.append(z3);vals.append(ff)
                if ff>0:out['edges'][(1<<i)|(1<<j),h]=max(out['edges'][(1<<i)|(1<<j),h],ff)
        routes.append({'order':[i,j,h], 'arguments':args, 'outputs':vals,
                       'positive_steps':sum(v>0 for v in vals)})
    return closure(out,ar), routes


def data(g):
    out=[]
    for shape,n in [('2x2',4),('4x2',8),('4x4',16)]:
        r=read(RES/'low_band'/'frontier'/f'bilayer_{shape}_g{g}_symmetric_number_low_band.json')
        assert r['N']==n and r['full_hilbert_dimension']==4**n
        b=F(r['blocks'][0]['eigen_upper'][0]);low=[];up=[]
        for block in r['blocks']:
            for l,u in zip(block['eigen_lower'],block['eigen_upper']):
                assert F(l)<=F(u)
                low.append((F(u)-b,block['multiplicity']))
                up.append((F(l)-b,block['multiplicity']))
        for row in r['number_sector_bins']['bins'][2:]:
            up.append((F(row['lower'])-b,row['multiplicity']))
        assert sum(m for _,m in low)==1+3*n
        assert sum(m for _,m in up)==4**n
        out.append({'E':F(r['energy_shift'])+b,'lower':low,'upper':up})
    return out


def trace(d,beta,exact):
    if exact:
        lo=sum(m*exp_interval(-beta*x)[0] for x,m in d['lower'])
        hi=sum(m*exp_interval(-beta*x)[1] for x,m in d['upper'])
    else:
        lo=sum(m*math.exp(-beta*float(x)) for x,m in d['lower'])
        hi=sum(m*math.exp(-beta*float(x)) for x,m in d['upper'])
    return lo,hi


def initial(dat,beta,ar):
    traces={};energies={}
    for s in range(8):
        n=(s&1>0)+(s&2>0)
        b=beta*(2 if s&4 else 1)
        traces[s]=trace(dat[n],b,ar.exact)
        energies[s]=b*(dat[n]['E'] if ar.exact else float(dat[n]['E']))
    def ratio(s,t,power):
        exponent=power*energies[s]-energies[t]
        exp=exp_interval(exponent)[0] if ar.exact else math.exp(exponent)
        v=ar.rnd(exp*traces[t][0]/traces[s][1]**power)
        assert v<=1+(0 if ar.exact else 1e-12)
        return min(1,v)
    st=fresh(ar)
    for s,i in st['edges']:st['edges'][s,i]=ratio(s,s|(1<<i),2)
    for s,mask in st['squares']:st['squares'][s,mask]=ratio(s,s|mask,4)
    st['joint']=ratio(0,7,8)
    return closure(st,ar)


def record(st,cycle,beta):
    return {'cycle':cycle,'spatial_base':[2*2**cycle]*2,'beta':beta*2**cycle,
            'joint':st['joint'], 'canonical':ladder(st,(0,1,2)),
            'edges':{f'{s}:{i}':v for (s,i),v in st['edges'].items()},
            'squares':{f'{s}:{m}':v for (s,m),v in st['squares'].items()},
            'closure_sweeps':st['closure_sweeps']}


def run(dat,beta,exact=False,max_cycles=16):
    ar=Arithmetic(exact);st=initial(dat,beta,ar);rows=[record(st,0,beta)]
    for cycle in range(1,max_cycles+1):
        nxt,routes=advance(st,ar);rows[-1]['routes_to_next']=routes
        if not any(x>0 for x in nxt['edges'].values()):
            return {'status':'no_positive_next_first_edge','states':rows,'failed_cycle':cycle}
        st=nxt;rows.append(record(st,cycle,beta))
        if min(ladder(st,(0,1,2)))>=F(499,500):
            return {'status':'small_defect_candidate_requires_all_integer_bridges','states':rows}
        if st['joint']<=0:
            return {'status':'no_positive_full_joint_after_partial_transport','states':rows}
    return {'status':'bounded_cycle_limit','states':rows}


def main():
    start=time.monotonic()
    physical=read(RES/'small_seed_exclusion_review'/'physical_results.json')
    acceptance=read(RES/'small_seed_exclusion_review'/'ACCEPTANCE.json')
    assert acceptance['physical_result_sha256']==HASHES[str((RES/'small_seed_exclusion_review'/'physical_results.json').relative_to(ROOT))]
    assert 'PASS' in physical['status']
    output={'status':'bounded_diagnostic_only','grid':{'beta_start':'1','beta_end':'60','step':'1/40','points':2361},
            'max_cycles':16,'max_closure_sweeps_per_cube':16,'new_physical_supports':False,
            'new_physical_vectors':False,'all_beta_exclusion':False,'couplings':{}}
    for g in ('1d25','1d20'):
        dat=data(g)
        scores=[];positive={''.join('xyt'[i] for i in p):0 for p in ORDERS};best=None
        for bi in range(40,2401):
            beta=F(bi,40);r=run(dat,float(beta));rows=r['states']
            for p in rows[0]['routes_to_next']:
                if p['positive_steps']==3:positive[''.join('xyt'[i] for i in p['order'])]+=1
            k=rows[1]['joint'] if len(rows)>1 else 0
            rank=(k,rows[0]['joint'])
            if best is None or rank>best[0]:best=(rank,beta)
            scores.append({'beta':str(beta),'status':r['status'],'first_full_joint':k,'states':len(rows)})
            if r['status'].startswith('small_defect'):raise RuntimeError(('CANDIDATE NEEDS EXACT BRIDGES',g,beta))
        selected={best[1],F(87,10),F(77,10),F(67,10)}
        exacts=[]
        for beta in sorted(selected):
            ex=run(dat,beta,True);ex['beta_initial']=beta;exacts.append(ex)
        output['couplings'][g]={'positive_fixed_first_cycles':positive,'best_beta':best[1],
             'max_float_first_full_joint':best[0][0],'exact_selected':exacts,
             'grid_results':scores,'successful_float_candidates':0}
        print(g,'best',best,'positive',positive,'exact',[(x['beta_initial'],x['status'],
              float(x['states'][1]['joint']) if len(x['states'])>1 else 0) for x in exacts],flush=True)
    for name,expected in physical['input_sha256'].items():
        if name in HASHES:assert HASHES[name]==expected
    for path in (HERE/'scan_joint_small.py',RES/'low_band_review'/'fast_exp.py',
                 RES/'joint_ratio_review'/'GENERAL_LEMMA.md'):
        HASHES[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    output.update(input_sha256=HASHES,seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  limits={'cpu':1,'address_space_bytes':1024**3})
    (HERE/'results.json').write_text(json.dumps(serial(output),indent=2)+'\n')
    print('DONE',output['seconds'],output['peak_rss_kib'],flush=True)


if __name__=='__main__':main()
