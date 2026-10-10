"""Structural and exact interval checks, separate from independent review."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
HERE=Path(__file__).resolve().parent;RESEARCH=HERE.parents[1]


def main():
    patches=records=accepted=ground_only=0
    for variant in ('combined','filter_only'):
        directory=HERE/variant
        for path in sorted(directory.glob('patch_*.json')):
            rec=json.loads(path.read_text());patches+=1
            assert rec['new_trial_residual_claim'] is False
            inputs=rec['recombination_source_sha256']
            for name,sha in inputs.items():
                source=RESEARCH/name
                assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
            basepath=next(RESEARCH/n for n in inputs if Path(n).name.startswith('temple_'))
            base=json.loads(basepath.read_text())
            assert rec['blocks'][1:]==base['blocks'][1:]
            assert rec['number_sector_bins']==base['number_sector_bins']
            assert rec['blocks'][0]['eigen_lower']==base['blocks'][0]['eigen_lower']
            lower=F(rec['blocks'][0]['eigen_lower'][0]);upper=F(rec['blocks'][0]['eigen_upper'][0])
            old=F(base['blocks'][0]['eigen_upper'][0])
            assert lower<=upper<=old
            assert F(rec['ground_width'])==upper-lower
        for file in sorted(directory.glob('combined_g*.json')):
            data=json.loads(file.read_text())
            for rec in data['results']:
                records+=1
                assert all(0<F(rec[k])<=1 for k in ('J1','J2','C0'))
                if not rec.get('accepted'):continue
                accepted+=1
                gap=F(rec['all_integer_L_ge2_gap'])
                assert 0<gap<=F(rec['bootstrap']['uniform_square_gap_lower'])
                assert gap<=F(rec['uniform_small_L2_through_L7_gap'])
                for window in rec['windows']:
                    if window['n']<rec['bootstrap']['n']:
                        assert gap<=F(window['gap_lower'])
                optional=rec.get('largest_ground_only_replay')
                if optional is not None:
                    ground_only+=1
                    assert optional['accepted']
                    assert 0<F(optional['all_integer_L_ge2_gap'])<=gap
    result=dict(status='passed_structural_exact_checks_not_independent_physical_review',
        patch_count=patches,selected_order_records=records,accepted_records=accepted,
        accepted_largest_ground_only_records=ground_only)
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
