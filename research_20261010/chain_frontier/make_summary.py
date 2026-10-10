"""Collect exact endpoints and resource/acceptance metadata without recalculation."""
from pathlib import Path
import json,hashlib,datetime
from fractions import Fraction as F
D=Path(__file__).resolve().parent

def main():
    grounds=[]
    for p in sorted(D.glob('*_ground.json')):
        r=json.loads(p.read_text());item={k:r.get(k) for k in ['status','N_dimers','support_depth','full_dimension','retained_states','trial_subspace_dimension','reached_support_dimension','ground_lower','ground_upper','second_eigenvalue_lower','exact_rayleigh','exact_residual_squared','ground_width_display','total_seconds','peak_process_rss_kib','trial_artifact']};item.update(source=p.name,g=r['relative_form_bound']['local_certificate']['coupling'],source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),gap_separation_display=float(F(r['second_eigenvalue_lower'])-F(r['exact_rayleigh'])));grounds.append(item)
    seeds=[]
    for p in sorted(D.glob('chain_sparse*.json')):
        r=json.loads(p.read_text())
        if 'seeds' in r:
            good=[x for x in r['seeds'] if x['bootstrap']['status'].startswith('accepted')];seeds.append(dict(source=p.name,g=r.get('g'),n=r.get('n'),depth=r.get('depth'),cancelled_first_step=p.stem.endswith('_correlated'),accepted_count=len(good),rejected_count=len(r['seeds'])-len(good),best=r.get('best'),tested_betas=[x['beta'] for x in r['seeds']]))
    bridges=[dict(source=p.name,**{k:v for k,v in json.loads(p.read_text()).items() if k in ['status','g','best']}) for p in sorted(D.glob('*_bridges.json'))]
    obs=[dict(source=p.name,**{k:v for k,v in json.loads(p.read_text()).items() if k in ['status','g','n','depth','all_beta_all_a_excluded','tail_beta_from','unresolved_intervals','delta_upper','curvature_lower']}) for p in sorted(D.glob('*_obstruction.json'))]
    out=dict(updated_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='exact_producer_candidates_and_obstructions; see separate independent audit before theorem promotion',grounds=grounds,seed_scans=seeds,all_size_bridges=bridges,obstructions=obs)
    (D/'frontier_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    manifest={str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts}
    (D/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('saved summary',len(grounds),'ground records',len(seeds),'seed scans',len(bridges),'bridges',len(obs),'obstruction records')
if __name__=='__main__':main()
