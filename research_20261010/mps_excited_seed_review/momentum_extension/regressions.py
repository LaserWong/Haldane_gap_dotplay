#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent
for folder,manifest in [('inputs','PHYSICAL_MANIFEST_SHA256.json'),('inputs','SCALAR_MANIFEST_SHA256.json'),('inputs70','MANIFEST_SHA256.json')]:
 for name,h in json.loads((P/folder/manifest).read_text())['files'].items():assert hashlib.sha256((P/folder/name).read_bytes()).hexdigest()==h
assert (P/'inputs/local_tensors.json').read_bytes()==(P.parent/'inputs/local_tensors.json').read_bytes()
def raw(name):return {k:int(v) for k,v in (s.split('=') for s in (P/name).read_text().splitlines())}
a=raw('independent_n24_benchmark.out');b=raw('independent_n24_remaining.out');assert not(a.keys()&b.keys());a.update(b);assert len(a)==26
m=json.loads((P/'inputs/exact_matrices_n24.json').read_text());C=list(map(int,m['C_displacements']));K=list(map(int,m['K_displacements']))
for r in range(13):assert a[f'C24_{r}']==C[r] and a[f'K24_{r}']==K[r]
assert sum(C)==sum(K)==0
for row in json.loads((P/'inputs/source_checks_plus.json').read_text())['fixtures']:
 n=row['n'];fixture=raw(f'independent_n{n}.out')
 for r in range(n):assert fixture[f'C{n}_{r}']==int(row['C'][r]) and fixture[f'K{n}_{r}']==int(row['K'][r])
assert json.loads((P/'independent_build.json').read_text())['status']=='PASS'
fourier=json.loads((P/'independent_fourier.json').read_text());assert fourier['Gram_rank']==23 and fourier['zero_global_raising_norm']
for row in fourier['rows'][1:]:
 assert F(row['Gram_eigenvalue_interval'][0])>0
 assert list(map(F,row['unnormalized_fourier_norm_interval']))==[24*F(x) for x in row['Gram_eigenvalue_interval']]
assert json.loads((P/'independent_singlet.json').read_text())['retained_orthogonal_states']==70
for mode,union in [(48,[['533/64','679/64']]),(70,[['539/64','339/32']])]:
 a=json.loads((P/f'independent_scalar{mode}.json').read_text());assert a['inconclusive_closed_unions']==union and not a['all_beta_exclusion']
 assert sum(g['multiplicity'] for g in fourier[f'groups{mode}'])+1==mode
# Existing sealed reviews remain byte-identical.
for parent in [P.parent,P.parent/'longitudinal_extension']:
 for name,h in json.loads((parent/'MANIFEST_SHA256.json').read_text())['files'].items():assert hashlib.sha256((parent/name).read_bytes()).hexdigest()==h
out={'status':'PASS independent full physical, Fourier, spin-completion, and scalar review','independent_n24_displacement_integers':26,'independent_tiny_displacement_integers':24,'Gram_rank':23,'zero_mode_omitted':True,'Fourier_norm_factor':24,'retained_counts':[48,70],'n24_singlet_derived_not_assumed':True,'H_eigenvector_assumption':False,'remaining_closed_windows':{'48':['533/64','679/64'],'70':['539/64','339/32']},'all_earlier_seals_intact':True}
(P/'regressions.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
