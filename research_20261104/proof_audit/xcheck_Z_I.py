# Cross-check (not a substitute): two-sided arb enclosure of Z_L(49/4), L=8,12, untwisted, from the independent
# watertight eigenvalue enclosures, vs the repo's refined thermal intervals L8_I, L12_I.
import sys, json
sys.path.insert(0,'/workspace/haldane_chat_bundle/runs/watertight')
import os; os.chdir('/workspace/haldane_chat_bundle/runs/watertight')
src=open('verify_indep.py').read().split('res = {}')[0]
exec(src)
from fractions import Fraction as Fr
d=json.load(open('/workspace/repos/Haldane_gap_dotplay/research_20261010/uniform_second_thermal_full_review/provenance_results.json'))
iv={c['case']:[Fr(x) for x in c['refined_rounded_interval']] for c in d['cases']}
for L in (8,12):
    E,tr,fr=load(L)
    up=sum((mu*(-arb(b0)*(arb(lo)+L*arb(a))).exp() for lo,hi,mu in E),arb(0)).upper()
    lo_=sum((mu*(-arb(b0)*(arb(hi)+L*arb(a))).exp() for lo,hi,mu in E),arb(0)).lower()
    rl,ru=iv[f'L{L}_I']
    inter = (lo_ <= arb(fmpq(ru.numerator,ru.denominator))) and (arb(fmpq(rl.numerator,rl.denominator)) <= up)
    print(L,'mine [',lo_.str(15),',',up.str(15),'] repo [%.15f, %.15f]'%(rl,ru),'intersect',inter)
