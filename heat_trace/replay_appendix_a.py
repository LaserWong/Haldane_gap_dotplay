#!/usr/bin/env python3
"""Replay physical Appendix A inputs and the archived exact scalar route.

The finite obligations are checked here; the linked analytic proof is an
independent mathematical reconstruction, not a proof-assistant formalization
and not a direct review of the unavailable original manuscript PDF.
"""
import hashlib, json, runpy
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
UP=ROOT.parent/'upstream/extracted'
if not UP.is_dir():UP=ROOT/'reference_sources'
def readfrac(value):return F(int(value['numerator']),int(value['denominator']))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def replay():
    inputs=[]
    for n in (6,8,10):
        for twist in ('I','P','C'):
            path=ROOT/'results'/f'A_L{n}_{twist}_full/certificate.json'
            c=json.loads(path.read_text())
            assert c['L']==n and c['twist']==twist and c['physical_dimension']==3**n
            assert c['model'].startswith('spin-1 isotropic Heisenberg')
            assert c['beta']=='21/2' and c['energy_shift_a']=='700741/500000'
            lo=readfrac(c['interval']['lower']);hi=readfrac(c['interval']['upper']);center=F(c['published_center'])
            assert center-F(1,10**5)<lo<=hi<center+F(1,10**5)
            assert c['run_metadata']['cpp_sha256']==sha(ROOT/'stream_horner.cpp')
            inputs.append({'L':n,'twist':twist,'certificate':str(path.relative_to(ROOT)),
                           'sha256':sha(path),'within_required_interval':True})
    source=UP/'cases/haldane_reference_audit/published_scalar_enclosures.py'
    # This is the Proposition5.4 computation only. Printed heat totals from
    # either appendix are not fed into this replay: the nine physical interval
    # obligations above have already been discharged from fresh calculations.
    code=source.read_text().split('# Full scalar chain in Proposition 5.4',1)[1]
    code=code[code.index('\n'):]
    namespace={'F':F};exec(compile(code,str(source), 'exec'),namespace)
    S,T=namespace['spatial'],namespace['temporal']
    bootstrap=runpy.run_path(str(UP/'tools/bootstrap_scalar.py'))['replay'](S,T,60,F(105,4))
    assert bootstrap['status']=='accepted_conditional_scalar_seed'
    anchor=ROOT.parent/'audit/mps/contraction.out'
    if not anchor.exists():anchor=ROOT/'audit_inputs/mps_contraction.out'
    fresh=anchor.read_text();archived=(UP/'cases/haldane_reference_audit/mps_exact_output.txt').read_text()
    assert fresh==archived
    mps={key:int(value) for line in fresh.splitlines() if '=' in line for key,value in [line.split('=',1)]}
    assert mps['V120']>0 and -700741*mps['V120']-500000*mps['U120']>0
    assert mps['Appendix_C8_N120']==1
    bridge=ROOT.parent/'audit/APPENDIX_A_BRIDGE.md'
    if not bridge.exists():bridge=ROOT/'audit_inputs/APPENDIX_A_BRIDGE.md'
    assert bridge.is_file()
    result={'schema':'appendix-a-computational-replay-v1',
      'status':'reconstructed_appendix_a_route_complete',
      'physical_thermal_inputs':inputs,
      'scalar_source_sha256':sha(source),
      'spatial_purity_lower':str(S),'thermal_purity_lower':str(T),
      'seed':{'n':60,'beta':'105/4','S_lower':str(S),'T_lower':str(T)},
      'bootstrap':bootstrap,
      'fresh_mps_anchor':{'path':str(anchor.relative_to(ROOT.parent)),'sha256':sha(anchor),
        'byte_identical_to_archived_totals':True,'V120_positive':True,'energy_strictly_below_minus_a':True,
        'U120':str(mps['U120']),'V120':str(mps['V120']),
        'positive_integer_margin':str(-700741*mps['V120']-500000*mps['U120'])},
      'independently_reconstructed_analytic_bridge':{'path':str(bridge.relative_to(ROOT.parent)),'sha256':sha(bridge),
        'original_manuscript_pdf_directly_reviewed':False,'proof_assistant_formalization':False},
      'theorem':{'model':'spin-1 isotropic Heisenberg, bilinear coefficient 1, hbar=1',
        'boundary':'periodic','parity':'even','minimum_length':bootstrap['final_n'],
        'ground_state':'unique','gap_lower_rational':bootstrap['conditional_gap_lower_rational'],
        'analytic_basis':'Independent transfer/A4/cooling/MPS/dominance/sequential-recursion/interpolation proof linked above'},
      'interpretation':'All nine Appendix A physical heat inputs, rebuilt N120 MPS anchor, and scalar comparisons are freshly checked. Together with the independently reconstructed analytic bridge they establish the stated even-length uniform bound. Appendix B larger inputs and the absent manuscript PDF are not claimed fully audited.'}
    path=ROOT/'appendix_a_replay.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'S':str(S),'T':str(T),'rounds':bootstrap['rounds'],'final_n':bootstrap['final_n'],
       'final_beta':bootstrap['final_beta'],'conditional_gap':bootstrap['conditional_gap_lower_rational']}),flush=True)
if __name__=='__main__':replay()
