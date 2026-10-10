"""Independent exact correlated xyt cancellation and successful recurrence."""
from independent_review import *
from trace_audit import exponential_interval,shifted_trace,floor_dec,ceil_dec,recurrence

def purification_lower(x):
    assert 0<x<=1
    return 1-(1-x)**2/(2*x*x)

def logarithm_lower(x):
    assert x>1
    k=0
    while x>=2:x/=2;k+=1
    def atanh(y):
        z=(y-1)/(y+1)
        return sum((2*z**(2*j+1)/F(2*j+1) for j in range(80)),F(0))
    return k*atanh(F(2))+atanh(x)

src=SRC/'symmetric_correlated_beta909d100_FINAL.json';data=json.loads(src.read_text())
recs=[json.loads((SRC/f'bilayer_{s}_g3d100_symmetric_number_low_band.json').read_text()) for s in ['2x2','4x2','4x4']]
verification=json.loads((OUT/'symmetric_ground_results.json').read_text())
assert len(verification['records'])==3
for s,v in zip(['2x2','4x2','4x4'],verification['records']):
    p=SRC/f'bilayer_{s}_g3d100_symmetric_number_low_band.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==v['updated_band_sha256']
reports=[]
# xyt only: other staircase orders are not used to assert the inherited theorem.
for saved in data:
    if saved['order']!='xyt':continue
    beta=F(saved['beta_initial']);e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
    q4=shifted_trace(recs[0],beta);q8=shifted_trace(recs[1],beta)
    q16=shifted_trace(recs[2],beta);q16double=shifted_trace(recs[2],2*beta)
    J1=floor_dec(exponential_interval(-2*beta*e[2]+8*beta*e[0])[0]*q16double[0]/q4[1]**8,16)
    J2=floor_dec(exponential_interval(-4*beta*e[2]+8*beta*e[1])[0]*q16double[0]**2/q8[1]**8,16)
    C=floor_dec(q16double[0]/q16[1]**2,16)
    assert [J1,J2,C]==[F(saved[k]) for k in ['J1','J2','C']]
    A1=floor_dec(purification_lower(J1),16)
    B1=floor_dec(purification_lower(J2*A1),16)
    C1=floor_dec(purification_lower(C**4*A1**2*B1),16)
    assert all(x>0 for x in [A1,B1,C1])
    assert list(map(str,[A1,B1,C1]))==saved['first_purities']
    status,updates=recurrence(A1,B1,C1)
    assert status=='accepted' and updates==saved['bootstrap']['updates']
    rounds=len(updates);q=[F(x) for x in updates[-1]['defects']] if updates else [ceil_dec(1-x) for x in [A1,B1,C1]]
    u=max(q);assert u<=F(1,500)
    final_n=4*2**rounds;final_beta=2*beta*2**rounds
    gap=floor_dec(logarithm_lower(1/(32*u))/final_beta,12)
    bs=saved['bootstrap']
    assert final_n==bs['n']==bs['m'] and final_beta==F(bs['beta']) and gap==F(bs['uniform_square_gap_lower'])
    reports.append(dict(beta_initial=str(beta),order='xyt',exact_cancellation_ratios=[str(x) for x in [J1,J2,C]],
                        first_purities=list(map(str,[A1,B1,C1])),all_exact_inputs_and_updates_equal=True,
                        final_n=final_n,final_beta=str(final_beta),gap_lower=str(gap),gap_display=float(gap),
                        scope='Every integer square side L >= final_n, conditional on previously audited transfer/interpolation theorem; shorter sizes require a separate bridge.'))
    print('EXACT CORRELATED PASS',beta,final_n,float(gap),flush=True)
result=dict(status='passed_independent_exact_xyt_trace_and_successful_bootstrap',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),records=reports)
(OUT/'symmetric_correlated_results.json').write_text(json.dumps(result,indent=2))
