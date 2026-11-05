# Spin-2 port of thermal_arb/run.py. One job = (tw in Z,P; L; Sz>=0; q). Resume-safe (skips if enc/<key>.json exists).
# usage: python3 run2.py one TW L SZ Q | python3 run2.py all L [nworkers]
import sys, os, json, time, pickle
os.environ['OMP_NUM_THREADS'] = '1'; os.environ['OPENBLAS_NUM_THREADS'] = '1'
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from blocks2 import *
from cert2 import certify
def sd_cached(L, tw, sz):
    fn = f'{D}/cache/sd_{tw}_L{L}_sz{sz}.pkl'
    if os.path.exists(fn): return pickle.load(open(fn, 'rb'))
    AB = full_H(L, tw); T, s = twisted_translation(L, tw); F = flip(L)
    c, Szv = checks(L, tw, AB, T, s, F); assert all(c.values()), c
    os.makedirs(f'{D}/cache', exist_ok=True)
    out = None
    for z in range(0, 2 * L + 1):     # build all sectors at once (one H build)
        sd = sector_data(L, AB, T, s, Szv, z); sd['checks'] = c
        f2 = f'{D}/cache/sd_{tw}_L{L}_sz{z}.pkl'; tmp = f'{f2}.{os.getpid()}.tmp'
        pickle.dump(sd, open(tmp, 'wb')); os.replace(tmp, f2)
        if z == sz: out = sd
    return out
def one(tw, L, sz, q):
    key = f'{tw}_L{L}_sz{sz}_q{q}'; out = f'{D}/enc/{key}.json'
    if os.path.exists(out): return
    t0 = time.time(); sd = sd_cached(L, tw, sz); t1 = time.time()
    mq = dict(q_values(L, tw, sz))[q]
    m, ent, Hf, real = block(L, q, sd); t2 = time.time()
    res = dict(tw=tw, L=L, sz=sz, q=q, mult=mq * (2 if sz > 0 else 1), sector_dim=sd['dim'], m=m, real=real, checks=sd['checks'])
    if m: res.update(certify(Hf, ent, L))
    else: res.update(mode='empty', lt=[], err_up=[], SH=None)
    t3 = time.time(); res['time_s'] = dict(sector=t1 - t0, block=t2 - t1, cert=t3 - t2)
    os.makedirs(f'{D}/enc', exist_ok=True)
    json.dump(res, open(out + '.tmp', 'w')); os.replace(out + '.tmp', out)
    print(key, m, res.get('mode'), 'maxerr %.2e' % max(res['err_up'] or [0]), 'cert %.1fs' % (t3 - t2), flush=True)
if __name__ == '__main__':
    if sys.argv[1] == 'one': one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    elif sys.argv[1] == 'all':
        import subprocess
        from concurrent.futures import ThreadPoolExecutor
        L = int(sys.argv[2]); nw = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        for tw in 'ZP': sd_cached(L, tw, 0)
        jobs = [(tw, L, sz, q) for sz in range(0, 2 * L + 1) for tw in 'ZP' for q, _ in q_values(L, tw, sz)]
        def run(j):
            r = subprocess.run([sys.executable, __file__, 'one', *map(str, j)], capture_output=True, text=True)
            print(r.stdout.strip(), r.stderr.strip()[-500:] if r.returncode else '', flush=True)
        with ThreadPoolExecutor(nw) as ex: list(ex.map(run, jobs))
