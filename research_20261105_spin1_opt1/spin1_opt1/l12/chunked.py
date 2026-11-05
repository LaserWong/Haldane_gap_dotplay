# Exact (FLINT fmpz / CPython int) re-certification of the 54 L=12 thermal blocks that thermal_arb certified in
# IEEE 'float' mode.  Same theorem and same exact-mode formulas as thermal_arb/cert.py (mode 'exact'):
#   Vt = Vint/2^SV, Lt = Lint/2^SH, Hs = Hint/2^SH (integers); eta >= ||Vt^*Vt - I||_F, r >= ||Hs Vt - Vt Lt||_F
#   computed from EXACT integer sums of squares; dH = B - Hs bounded in arb from exact ball entries.
# Only difference: the m x m integer products are split across processes (600 s CPU/process box limit):
#   * Gram: column panels I<=J of V; ||G - I||_F^2 = sum_{I,J} ||(G - I)_{IJ}||_F^2 (G Hermitian: IJ and JI equal).
#     Panel products via fmpz_mat (exact).
#   * Residual: column chunks; Hs V computed EXACTLY with int64 sparse products on limbs
#     (V = sum_a 2^{20a} v_a, Hint = sum_b 2^{21b} h_b, |v_a| <= 2^20, |h_b| <= 2^21, row nnz <= 2^20 => every
#     int64 partial sum < 2^62 in absolute value, asserted), recombined in CPython ints.
# Floats (LAPACK eigh, block midpoints) only produce the trial data; rigor never depends on their accuracy.
# usage: chunked.py eig KEY | gram KEY I J | resid KEY c | finish KEY        KEY = TW_L12_szS_qQ
import sys, os, json, time
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
TA = '/workspace/haldane_chat_bundle/runs/thermal_arb'; sys.path.insert(0, TA)
D = os.path.dirname(os.path.abspath(__file__)); WK = f'{D}/work'
import numpy as np, scipy.sparse as sp, flint
from flint import arb, acb, fmpz_mat
flint.ctx.prec = 128
SV, SH = 60, 56
NP = 4          # Gram panels
NR = 4          # residual column chunks
def parse(key):
    tw, L, sz, q = key.split('_'); return tw, int(L[1:]), int(sz[2:]), int(q[1:])
def get_block(key):
    from run import sd_cached
    from blocks import block
    tw, L, sz, q = parse(key); sd = sd_cached(L, tw, sz)
    return sd, block(L, q, sd)
def panels(m, k):
    b = [round(i * m / k) for i in range(k + 1)]; return [(b[i], b[i + 1]) for i in range(k)]
def fz(A):
    A = np.ascontiguousarray(A); return fmpz_mat(A.shape[0], A.shape[1], A.ravel().tolist())
def sq(M): return sum(int(x) * int(x) for x in M.entries())
def wjson(fn, obj):
    json.dump(obj, open(fn + '.tmp', 'w')); os.replace(fn + '.tmp', fn)
cmd, key = sys.argv[1], sys.argv[2]; P = f'{WK}/{key}'; t0 = time.process_time()
if cmd == 'eig':
    if os.path.exists(f'{P}_meta.json'): sys.exit()
    sd, (m, ent, Hf, real) = get_block(key); cplx = np.iscomplexobj(Hf)
    lam, V = np.linalg.eigh(Hf)
    Lint = np.rint(lam * 2.0**SH).astype(np.int64); assert (np.diff(Lint) >= 0).all()
    assert np.abs(Hf).max() < 2**6 and np.abs(V).max() <= 1.0
    np.save(f'{P}_Lint.npy', Lint)
    np.save(f'{P}_Vr.npy', np.rint(V.real * 2.0**SV).astype(np.int64))
    if cplx: np.save(f'{P}_Vi.npy', np.rint(V.imag * 2.0**SV).astype(np.int64))
    wjson(f'{P}_meta.json', dict(m=m, cplx=bool(cplx), real=bool(real), sector_dim=int(sd['dim']), eig_cpu=time.process_time() - t0))
    print('eig', key, m, 'cplx' if cplx else 'real', '%.0fs' % (time.process_time() - t0), flush=True)
