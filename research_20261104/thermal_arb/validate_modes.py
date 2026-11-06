# Cross-validation: the same block certified in 'exact' and 'float' mode must give intersecting enclosures,
# and float-mode error bounds must dominate the exact ones (sanity of the a-priori Higham bounds).
import sys, os, json
os.environ.setdefault('OMP_NUM_THREADS', '1')
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from run import sd_cached  # noqa
from blocks import block, q_values
from cert import certify
from flint import arb
rep = []
for tw, L, sz, q in [('I', 9, 0, 2), ('P', 9, 1, 3), ('I', 10, 0, 0), ('P', 10, 0, 4)]:
    sd = sd_cached(L, tw, sz); m, ent, Hf, real = block(L, q, sd)
    e = certify(Hf, ent, L, 'exact'); f = certify(Hf, ent, L, 'float')
    xe = [arb(int(x)) * arb(2)**-e['SH'] for x in e['lt']]; xf = [arb(float.fromhex(x)) for x in f['lt']]
    inter = all(abs(a - b) <= arb(ea) + arb(eb) for a, b, ea, eb in zip(xe, xf, e['err_up'], f['err_up']))
    r = dict(block=f'{tw}_L{L}_sz{sz}_q{q}', m=m, exact_maxerr=max(e['err_up']), float_maxerr=max(f['err_up']),
             exact_eta=e['eta_up'], float_eta=f['eta_up'], exact_r=e['r_up'], float_r=f['r_up'], intersect=bool(inter))
    print(r, flush=True); rep.append(r)
json.dump(rep, open(f'{D}/validate_modes.json', 'w'), indent=1)
