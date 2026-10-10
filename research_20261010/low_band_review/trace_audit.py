"""Independent exact Taylor/trace/seed/recurrence replay, no producer imports."""
from independent_review import *
from functools import lru_cache

@lru_cache(None)
def exponential_interval(x):
    x=F(x);y=abs(x);n=max(120,3*int(y)+40)
    # Direct powers/factorials are deliberately distinct from producer's term loop.
    poly=sum((y**j/F(math.factorial(j)) for j in range(n+1)),F(0))
    first=y**(n+1)/F(math.factorial(n+1))
    upper=poly+first/(1-y/F(n+2))
    return (poly,upper) if x>=0 else (1/upper,1/poly)

def shifted_trace(rec,beta):
    beta=F(beta);assert beta>=0
    n=rec['N'];alpha=F(rec['relative_form_bound']['alpha']);B=F(rec['relative_form_bound']['B'])
    shift=F(rec['blocks'][0]['eigen_upper'][0]);low=high=F(0)
    for block in rec['blocks']:
        for lo,hi in zip(block['eigen_lower'],block['eigen_upper']):
            low += block['multiplicity']*exponential_interval(-beta*(F(hi)-shift))[0]
            high += block['multiplicity']*exponential_interval(-beta*(F(lo)-shift))[1]
    # Exact implementation-equivalent positive polynomial with outward-rounded x.
    x=exponential_interval(-beta*alpha)[1]
    tail=exponential_interval(beta*(B+shift))[1]*sum((math.comb(n,q)*3**q*x**q for q in range(2,n+1)),F(0))
    if 'number_sector_bins' in rec:
        tail=sum((row['multiplicity']*exponential_interval(-beta*(F(row['lower'])-shift))[1] for row in rec['number_sector_bins']['bins'][2:]),F(0))
    return low,high+tail,tail

def floor_dec(x,digits=15):
    den=10**digits;return F((x*den).__floor__(),den)
def ceil_dec(x,digits=18):
    den=10**digits;return F((x*den).__ceil__(),den)

def recurrence(A,B,C):
    q=[ceil_dec(1-x) for x in [A,B,C]];updates=[]
    for j in range(65):
        if max(q)<=F(1,500):return 'accepted',updates
        if j==64:return 'not_accepted',updates
        for direction in range(3):
            t=1-(1-q[0])**4*(1-q[1])**2*(1-q[2])
            if t>=1:return 'bound_left_purity_domain',updates
            v=ceil_dec(t*t/(2*(1-t)**2))
            if v>=1:return 'bound_left_purity_domain',updates
            q=q[1:]+[v]
        updates.append({'round':j+1,'defects':list(map(str,q))})

def main():
    paths=[SRC/f'bilayer_{shape}_g3d100_low_band.json' for shape in ['2x2','4x2','4x4']]
    recs=[json.loads(p.read_text()) for p in paths]
    source_results=json.loads((OUT/'independent_results.json').read_text())
    assert all(hashlib.sha256(path.read_bytes()).hexdigest()==rr['source_sha256'] for path,rr in zip(paths,source_results['records']))
    seedpath=SRC/'full_low_band_seed_g3d100.json';saved=json.loads(seedpath.read_text());rows=[]
    for row in saved['seeds']:
        beta=F(row['beta']);qt=[shifted_trace(r,beta) for r in recs];qt2=shifted_trace(recs[2],2*beta)
        shifts=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
        A=floor_dec(exponential_interval(-beta*(shifts[1]-2*shifts[0]))[0]*qt[1][0]/qt[0][1]**2)
        B=floor_dec(exponential_interval(-beta*(shifts[2]-2*shifts[1]))[0]*qt[2][0]/qt[1][1]**2)
        C=floor_dec(qt2[0]/qt[2][1]**2)
        assert all(x==F(row[key]) for key,x in zip(['A','B','C'],[A,B,C]))
        status,updates=recurrence(A,B,C)
        assert status==row['bootstrap']['status'] and updates==row['bootstrap']['updates']
        rows.append(dict(beta=str(beta),seed_input_equality=True,recurrence_equality=True,status=status,
                         seed_inputs=list(map(str,[A,B,C])),trace_intervals_display=[[float(a),float(b)] for a,b,_ in qt]))
        print('EXACT SEED PASS',beta,status,flush=True)
    zero_checks=[]
    for rec in recs:
        lo,hi,tail=shifted_trace(rec,F(0))
        assert lo==1+3*rec['N'] and hi==4**rec['N'] and tail==4**rec['N']-1-3*rec['N']
        zero_checks.append(dict(N=rec['N'],lower=str(lo),upper=str(hi),tail=str(tail)))
    report=dict(status='passed_independent_exact_trace_and_seed_replay',seeds_source_sha256=hashlib.sha256(seedpath.read_bytes()).hexdigest(),
                beta_zero_count_checks=zero_checks,rows=rows)
    (OUT/'trace_results.json').write_text(json.dumps(report,indent=2))
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[seedpath]}
    for rec in recs:
        for b in rec['blocks']:
            p=SRC/b['trial_file'];manifest[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    (OUT/'reviewed_input_manifest.json').write_text(json.dumps(manifest,indent=2))

if __name__=="__main__":main()