elif cmd == 'gram':
    I, J = int(sys.argv[3]), int(sys.argv[4]); out = f'{P}_gram_{I}_{J}.json'
    if os.path.exists(out): sys.exit()
    meta = json.load(open(f'{P}_meta.json')); m, cplx = meta['m'], meta['cplx']; pn = panels(m, NP)
    Vr = np.load(f'{P}_Vr.npy', mmap_mode='r'); Vi = np.load(f'{P}_Vi.npy', mmap_mode='r') if cplx else None
    (a0, a1), (b0, b1) = pn[I], pn[J]
    rI = fz(Vr[:, a0:a1]).transpose(); rJ = fz(Vr[:, b0:b1]) if I != J else None
    G = rI * (rJ if I != J else rI.transpose())
    if cplx:
        iI = fz(Vi[:, a0:a1]).transpose(); iJ = fz(Vi[:, b0:b1]) if I != J else iI.transpose()
        G = G + iI * iJ
        Gim = rI * iJ
        Gim = Gim - (iI * (rJ if I != J else rI.transpose()))
    if I == J:
        w = a1 - a0; G = G - fmpz_mat(w, w, [(1 << (2 * SV)) if i == j else 0 for i in range(w) for j in range(w)])
    g2 = sq(G) + (sq(Gim) if cplx else 0)
    wjson(out, dict(I=I, J=J, g2=str(g2), weight=1 if I == J else 2, cpu=time.process_time() - t0))
    print('gram', key, I, J, '%.0fs' % (time.process_time() - t0), flush=True)
elif cmd == 'resid':
    c = int(sys.argv[3]); out = f'{P}_resid_{c}.json'
    if os.path.exists(out): sys.exit()
    meta = json.load(open(f'{P}_meta.json')); m, cplx = meta['m'], meta['cplx']
    sd, (m2, ent, Hf, real) = get_block(key); assert m2 == m
    Hr = np.rint(Hf.real * 2.0**SH).astype(np.int64); Hi = np.rint(Hf.imag * 2.0**SH).astype(np.int64) if cplx else None
    assert np.abs(Hf).max() < 2**6
    def limbsH(A):
        S = sp.csr_matrix(A); assert int(np.diff(S.indptr).max()) < 2**20
        x = S.data.astype(np.int64); h0 = x & (2**21 - 1); h1 = (x >> 21) & (2**21 - 1); h2 = x >> 42
        assert ((h0 + (h1 << 21) + (h2 << 42)) == x).all() and np.abs(h2).max() <= 2**20
        mk = lambda d: sp.csr_matrix((d, S.indices, S.indptr), shape=S.shape)
        return [(mk(h0), 21 * 0), (mk(h1), 21), (mk(h2), 42)]
    HL = {'r': limbsH(Hr)}
    if cplx: HL['i'] = limbsH(Hi)
    del Hf
    Lint = np.load(f'{P}_Lint.npy')
    Vr = np.load(f'{P}_Vr.npy', mmap_mode='r'); Vi = np.load(f'{P}_Vi.npy', mmap_mode='r') if cplx else None
    def limbsV(X):
        X = np.ascontiguousarray(X); v0 = X & (2**20 - 1); v1 = (X >> 20) & (2**20 - 1); v2 = X >> 40
        assert ((v0 + (v1 << 20) + (v2 << 40)) == X).all() and np.abs(v2).max() <= 2**20
        return [(v0, 0), (v1, 20), (v2, 40)]
    def HV(which, X):   # exact Hint_which @ X as an object (Python int) array
        acc = None
        for h, sh in HL[which]:
            for v, sv in limbsV(X):
                Pm = h @ v; assert Pm.dtype == np.int64 and np.abs(Pm).max() < 2**62
                T = Pm.astype(object) * (1 << (sh + sv)) if sh + sv else Pm.astype(object)
                acc = T if acc is None else acc + T
        return acc
    c0, c1 = panels(m, NR)[c]; r2 = 0; SUB = 256
    for s0 in range(c0, c1, SUB):
        s1 = min(c1, s0 + SUB); lam = Lint[s0:s1].astype(object)[None, :]
        Xr = np.array(Vr[:, s0:s1]); Xi = np.array(Vi[:, s0:s1]) if cplx else None
        if cplx:
            Rre = HV('r', Xr) - HV('i', Xi) - Xr.astype(object) * lam
            Rim = HV('r', Xi) + HV('i', Xr) - Xi.astype(object) * lam
            r2 += int((Rre * Rre).sum()) + int((Rim * Rim).sum())
        else:
            R = HV('r', Xr) - Xr.astype(object) * lam; r2 += int((R * R).sum())
    wjson(out, dict(c=c, cols=[c0, c1], r2=str(r2), cpu=time.process_time() - t0))
    print('resid', key, c, '%.0fs' % (time.process_time() - t0), flush=True)
