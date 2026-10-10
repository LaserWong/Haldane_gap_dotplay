#!/usr/bin/env python3
import sys; sys.dont_write_bytecode=True
from common import *
import subprocess,sys,tempfile
from datetime import datetime,timezone
assert not (HERE/'MANIFEST_SHA256.json').exists(), 'Frozen snapshot: use REPRODUCE.sh'
with tempfile.TemporaryDirectory(prefix='haldane-stage11-compare-') as temp:
    run=subprocess.run([sys.executable,str(HERE/'plot_overview.py'),'--output-dir',temp],check=True,capture_output=True,text=True)
    entries=[]
    for stem in ['certified_bounds','ordinary_interval_pieces','trial_space_counts','aklt_reference_scope','recipe_upper_caps','mps_recipe_windows','chain_window_refinement','accepted_recipe_scope','uniform_gap_frontier']:
        for ext in ['png','pdf']:
            name=stem+'.'+ext;old=sha(HERE/name);new=sha(Path(temp)/name);assert old==new,name
            entries.append({'file':name,'sha256':old,'byte_identical':True})
    report={'status':'PASS byte-identical independent re-render','checked_utc':datetime.now(timezone.utc).isoformat(),'files':entries,'replay_validation':json.loads((Path(temp)/'validation.json').read_text()),'writes':'temporary directory only for replay images; this recorder writes render_reproducibility.json before freeze'}
    (HERE/'render_reproducibility.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','identical_files':len(entries)}))
