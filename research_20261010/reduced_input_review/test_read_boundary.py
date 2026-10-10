"""Run frozen producer against isolated allowed inputs; trap forbidden reads.
The producer is deliberately NOT used for independent mathematical acceptance.
"""
from audit_helpers import *
import importlib.util, shutil, io, tempfile
SRC=HERE/'snapshot/research_20261010';PROD=RESEARCH/'low_band/reduced_input'
# Imports use existing arithmetic code, but numerical inputs are isolated below.
for p in [RESEARCH/'low_band/translation_band',RESEARCH/'low_band/frontier_g006',RESEARCH/'root_review']:
    sys.path.insert(0,str(p))
spec=importlib.util.spec_from_file_location('frozen_reduced_consumer',SRC/'low_band/reduced_input/replay_minimal.py')
consumer=importlib.util.module_from_spec(spec);spec.loader.exec_module(consumer)
temporary=tempfile.TemporaryDirectory(prefix='reduced_input_boundary_')
root=Path(temporary.name)/'research_20261010';root.mkdir(parents=True,exist_ok=True)
# All byte materialization happens before the read-denial hook is active.
records=[]
for g in ['3/100','1/25','1/20','3/50']:
    tag=f'g{g}'.replace('/','d')
    for mode in ['ground_only','trial193']:
        expected=load(SRC/f'low_band/reduced_input/{mode}_{tag}.json')
        dest=root/mode;dest.mkdir(parents=True,exist_ok=True)
        for name in expected['numeric_files_read_sha256']:
            target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SRC/name,target)
        historical=[load(SRC/f'low_band/reduced_input/largest_ground_{tag}.json')['historical_source'],
                    load(SRC/f'low_band/reduced_input/largest_triplet_GA_{tag}.json')['historical_source']]
        historical += [f'low_band/frontier_g006/{prefix}_8x8_{tag}.json' for prefix in ['temple','number_bins']]
        for name in historical:
            poison=dest/name;poison.parent.mkdir(parents=True,exist_ok=True);poison.write_text('INVALID JSON: FORBIDDEN LARGEST HIGHER-MOMENT INPUT\n')
        if mode=='ground_only':assert not (dest/f'low_band/reduced_input/largest_triplet_GA_{tag}.json').exists()
        records.append((g,mode,expected,dest))
active=False;allowed=set();seen=set();denied=[]
def hook(event,args):
    if not active or event!='open':return
    path,mode,flags=args
    if not isinstance(path,(str,bytes,os.PathLike)):return
    p=Path(os.fsdecode(path)).resolve()
    if p.suffix!='.json':return
    if p not in allowed:
        denied.append(str(p));raise PermissionError('Numerical read outside minimal declared inputs: '+str(p))
    seen.add(p)
sys.addaudithook(hook)
reports=[]
for g,mode,expected,dest in records:
    allowed={(dest/name).resolve() for name in expected['numeric_files_read_sha256']};seen=set();denied=[]
    consumer.RESEARCH=dest;consumer.BAND=dest/'low_band';consumer.HERE=consumer.BAND/'reduced_input'
    active=True
    try: actual=consumer.run(g,expected['beta_initial'],mode)
    finally:active=False
    assert actual==expected and seen==allowed and not denied
    assert not any('8x8' in str(p) for p in seen)
    reports.append(dict(g=g,mode=mode,exact_frozen_output_equal=True,all_numerical_reads_match_declared_set=True,read_count=len(seen),legacy_higher_moment_files_poisoned=True,undeclared_json_reads_denied=True,optional_triplet_file_absent=mode=='ground_only',opened_paths=sorted(str(p.relative_to(dest)) for p in seen)))
    print('READ BOUNDARY PASS',g,mode,len(seen),flush=True)
save('read_boundary.json',reports)

temporary.cleanup()
