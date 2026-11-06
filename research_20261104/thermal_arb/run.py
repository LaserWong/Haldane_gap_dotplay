# One job = one (twist, L, Sz>=0, q) block. Resume-safe: skips if enc/<key>.json exists. Writes atomically.
# usage: python3 run.py TW L SZ Q      |  python3 run.py jobs  (prints job list, big blocks first)
import sys, os, json, time, pickle
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from blocks import *
from cert import certify
def sd_cached(L, tw, sz):
    fn = f'{D}/cache/sd_{tw}_L{L}_sz{sz}.pkl'
    if os.path.exists(fn): return pickle.load(open(fn, 'rb'))
    H = full_H(L, tw); T, s = twisted_translation(L, tw); F = flip(L)
    c, Szv = checks(L, tw, H, T, s, F); assert all(c.values()), c
    sd = sector_data(L, H, T, s, Szv, sz); sd['checks'] = c
    os.makedirs(f'{D}/cache', exist_ok=True); tmp = f'{fn}.{os.getpid()}.tmp'; pickle.dump(sd, open(tmp, 'wb')); os.replace(tmp, fn)
    return sd
if __name__ != '__main__': pass
elif sys.argv[1] == 'jobs':
    import math
    J = []
    for L in range(4, 13):
        for tw in 'IP':
            for sz in range(0, L + 1):
                for q, mu in q_values(L, tw, sz):
                    est = math.comb(2*L, L + sz)  # rough size proxy (unused for correctness)
                    J.append((est, tw, L, sz, q))
    for e, tw, L, sz, q in sorted(J, key=lambda x: -x[0]): print(tw, L, sz, q)
    sys.exit()
if __name__ == '__main__' and sys.argv[1] == 'eig':   # stage 1 for big blocks (keeps each process < ~5 min CPU)
  import numpy as np
  from cert import MEXACT
  tw, L, sz, q = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
  key = f'{tw}_L{L}_sz{sz}_q{q}'; fe = f'{D}/cache/eig_{key}.npz'
  if not os.path.exists(f'{D}/enc/{key}.json') and not os.path.exists(fe):
    m, ent, Hf, real = block(L, q, sd_cached(L, tw, sz))
    if m > MEXACT:
      t = time.time(); lam, V = np.linalg.eigh(Hf); np.savez(fe + '.tmp.npz', lam=lam, V=V); os.replace(fe + '.tmp.npz', fe)
      print('eig', key, m, '%.1fs' % (time.time() - t), flush=True)
  sys.exit()
if __name__ == '__main__':
  tw, L, sz, q = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
  key = f'{tw}_L{L}_sz{sz}_q{q}'; out = f'{D}/enc/{key}.json'
  if os.path.exists(out): sys.exit()
  t0 = time.time(); sd = sd_cached(L, tw, sz); t1 = time.time()
  mq = dict(q_values(L, tw, sz))[q]
  m, ent, Hf, real = block(L, q, sd); t2 = time.time()
  res = dict(tw=tw, L=L, sz=sz, q=q, mult=mq * (2 if sz > 0 else 1), sector_dim=sd['dim'], m=m, real=real)
  fe = f'{D}/cache/eig_{key}.npz'; eig = None
  if os.path.exists(fe):
    import numpy as np; z = np.load(fe); eig = (z['lam'], z['V'])
  if m: res.update(certify(Hf, ent, L, eig=eig))
  else: res.update(mode='empty', lt=[], err_up=[])
  t3 = time.time(); res['time_s'] = dict(sector=t1 - t0, block=t2 - t1, cert=t3 - t2)
  json.dump(res, open(out + '.tmp', 'w')); os.replace(out + '.tmp', out)
  if eig is not None: os.remove(fe)
  print(key, m, res.get('mode'), 'maxerr %.2e' % max(res['err_up'] or [0]), 'cert %.1fs' % (t3 - t2), flush=True)
