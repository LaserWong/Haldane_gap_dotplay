#!/usr/bin/env python3
"""Independent open-cluster witness, exact work counts, and integer bounds."""
from pathlib import Path
from fractions import Fraction as F
import math,json,hashlib,time
from audit_exact import ceilsqrt,expbounds,Q
ROOT=Path(__file__).resolve().parent;SNAP=ROOT/'snapshot_initial'
BASE=ROOT.parents[1]

def open8():
    source=BASE/'upstream/extracted/cases/spin2_campaign/higher_inputs'
    rec=json.loads((source/'open8_m0.json').read_text());path=source/rec['vector_file']
    q=json.loads(path.read_text());lower=F(rec['lower']);pw=[5**j for j in range(8)]
    # Independent row-oriented application, rather than scattering columns.
    states=[]
    for c in range(5**8):
        r=tuple(c//p%5 for p in pw)
        if sum(r)==16:states.append((c,r))
    assert len(states)==len(q)==38165 and min(q)>0
    lookup={c:i for i,(c,r) in enumerate(states)};margin=None;edges=0
    for i,(code,r) in enumerate(states):
        value=2*sum((r[k]-2)*(r[k+1]-2) for k in range(7))*q[i]
        for k in range(7):
            a,b=r[k:k+2]
            if a>0 and b<4:
                value-=(5-a)*(b+1)*q[lookup[code-pw[k]+pw[k+1]]];edges+=1
            if a<4 and b>0:
                value-=(a+1)*(5-b)*q[lookup[code+pw[k]-pw[k+1]]];edges+=1
        residual=value*lower.denominator-2*lower.numerator*q[i]
        margin=residual if margin is None else min(margin,residual)
    assert margin>=0 and lower/7>F(-39,8)
    old=json.loads((SNAP/'cluster_verification.json').read_text())
    assert str(margin)==old['minimum_integer_margin']
    assert edges==old['integer_offdiagonal_edges']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==old['source_vector_sha256']
    return {'dimension':len(q),'offdiagonal_edges':edges,'minimum_integer_margin':str(margin),'lower':str(lower),'per_bond':str(lower/7),'strictly_above_minus_39_over_8':True,'witness_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def multiply(a,b):
    d={}
    for i,x in a.items():
        for j,y in b.items():d[i+j]=d.get(i+j,0)+x*y
    return d

def work(n):
    dims={0:1}
    for _ in range(n):dims=multiply(dims,{i:1 for i in range(-2,3)})
    fixed={m:0 for m in dims};flipfixed=0
    for reflection in [False,True]:
        for t in range(n):
            perm=[(t-i if reflection else t+i)%n for i in range(n)]
            remaining=set(range(n));lengths=[]
            while remaining:
                i=min(remaining);cy={i};j=perm[i]
                while j!=i:cy.add(j);j=perm[j]
                remaining-=cy;lengths.append(len(cy))
            poly={0:1}
            for k in lengths:poly=multiply(poly,{k*m:1 for m in range(-2,3)})
            for m,v in poly.items():fixed[m]+=v
            flipfixed+=5**sum(k%2==0 for k in lengths)
    rest={0:1}
    for _ in range(n-2):rest=multiply(rest,{i:1 for i in range(-2,3)})
    moves=multiply(rest,multiply({i:1 for i in range(-2,2)},{i:1 for i in range(-1,3)}))
    out=[]
    for m in range(0,-2*n-1,-1):
        numerator=fixed[m]+(flipfixed if m==0 else 0);denominator=(4 if m==0 else 2)*n
        reps,rem=divmod(numerator,denominator);assert rem==0
        edges=dims[m]+2*n*moves.get(m,0)
        out.append({'M':m,'dimension':dims[m],'representatives':reps,'stored_edges':edges,'weight_sum':dims[m]*(1 if m==0 else 2)})
    return out

def integer_ranges():
    # More conservative than the actual largest magnetization block.
    d=5**10;ds=ceilsqrt(d);eta=(7*ds+1)//2;K=640
    B=2*(Q+eta*(K*(K+1)//2+K+2))
    # Diagonal <=512+(40+32)L, each of <=2L offdiagonals has component row-L1 <=96.
    R=512+(40+32)*10+2*10*96
    high=R*(B//256+2)+B;low=R*511
    assert B<2**58 and R*B<2**100 and R*B//256+B+2<2**63-1
    assert high<2**63-1 and low<2**63-1
    assert 672*B*B<2**127 and Q*B<2**127
    # Exhaust the actual extreme-value pattern in the high/low identity.
    xs=[0,1,-1,B,-B]+[s*(2**b+k) for b in [8,9,56,57] for k in [-1,0,1] for s in [-1,1]]
    checks=0
    for bits in [8,9]:
        den=1<<bits
        for a in [-1232,-96,-48,-24,-16,-8,-1,0,1,8,16,24,48,96,1232]:
            for x in xs:
                h=x>>bits;l=x&(den-1)
                assert x==den*h+l and 0<=l<den
                assert (a*x)//den==a*h+(a*l)//den
                checks+=1
    return {'max_dimension_used':d,'max_degree':K,'eta_prime':eta,'coordinate_bound':str(B),'universal_row_l1_bound':R,'max_split_high_and_subtraction':str(high),'max_split_low':low,'max_norm_chunk_abs':str(672*B*B),'all_signed_bounds_pass':True,'extreme_split_checks':checks}

def archived_matrices():
    results=[]
    for tw in ['I','P','C']:
        path=SNAP/f'original_dependencies/thermal4_{tw}.txt'
        data=iter(map(int,path.read_text().split()));assert next(data)==9;entries=0
        for magnetization in range(9):
            states=[(code,tuple(code//5**k%5 for k in range(4))) for code in range(625) if sum(code//5**k%5 for k in range(4))==8+magnetization]
            loc={code:i for i,(code,w) in enumerate(states)}
            d,mult,nnz=next(data),next(data),next(data)
            assert d==len(states) and mult==(1 if magnetization==0 else 2)
            actual={}
            for _ in range(nnz):
                i,j,a,b=next(data),next(data),next(data),next(data)
                assert (i,j) not in actual;actual[i,j]=(a,b)
            expected={}
            def put(i,j,a,b=0):
                c,e=expected.get((i,j),(0,0));expected[i,j]=(a+c,b+e)
            for j,(code,w) in enumerate(states):
                put(j,j,-4-2*sum((w[k]-2)*(w[(k+1)%4]-2) for k in range(4)))
                for k in range(4):
                    ell=(k+1)%4
                    for direction in [-1,1]:
                        if not(0<=w[k]+direction<=4 and 0<=w[ell]-direction<=4):continue
                        i=loc[code+direction*(5**k-5**ell)]
                        h=(4-w[k])*w[ell] if direction==1 else w[k]*(4-w[ell])
                        if ell!=0 or tw=='I':put(i,j,-h)
                        elif tw=='P':put(i,j,h)
                        elif direction==1:put(i,j,0,-h)
                        else:put(i,j,h,h)
            expected={key:value for key,value in expected.items() if value!=(0,0)}
            assert actual==expected,(tw,magnetization)
            entries+=nnz
        assert next(data,None) is None
        results.append({'twist':tw,'sectors':9,'exact_matrix_entries_verified':entries,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    return results

def main():
    start=time.monotonic();out={'open8':open8(),'integer_ranges':integer_ranges(),'archived_GMP_input_matrices':archived_matrices(),'sizes':{}}
    oldwork=json.loads((SNAP/'results/exact_work_counts.json').read_text())
    oldbudget=json.loads((SNAP/'results/cost_error_budget.json').read_text())
    A=F(json.loads((SNAP/'results/coefficient_audit.json').read_text())['chebyshev']['weighted_recurrence_error'])
    for n in [3,4,8,9,10]:
        rows=work(n);prior=oldwork[str(n)]['rows']
        for r,p in zip(rows,prior):
            for key,value in r.items():assert value==p[key],(n,key,value,p[key])
        assert len(rows)==len(prior) and sum(r['weight_sum'] for r in rows)==5**n
        result={'hilbert_dimension':5**n,'all_dimensions_orbits_edges_match':True,'representatives':sum(r['representatives'] for r in rows),'column_edges':sum(r['representatives']*r['stored_edges'] for r in rows)}
        if n in [9,10]:
            e2=0
            for r,p in zip(rows,oldbudget[str(n)]['exact_work']['rows']):
                eta=(5*ceilsqrt(r['dimension'])+1)//2;E=75+math.ceil(eta*(A+137))
                assert E==p['column_error_numerator'];e2+=r['weight_sum']*E*E
            e=ceilsqrt(e2);assert e==oldbudget[str(n)]['frobenius_error_numerator']
            x=8*n*(F(39,8)-F(5951,1250));expup=expbounds(x/2)[1];delta=F(e+1,Q)*expup
            assert delta==F(oldbudget[str(n)]['thermal_norm_error_upper'])
            conditional=20*delta+delta*delta
            assert conditional==F(oldbudget[str(n)]['conditional_trace_error_upper_at_Z_le_100'])
            result.update({'frobenius_error_numerator':e,'thermal_norm_error_upper_display':float(delta),'conditional_error_at_Z_le_100_display':float(conditional),'condition_Z_le_100_not_verified':True})
        out['sizes'][str(n)]=result
    out['elapsed_seconds']=time.monotonic()-start
    (ROOT/'results/independent_bounds_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
