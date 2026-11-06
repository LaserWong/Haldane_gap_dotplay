# Assemble rigorous arb enclosures Z_L^g = sum_blocks mult * sum_i exp(-beta0 (mu_i + a L)), mu_i in [lt_i -+ err_i].
# Checks: block dims * multiplicities = 3^L and per-sector; enclosed power sums contain exact Tr H^j (digest_moments.json).
# Compares with repo refined_rounded_interval (exact rationals) and the coarse window center +- 3e-5.
import sys, os, json, glob, math, flint
from flint import arb, fmpq
flint.ctx.prec = 256
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
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
Ls = [int(x) for x in sys.argv[1:]] or range(4, 13)
for L in Ls:
    for tw in 'IP':
        key = f'L{L}_{tw}'
        need = [(sz, q) for sz in range(L + 1) for q, _ in q_values(L, tw, sz)]
        recs = []
        for sz, q in need:
            fn = f'{D}/enc/{tw}_L{L}_sz{sz}_q{q}.json'
            if not os.path.exists(fn): recs = None; break
            recs.append(json.load(open(fn)))
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
fn = f'{D}/results.json'; old = json.load(open(fn)) if os.path.exists(fn) else {}
old.update(out); json.dump(old, open(fn, 'w'), indent=1)
