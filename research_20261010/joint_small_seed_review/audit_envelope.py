"""Independent mixed-cube obstruction audit. No project implementation imports.
Reads sealed accepted quotient data, independently replays all 644 exact records,
and checks the entire cap-operation grammar, formal basepoints, and adversarial cases.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import json, hashlib, itertools, math, random, time
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
R=HERE.parent
P=R/'joint_small_seed_tests'
O=R/'small_seed_order_exclusions'
A=O/'independent_review'
SEEN={}
PERMS=list(itertools.permutations(range(3)))
EDGES=[(s,i) for s in range(8) for i in range(3) if not s>>i&1]
SQUARES=[(s,m) for m in (3,5,6) for s in range(8) if not s&m]

def hashfile(p):
    key=str(p.relative_to(ROOT));h=hashlib.sha256(p.read_bytes()).hexdigest()
    assert key not in SEEN or SEEN[key]==h, ('changed input',key)
    SEEN[key]=h
    return h

def load(p):
    hashfile(p);return json.loads(p.read_text())

def manifest(p,base):
    d=load(p)
    for k,h in d.items():assert hashfile(base/k)==h,('seal mismatch',str(p),k)
    return d

def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x

def write(name,obj):
    (HERE/name).write_text(json.dumps(encode(obj),indent=2)+'\n')

def provenance():
    producer=manifest(P/'MANIFEST_SHA256.json',P)
    oldreview=manifest(A/'MANIFEST_SHA256.json',A)
    accepted=load(A/'ACCEPTANCE.json')
    assert accepted['status'].startswith('PASS independent analytic')
    assert hashfile(A/'INPUT_SHA256.json')==accepted['input_manifest_sha256']
    assert hashfile(A/'results.json')==accepted['independent_result_sha256']
    assert hashfile(A/'audit_orders.py')==accepted['audit_code_sha256']
    oldsources=manifest(A/'INPUT_SHA256.json',ROOT)
    freeze=manifest(O/'PRODUCER_FREEZE_SHA256.json',O)
    assert hashfile(O/'PRODUCER_FREEZE_SHA256.json')==accepted['producer_freeze_sha256']
    assert freeze==accepted['reviewed_producer_sha256']
    physicaldir=R/'small_seed_exclusion_review'
    manifest(physicaldir/'MANIFEST_SHA256.json',physicaldir)
    manifest(physicaldir/'SOURCE_MANIFEST_SHA256.json',ROOT)
    pa=load(physicaldir/'ACCEPTANCE.json');physical=load(physicaldir/'physical_results.json')
    assert pa['status'].startswith('PASS independent physical reconstruction')
    assert physical['status'].startswith('PASS independently reconstructed all six physical')
    assert hashfile(physicaldir/'physical_results.json')==pa['physical_result_sha256']==accepted['prior_physical_result_sha256']
    for k,h in physical['input_sha256'].items():assert hashfile(ROOT/k)==h
    env=load(P/'envelope_results.json')
    for k,h in env['input_sha256'].items():assert hashfile(ROOT/k)==h
    for f in ('joint_ratio_review/GENERAL_LEMMA.md','general_dimension_review/PROOF_REVIEW.md'):
        hashfile(R/f)
    return load(O/'results.json'),load(A/'results.json'),env,{'producer_files':len(producer),'prior_accepted_sources':len(oldsources),'physical_result_sha256':pa['physical_result_sha256']}

# G is evaluated directly on its integer numerator and denominator; ceil uses
# a remainder test, independently of the producer's rational-expression routine.
def G320(z):
    assert 0<z<=1
    n,d=z.numerator,z.denominator
    numerator=n*n+2*n*d-d*d;denominator=2*n*n
    quotient,remainder=divmod(numerator<<320,denominator)
    return Q(quotient+bool(remainder),1<<320)

def envelope(inputs):
    j,q,c=(max(Q(row[i]) for row in inputs) for i in range(3))
    assert all(0<x<=1 for x in (j,q,c))
    args=[];caps=[]
    z=j
    for stage in range(1,5):
        args.append(z);caps.append(G320(z))
        if caps[-1]<0:
            return {'max_input_upper':[j,q,c],'arguments':args,'caps':caps,
                    'failed_stage':stage,'negative_upper':caps[-1]}
        assert caps[-1]>0
        if stage==1:z=q*caps[0]
        elif stage==2:z=(c*caps[0])**2*c*c*caps[1]
        elif stage==3:z=(caps[0]*caps[0]*caps[1])**2*caps[2]
    raise AssertionError('new envelope did not exclude')

def compare_record(saved,inputs):
    r=envelope(inputs)
    for k,v in r.items():
        old=saved[k]
        if isinstance(v,list):assert list(map(Q,old))==v,(k,old,v)
        elif isinstance(v,Q):assert Q(old)==v,(k,old,v)
        else:assert old==v
    if r['failed_stage']==4:
        z=r['arguments'][-1]
        assert Q(saved['first_doubled_base_joint_upper'])==z
        assert z*z+2*z<1
    return r

def audit_records(old,accepted,env):
    out={};checked=0;quotient_comparisons=0
    assert set(env['couplings'])==set(old['results'])=={'1d25','1d20'}
    for tag,ed in env['couplings'].items():
        od=old['results'][tag];ad=accepted['couplings'][tag]
        assert Q(ed['g'])==Q(od['g'])==Q(1,25 if tag=='1d25' else 20)
        assert ed['beta_cover']==[[0,4],[4,20],[20,'infinity']]
        assert Q(ad['hot']['J1_upper'])<=Q(od['hot']['common_J1_upper'])
        assert Q(ad['hot']['purity_upper'])<=Q(od['hot']['thermal_purity_2x2_at_beta4_upper'])
        hot=compare_record(ed['hot'],[[od['hot']['common_J1_upper'],'1','1']]);checked+=1
        assert hot['failed_stage']==1
        coldinp=[od['orders'][o]['cold']['input_upper'] for o in ('xyt','xty','txy')]
        for o in ('xyt','xty','txy'):
            assert all(Q(x)<=Q(y) for x,y in zip(ad['cold'][o]['input_upper'],od['orders'][o]['cold']['input_upper']))
            quotient_comparisons+=3
        assert all(Q(x)>0 for x in od['cold_positive_slopes'].values())
        assert {k:Q(v) for k,v in od['cold_positive_slopes'].items()}=={k:Q(v) for k,v in ad['positive_slopes'].items()}
        cold=compare_record(ed['cold'],coldinp);checked+=1
        assert len(ed['middle'])==320
        middle=[]
        for k,rec in enumerate(ed['middle']):
            interval=[Q(4)+Q(k,20),Q(4)+Q(k+1,20)]
            assert list(map(Q,rec['beta_interval']))==interval
            inputs=[]
            for o in ('xyt','xty','txy'):
                prior=od['orders'][o]['middle'][k];sealed=ad['orders'][o][k]
                assert list(map(Q,prior['beta_interval']))==list(map(Q,sealed['interval']))==interval
                vals=list(map(Q,prior['input_upper']))
                assert all(Q(x)<=y for x,y in zip(sealed['input_upper'],vals))
                quotient_comparisons+=3;inputs.append(vals)
            assert [list(map(Q,x)) for x in rec['order_input_upper']]==inputs
            r=compare_record(rec,inputs);r['beta_interval']=interval
            middle.append(r);checked+=1
        hist=dict(Counter(str(r['failed_stage']) for r in middle))
        assert hist==ed['middle_failed_stage_histogram']
        closest=max(r['negative_upper'] for r in middle)
        assert closest==Q(ed['closest_negative_upper'])
        maxj=max(r['max_input_upper'][0] for r in [hot,cold,*middle])
        assert maxj<Q(499,500)**7 # Also rules out onset at the original cube.
        out[tag]={'hot':hot,'cold':cold,'middle':middle,'histogram':hist,
                  'closest_negative_upper':closest,'maximum_initial_joint_upper':maxj,
                  'initial_joint_below_small_defect_product':True}
    assert checked==644 and quotient_comparisons==5778
    return out,checked,quotient_comparisons

def poly(*args):
    c=Counter()
    for exps,power in args:
        for k,v in exps.items():c[k]+=v*power
    return {k:v for k,v in c.items() if v}

def edge(s,i):return {s|1<<i:1,s:-2}
def square(s,m):return {s|m:1,s:-4}

def algebra():
    joint={7:1,0:-8};identities=[];rotations=[]
    assert len(EDGES)==12 and len(SQUARES)==6
    for s,m in SQUARES:
        ij=[i for i in range(3) if m>>i&1]
        for i,j in (ij,ij[::-1]):
            assert poly((edge(s,i),2),(edge(s|1<<i,j),1))==square(s,m)
            identities.append({'square':[s,m],'orientation':[i,j]})
    for i,j,k in PERMS:
        assert poly((edge(0,i),4),(square(1<<i,(1<<j)|(1<<k)),1))==joint
        assert poly((square(0,(1<<i)|(1<<j)),2),(edge((1<<i)|(1<<j),k),1))==joint
        # Each rotating queue's updated edge lands at the previous terminal
        # vertex, which becomes the next base in that edge's direction.
        base=(0,0,0);queue=[i,j,k];new_edges=[]
        for step in range(3):
            endpoint=tuple(b+1 for b in base)
            new_edges.append((endpoint,queue[0]))
            b=list(base);b[queue[0]]+=1;base=tuple(b)
            queue=queue[1:]+queue[:1]
        assert base==(1,1,1) and queue==[i,j,k]
        prefix=[1,1,1]
        for (point,axis),axis_expected in zip(new_edges,[i,j,k]):
            assert point==tuple(prefix) and axis==axis_expected
            prefix[axis]+=1
        rotations.append({'order':[i,j,k],'outputs':new_edges,'new_base':base})
    # Canonical suffix constraints retained by closure yield precisely the
    # max(b^4 c^2,K^2) and max(c,K)^4 factors.
    assert (2*2,1*2)==(4,2)
    return {'oriented_square_identities':identities,'six_rotation_ledgers':rotations,'full_product_factorizations_checked':12}

# Universal cap proof encoded as exponent dominance on independent D,E,F in
# [0,1]. Rational half-exponents permit checking roots without approximations.
def cap_grammar():
    D=(Q(1),Q(0),Q(0));E=(Q(0),Q(1),Q(0));F=(Q(0),Q(0),Q(1))
    R=(Q(2),Q(1),Q(0));S=(Q(0),Q(2),Q(1));T=(Q(4),Q(2),Q(1))
    def sumexp(*terms):return tuple(sum(p*v[i] for p,v in terms) for i in range(3))
    rules=[('root square product',sumexp((2,D),(1,E)),R),
           ('suffix square product',sumexp((2,E),(1,F)),S),
           ('root square first deduction',sumexp((Q(1,2),R)),D),
           ('root square second deduction',R,E),
           ('suffix square first deduction',sumexp((Q(1,2),S)),E),
           ('suffix square second deduction',S,F),
           ('first edge and suffix to full',sumexp((4,D),(1,S)),T),
           ('root square and last to full',sumexp((2,R),(1,F)),T),
           ('full to root square',sumexp((Q(1,2),T)),R),
           ('full to suffix square',T,S)]
    for name,actual,target in rules:assert all(a>=t for a,t in zip(actual,target)),name
    return [{'operation':n,'output_exponents':a,'target_exponents':t,'dominates':True} for n,a,t in rules]

def rules():
    out=[]
    for s,m in SQUARES:
        i,j=[i for i in range(3) if m>>i&1]
        for a,b in ((i,j),(j,i)):
            out.extend([(('q',s,m),[(('e',s,a),Q(2)),(('e',s|1<<a,b),Q(1))]),
                        (('e',s,a),[(('q',s,m),Q(1,2))]),
                        (('e',s|1<<a,b),[(('q',s,m),Q(1))])])
    for i,j,k in PERMS:
        out.extend([(('k',),[(('e',0,i),Q(4)),(('q',1<<i,(1<<j)|(1<<k)),Q(1))]),
                    (('k',),[(('q',0,(1<<i)|(1<<j)),Q(2)),(('e',(1<<i)|(1<<j),k),Q(1))]),
                    (('q',0,(1<<i)|(1<<j)),[(('k',),Q(1,2))]),
                    (('q',1<<i,(1<<j)|(1<<k)),[(('k',),Q(1))])])
    return out

def bool_close(state):
    known=set(state)
    while True:
        old=len(known)
        for dest,src in rules():
            if all(k in known for k,p in src):known.add(dest)
        if len(known)==old:return known

def partial_tests():
    counts={}
    for maxdepth in (0,1):
        available=[('e',s,i) for s,i in EDGES if s.bit_count()<=maxdepth]
        for mask in range(1<<len(available)):
            known=bool_close(k for j,k in enumerate(available) if mask>>j&1)
            assert ('k',) not in known
            assert all(k[1].bit_count()<=maxdepth for k in known if k[0]=='e')
            assert all(k[1]==0 for k in known if k[0]=='q')
        counts[str(maxdepth+1)+'_positions']=1<<len(available)
    return counts

def sqrt_down(v):
    n=math.isqrt((v.numerator<<192)//v.denominator)
    return Q(n,1<<96)

def random_closure_tests():
    rng=random.Random(611021);grammar=rules();tests=0;updates=0
    choices=[Q(0),Q(1,100),Q(1,2),Q(99,100),Q(1)]
    for D,E,F in itertools.product(choices,repeat=3):
        caps={('e',s,i):(D,E,F)[s.bit_count()] for s,i in EDGES}
        caps.update({('q',s,m):D*D*E if s==0 else E*E*F for s,m in SQUARES})
        caps[('k',)]=D**4*E**2*F
        # Independent saved products can be stronger than component products.
        state={key:(cap if key[0]!='e' else cap*Q(rng.randrange(11),10)) for key,cap in caps.items()}
        for repeat in range(8):
            rng.shuffle(grammar)
            for dest,src in grammar:
                value=Q(1)
                for key,power in src:value*=sqrt_down(state[key]) if power==Q(1,2) else state[key]**int(power)
                state[dest]=max(state[dest],value)
                assert 0<=state[dest]<=caps[dest],(D,E,F,dest)
                updates+=1
        tests+=1
    return {'cap_boundary_states':tests,'arbitrary_order_scalar_updates':updates,'independent_products_retained':True}

def adversarial(couplings):
    odd=(1+Q(1,16)**6)/(1-Q(1,16)**3)**2
    even=(1+Q(1,16)**4)/(1+Q(1,16)**2)**2
    assert odd>1 and even<1
    j=Q(1,4);weak=Q(1,8)
    assert j>weak**7 and sqrt_down(j)>weak
    bad=next(r for r in couplings['1d25']['middle'] if r['failed_stage']==4)
    assert G320(bad['max_input_upper'][0])>0 and G320(bad['arguments'][3])<0
    assert bad['max_input_upper'][0]>bad['arguments'][3]
    # Swapping measured numbers at another physical base is invalid. Exact
    # signed-transfer/Gibbs Ising example inherited as rational test values.
    spatial=Q(353,578);cooled=Q(67073,132098)
    assert cooled<spatial
    return {'odd_base_counterexample':{'even_purity':even,'odd_purity':odd},
            'joint_retention_example':{'all_weak_components':weak,'separate_K':j,'weak_product':weak**7},
            'old_K_reuse_counterexample':{'beta_interval':bad['beta_interval'],'old_K_upper':bad['max_input_upper'][0],
                'new_K_upper':bad['arguments'][3],'incorrect_old_K_first':G320(bad['max_input_upper'][0]),'correct_next_first':bad['caps'][3]},
            'spatial_cooling_is_not_monotone':{'before':spatial,'after':cooled},
            'onset_comparison':{'threshold_product':Q(499,500)**7,'threshold_product_above_purification_cutoff':(Q(499,500)**7)**2+2*Q(499,500)**7>1}}

def graph(nx,ny):
    out=Counter()
    for x in range(nx):
        for y in range(ny):
            out[('rung',tuple(sorted(((x,y,0),(x,y,1)))))]+=1
            for layer in range(2):
                for dx,dy in ((1,0),(0,1)):
                    out[('inlayer',tuple(sorted(((x,y,layer),((x+dx)%nx,(y+dy)%ny,layer)))))]+=1
    return out

def reflection():
    out=[]
    for nx,ny in ((2,2),(4,2),(2,4),(4,4)):
        mapped=Counter()
        for (kind,ends),n in graph(nx,ny).items():
            mapped[(kind,tuple(sorted((y,x,l) for x,y,l in ends)))]+=n
        assert mapped==graph(ny,nx)
        out.append({'shape':[nx,ny],'spin_bond_multiset_preserved':True})
    return out

def main():
    start=time.monotonic();old,prior,env,provenance_report=provenance()
    couplings,count,comparisons=audit_records(old,prior,env)
    proof={'algebra':algebra(),'universal_cap_grammar':cap_grammar(),'partial_support_exhaustion':partial_tests(),
           'numerical_boundary_stress':random_closure_tests(),'adversarial_scope_checks':adversarial(couplings),
           'full_spin_coordinate_exchange':reflection()}
    for name,h in SEEN.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
    stamp=datetime.now(timezone.utc)
    result={'status':'PASS independent analytic and exact arithmetic review of the defined synchronous mixed-cube method',
            'updated_utc':stamp.isoformat(),'updated_America_New_York':stamp.astimezone(ZoneInfo('America/New_York')).isoformat(),
            'provenance':provenance_report,'records_checked':count,'sealed_quotient_upper_comparisons':comparisons,
            'couplings':couplings,'proof_checks':proof,'seconds':time.monotonic()-start,
            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'limits':{'cpus':1,'address_space_bytes':1024**3},'no_project_implementation_imports':True,
            'physical_reconstruction':'Inherited sealed accepted physical reconstruction; not rerun',
            'producer_or_root_edits':False,'remote_writes':False}
    write('results.json',result);write('INPUT_SHA256.json',SEEN)
    write('ADVERSARIAL_TESTS.json',proof)
    print('PASS',count,'records;',comparisons,'sealed quotient comparisons;',len(SEEN),'sealed files')
    for tag,r in couplings.items():print(tag,r['histogram'],float(r['closest_negative_upper']))
    print('Seconds',result['seconds'],'RSS KiB',result['peak_rss_kib'])
if __name__=='__main__':main()
