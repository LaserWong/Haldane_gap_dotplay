import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;RES=HERE.parent
row=json.load(open(RES/'bilayer_seed_error_budget/joint_targets.json'))['results'][0];assert row['g']=='21/200';trial=row['optimized43D_8x4_trial'];c=trial['integer_coefficients'];assert len(c)==43
(HERE/'coefficients.txt').write_text('400 21\n'+'\n'.join(' '.join(map(str,c[a:b])) for a,b in [(1,15),(15,29),(29,43)])+'\n')
(HERE/'trial.json').write_text(json.dumps({'g':'21/200','trial':trial,'target_ground_lower':row['target_ground32_lower'],'residual_squared_budget':row['residual_squared_budget_for_optimized43D_8x4'],'candidate_shifted_rayleigh':row['optimized43D_8x4_rayleigh'],'integer_denominator':400,'integer_A_coefficient':21},indent=2)+'\n')
paths=[RES/'bilayer_seed_error_budget/MANIFEST_SHA256.json',RES/'bilayer_seed_error_budget/joint_targets.json',RES/'bilayer_complete_residual_8x4/residual_scalar',RES/'bilayer_complete_residual_8x4/residual_scalar.cpp',RES/'bilayer_complete_residual_8x4/geometry_8x4.txt']
(HERE/'INITIAL_INPUT_SHA256.json').write_text(json.dumps({str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
