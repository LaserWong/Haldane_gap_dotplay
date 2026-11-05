# Assemble rigorous arb enclosures Z_L^g = sum_blocks mult * sum_i exp(-beta0 (mu_i + a L)), mu_i in [lt_i -+ err_i].
# Checks: block dims * multiplicities = 3^L and per-sector; enclosed power sums contain exact Tr H^j (digest_moments.json).
# Compares with repo refined_rounded_interval (exact rationals) and the coarse window center +- 3e-5.
import sys, os, json, glob, math, flint
from flint import arb, fmpq
flint.ctx.prec = 256
D = '/workspace/haldane_chat_bundle/runs/thermal_arb'; sys.path.insert(0, D)
E = os.path.dirname(os.path.abspath(__file__)) + '/l12/enc'   # exact_chunked overrides
OUT = os.path.dirname(os.path.abspath(__file__))
from blocks import q_values
REPO = os.environ.get('HALDANE_REPO', '/workspace/repos/Haldane_gap_dotplay')
prov = json.load(open(f'{REPO}/research_20261010/uniform_second_thermal_full_review/provenance_results.json'))
mom = json.load(open(f'{D}/digest_moments.json'))
beta = arb(fmpq(49, 4)); a = arb(fmpq(700741, 500000))
def Q(s): return fmpq(*map(int, s.split('/'))) if '/' in s else fmpq(int(s))
cases = {}
for c in (prov['cases'] if isinstance(prov, dict) and 'cases' in prov else prov):
    cases[c.get('case') or c.get('name') or f"L{c['L']}_{c['twist']}"] = c
out = {}
OVL = []
Ls = [int(x) for x in sys.argv[1:]] or range(4, 13)
for L in Ls:
    for tw in 'IP':
        key = f'L{L}_{tw}'
        need = [(sz, q) for sz in range(L + 1) for q, _ in q_values(L, tw, sz)]
        recs = []
        for sz, q in need:
            fn = f'{D}/enc/{tw}_L{L}_sz{sz}_q{q}.json'; fo = f'{E}/{tw}_L{L}_sz{sz}_q{q}.json'
            if not os.path.exists(fn): recs = None; break
            r0 = json.load(open(fn))
            if os.path.exists(fo):
                r1 = json.load(open(fo)); assert (r1['m'], r1['mult'], r1['sector_dim'], r1['sz'], r1['q']) == (r0['m'], r0['mult'], r0['sector_dim'], r0['sz'], r0['q'])
                # sanity: new exact enclosures intersect old float ones (sorted eigenvalues)
                po = sorted(zip((float.fromhex(x) if not r0['SH'] else int(x) / 2**r0['SH'] for x in r0['lt']), r0['err_up']))
                pn = [(int(x) / 2**r1['SH'], e) for x, e in zip(r1['lt'], r1['err_up'])]
                bad = sum(abs(p[0] - n[0]) > p[1] + n[1] + 1e-15 for p, n in zip(po, pn))   # float sanity only
                OVL.append((fo.split('/')[-1], max(abs(p[0] - n[0]) for p, n in zip(po, pn)), max(r0['err_up']), max(r1['err_up']), bad))
                r0 = r1
            assert r0['mode'] != 'float', ('IEEE block remains', fn)
            recs.append(r0)
        if recs is None: print(key, 'incomplete'); continue
        Z = arb(0); dim = 0; P = [arb(0)] * 5; modes = {}; maxerr = 0.0; tcert = 0.0
        secdim = {}
        for r in recs:
            mu = r['mult']; dim += mu * r['m']; secdim.setdefault(r['sz'], [r['sector_dim'], 0])
            secdim[r['sz']][1] += r['m'] * (r['mult'] // (2 if r['sz'] > 0 else 1))
            modes[r['mode']] = modes.get(r['mode'], 0) + 1; tcert += r.get('time_s', {}).get('cert', 0)
            s = 0
            for lt, e in zip(r['lt'], r['err_up']):
                x = (arb(int(lt)) * arb(2)**(-r['SH'])) if r['SH'] else arb(float.fromhex(lt))
                ball = arb(x, arb(e)); maxerr = max(maxerr, e)   # [x-e, x+e] (radius rounded outward by arb)
                Z += mu * (-(beta * (ball + a * L))).exp()
                pw = arb(1)
                for j in range(1, 5): pw = pw * ball; P[j] += mu * pw   # x*x products (x**2 on 0-straddling balls is nan)
        assert dim == 3**L and all(v[0] == v[1] for v in secdim.values()), (key, dim, secdim)
        tr = [int(x) for x in mom[key]['exact_moments_TrH_j']]
        mcheck = all(P[j + 1].contains(tr[j]) for j in range(len(tr)))
        c = cases[key] if key in cases else None
        lo, hi = Q(c['refined_rounded_interval'][0]), Q(c['refined_rounded_interval'][1])
        cc = Q(c['coarse_center']) if 'coarse_center' in c else None
        inside = bool(Z > arb(lo) and Z < arb(hi))
        rec = dict(Z_lower=Z.lower().str(25, radius=False), Z_upper=Z.upper().str(25, radius=False),
                   Z_rel_radius=float((Z.rad() / Z.mid()).upper()), repo_lo=str(lo), repo_hi=str(hi),
                   repo_rel_width=float(arb(hi - lo) / arb(hi)), inside_refined=inside,
                   moments_contain_exact=mcheck, digests_match=mom[key]['repo_digests_match'],
                   max_eig_err=maxerr, blocks_by_mode=modes, cert_seconds=tcert)
        if cc is not None:
            rec['inside_coarse_window'] = bool(Z > arb(cc - fmpq(3, 100000)) and Z < arb(cc + fmpq(3, 100000)))
        out[key] = rec
        print(key, 'Z in [%s, %s]' % (rec['Z_lower'][:22], rec['Z_upper'][:22]), 'relrad %.1e' % rec['Z_rel_radius'],
              'repo relwidth %.1e' % rec['repo_rel_width'], 'INSIDE' if inside else 'NOT INSIDE', 'mom', mcheck, modes, flush=True)
print('overrides n=%d: max |new-old| eig %.2e, old(float) maxerr %.2e, new(exact_chunked) maxerr %.2e, non-intersecting pairs %d' % (len(OVL), max(o[1] for o in OVL), max(o[2] for o in OVL), max(o[3] for o in OVL), sum(o[4] for o in OVL)) if OVL else 'no overrides')
fn = f'{OUT}/results.json'; old = json.load(open(fn)) if os.path.exists(fn) else {}
old.update(out); json.dump(old, open(fn, 'w'), indent=1)