elif cmd == 'finish':
    out = f'{D}/enc/{key}.json'
    if os.path.exists(out): sys.exit()
    from cert import _dH_norm, upf
    from blocks import q_values
    meta = json.load(open(f'{P}_meta.json')); m, cplx = meta['m'], meta['cplx']
    tw, L, sz, q = parse(key)
    sd, (m2, ent, Hf, real) = get_block(key); assert m2 == m
    Hr = np.rint(Hf.real * 2.0**SH).astype(np.int64); Hi = np.rint(Hf.imag * 2.0**SH).astype(np.int64) if cplx else None
    sh = arb(2)**-SH
    nzr = set(zip(*np.nonzero(Hr))) | (set(zip(*np.nonzero(Hi))) if cplx else set())
    def Hs_of(k):
        if k == 'keys': return nzr
        i, j = k; return acb(arb(int(Hr[i, j])) * sh, arb(int(Hi[i, j])) * sh if cplx else 0)
    dHn = _dH_norm(m, ent, Hs_of)
    g2 = 0; cnt = 0
    for I in range(NP):
        for J in range(I, NP):
            g = json.load(open(f'{P}_gram_{I}_{J}.json')); assert (g['I'], g['J']) == (I, J); g2 += g['weight'] * int(g['g2']); cnt += 1
    assert cnt == NP * (NP + 1) // 2
    r2 = 0; cols = []
    for c in range(NR):
        rr = json.load(open(f'{P}_resid_{c}.json')); r2 += int(rr['r2']); cols.append(tuple(rr['cols']))
    assert cols == panels(m, NR) and cols[0][0] == 0 and cols[-1][1] == m
    Lint = np.load(f'{P}_Lint.npy'); assert len(Lint) == m and (np.diff(Lint) >= 0).all()
    c_ = arb(-L) / 2; Hn = arb(3 * L) / 2
    eta = arb(arb(g2).sqrt().upper()) * arb(2)**(-2 * SV)
    rR = arb(arb(r2).sqrt().upper()) * arb(2)**(-(SV + SH))
    assert eta < arb(1) / 2, 'eta too large'
    r = rR + dHn * (1 + eta).sqrt(); delta = Hn * eta + r * (1 + eta).sqrt()
    lt = [arb(int(x)) * sh for x in Lint]
    errs = [upf(eta * abs(x - c_) + delta) for x in lt]
    mq = dict(q_values(L, tw, sz))[q]
    res = dict(tw=tw, L=L, sz=sz, q=q, mult=mq * (2 if sz > 0 else 1), sector_dim=int(sd['dim']), m=m, real=bool(real),
               mode='exact_chunked', lt=[str(int(x)) for x in Lint], SH=SH, err_up=errs, eta_up=upf(eta), delta_up=upf(delta),
               dH_up=upf(dHn), r_up=upf(rR), gram_panels=NP, resid_chunks=NR)
    wjson(out, res)
    print('finish', key, m, 'maxerr %.2e' % max(errs), 'eta %.2e' % upf(eta), flush=True)
