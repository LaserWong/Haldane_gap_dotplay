"""Historical extraction only; not the reduced certificate consumer.
This one-time exporter reads previously audited comprehensive source files and
writes strictly G/K-only ground and G/A-only translated-band inputs. The actual
consumer never opens those comprehensive largest-seed files.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RESEARCH=BAND.parent


def main():
    for g in map(F,('3/100','1/25','1/20','3/50')):
        tag=f'g{g}'.replace('/','d')
        physical=BAND/'frontier_g006' if g==F(3,50) else BAND/'translation_band'
        ground=physical if g==F(3,50) else RESEARCH/'large_seed_moments'
        source=ground/f'block1_8x8_{tag}.json';gr=json.loads(source.read_text())
        keys=('nx','ny','N_dimers','s','coupling','E00','gram_common_factor_removed','gram',
              'shifted_hamiltonian_numerator','integer_matrix_denominator','coefficients',
              'trial_subspace_dimension','basis','selected_basis_indices')
        minimal={key:gr[key] for key in keys};minimal.update(
            artifact_role='largest ground Rayleigh input; no squared Hamiltonian or spectral information',
            historical_source=str(source.relative_to(RESEARCH)),historical_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        (HERE/f'largest_ground_{tag}.json').write_text(json.dumps(minimal,indent=2))
        source=physical/f'translated_8x8_{tag}_moments.json';mom=json.loads(source.read_text())
        minimal={key:mom[key] for key in ('nx','ny','N','g','matrix_denominator','column_rule','G','A')}
        minimal.update(artifact_role='largest translated trial Gram/first moment only; no H2 or residual',
            spin_multiplicity=3,historical_source=str(source.relative_to(RESEARCH)),
            historical_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        (HERE/f'largest_triplet_GA_{tag}.json').write_text(json.dumps(minimal,indent=2))
    print('Exported eight minimal largest-seed inputs; consumer uses no historical largest source files.')


if __name__=='__main__':main()
