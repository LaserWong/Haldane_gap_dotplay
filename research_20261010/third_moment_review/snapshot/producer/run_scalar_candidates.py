"""Exact .09 candidate replays; .10 bounded floating proposal. Audit required."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys,json,copy,math,hashlib,shutil,time
from fractions import Fraction as F
from pathlib import Path
from exact_filter import HERE,RES
sys.dont_write_bytecode=True
BAND=HERE.parent;OUT=HERE/'scalar_candidates';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(BAND/'frontier_g009'))
import scan_joint as S

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def serial(x):return S.serial(x)
def original_paths(tag):
    base=BAND/'frontier_g009' if tag=='g9d100' else BAND/'combined_ground_bounds'/'combined'
    prefix='combined_patch' if tag=='g9d100' else 'patch'
    return [base/f'{prefix}_{nx}x{ny}_{tag}.json' for nx,ny in ((4,4),(8,4),(8,8))]

def inputs(tag,kind):
    paths=original_paths(tag);base=[json.loads(p.read_text()) for p in paths]
    trialpath=HERE/f'{kind}_8x8_{tag}.json';trial=json.loads(trialpath.read_text());recs=copy.deepcopy(base)
    # txy uses 4x4 and 8x4 denominator upper traces only; 8x8 is numerator only.
    recs[2]['blocks']=[copy.deepcopy(base[2]['blocks'][0])]
    recs[2]['blocks'][0]['eigen_upper']=[trial['shifted_rayleigh_upper']]
    assert recs[:2]==base[:2] and recs[2]['blocks'][0]['eigen_lower']==base[2]['blocks'][0]['eigen_lower']
    assert recs[2]['blocks'][0]['multiplicity']==1 and len(recs[2]['blocks'][0]['eigen_upper'])==1
    sources={str(p.relative_to(RES)):sha(p) for p in paths+[trialpath]}
    for path in paths:
        dest=OUT/f'denominator_snapshot_{path.name}'
        if dest.exists():assert dest.read_bytes()==path.read_bytes()
        else:shutil.copyfile(path,dest)
    for i,(nx,ny) in enumerate(((4,4),(8,4),(8,8))):
        path=OUT/f'input_{kind}_{nx}x{ny}_{tag}.json';path.write_text(json.dumps(recs[i],indent=2)+'\n')
    return recs,sources

def propose(recs):
    proposals=[];best_partial=None
    for bi in range(100,401):
        beta=F(bi,20);st=S.stages(recs,float(beta),'txy');rows,status=S.sequence(st,float(beta),'txy',False)
        if status=='accepted_small_defect':
            last=rows[-1];score=math.log(1/(32*last['u']))/last['beta'];proposals.append((score,beta))
        rank=(len(rows),-min((r['u'] for r in rows),default=1),st['positive_steps'])
        if best_partial is None or rank>best_partial[0]:best_partial=(rank,beta,status,st)
    return sorted(proposals,reverse=True),dict(beta=str(best_partial[1]),sequence_status=best_partial[2],initial=serial(best_partial[3]))

def ladder_labels(n,beta,order):
    state=[n,n,F(beta)];out=[]
    for axis in order:
        i={'x':0,'y':1,'t':2}[axis];target=state[:];target[i]*=2
        out.append(dict(axis=axis,base=[state[0],state[1],str(state[2])],endpoint=[target[0],target[1],str(target[2])]))
        state=target
    return out

def main():
    shortpath=BAND/'frontier_g007_g010'/'short_sizes'/'uniform_short_sizes.json'
    shutil.copyfile(shortpath,OUT/'short_L2_through_L7.json');short=F(json.loads(shortpath.read_text())['gap_lower'])
    summary=[]
    for tag in ('g9d100','g1d10'):
        for kind in ('filtered','enlarged'):
            start=time.monotonic();recs,sources=inputs(tag,kind);proposals,partial=propose(recs)
            result=dict(status='candidate_not_independently_audited',g=recs[0]['g'],variant=kind,
              numerator_retained_states=1,largest_trial_max_triplet_number=6,
              smaller_seed_denominators_byte_identical_to_source=True,
              all_denominator_ground_lower_bounds_unchanged=True,no_new_residual_claim=True,
              beta_grid='5..20 step .05; txy joint, at most 10 cycles',successful_float_grid_points=len(proposals),
              best_float_proposals=[dict(score=a,beta=str(b)) for a,b in proposals[:10]],best_partial_float=partial,
              source_sha256=sources|{str(shortpath.relative_to(RES)):sha(shortpath)})
            if tag=='g9d100':
                result['exact_attempts']=[]
                for _,beta in proposals[:5]:
                    try:exact=S.exact_record(recs,beta,'txy',short)
                    except AssertionError:
                        result['exact_attempts'].append(dict(beta=str(beta),status='exact_replay_or_window_assertion_failed'));continue
                    for st in exact['states']:
                        n=st['n'];bb=F(st['beta']);st['canonical_edge_labels']=ladder_labels(n,bb,'xyt')
                        st['raw_edge_labels']=ladder_labels(n,bb,'txy') if st['raw'] else None
                        st['physical_base']=[n,n,str(bb)]
                        st['completed_cycles_after_seed']=st['cycle']
                    for w in exact.get('windows',[]):
                        w['scope']='Every integer L,W in [n,through], at the stated physical beta'
                        w['included_in_final_minimum']=w['n']<exact['states'][-1]['n']
                    if exact.get('accepted'):
                        last=exact['states'][-1]
                        exact['coverage']=dict(short_integer_sides=[2,7],first_dyadic_window_starts=8,
                           all_early_windows=[[w['n'],w['through']] for w in exact['windows'] if w['included_in_final_minimum']],
                           asymptotic_all_integer_sides_from=last['n'],terminal_physical_beta=last['beta'],
                           no_missing_early_window=True)
                        expected=8
                        for lo,hi in exact['coverage']['all_early_windows']:assert lo==expected;expected=hi
                        assert expected==last['n']
                    result['exact_attempts'].append(exact)
                    if exact.get('accepted'):
                        result['accepted_candidate']=True;result['all_integer_L_ge2_gap']=exact['all_integer_L_ge2_gap'];result['gap_display']=exact['all_integer_gap_display'];break
                if not result.get('accepted_candidate'):result['accepted_candidate']=False
            else:
                result['status']='bounded_float_proposal_only_not_an_all_temperature_exclusion'
            result['seconds']=time.monotonic()-start
            path=OUT/f'candidate_{kind}_{tag}.json';path.write_text(json.dumps(result,indent=2)+'\n')
            row=dict(g=tag,variant=kind,float_successes=len(proposals),exact_accepted=result.get('accepted_candidate'),gap_display=result.get('gap_display'),file=path.name)
            summary.append(row);print(json.dumps(row),flush=True)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':main()
