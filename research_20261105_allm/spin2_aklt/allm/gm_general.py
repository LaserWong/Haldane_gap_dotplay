"""Exact-rational check of the generalized Gosset-Mozgunov bound (CERT_ALLM.md, Lemma GM').
For n-site windows with positive weights c_0..c_{n-2}, ring length m >= n:
  q(x) = sum_j c_j c_{j+x} (0 if x > n-2),  C_m(e) = q(e) + q(m-e).
Hypothesis (H_m): C_m(e) <= q(1) for all 2 <= e <= m-2.   (q(m-1)=0 automatically since m>=n.)
Conclusion: eps°_m >= F*(eps_n - G),  F = (sum c)^2/((n-1) q(1)),  G = (n-1)(sum c^2 - q(1))/(sum c)^2.
For m >= 2n-3 the hypothesis is m-independent: max_{2<=x<=n-2} q(x) <= q(1)."""
from fractions import Fraction as Fr
import json, sys
n = 8; eps = Fr(6261, 50000)
def q(c, x): return sum(c[j]*c[j+x] for j in range(len(c)-x)) if x <= len(c)-1 else Fr(0)
def check(c, m):
    q1 = q(c, 1)
    assert q(c, m-1) == 0
    viol = [e for e in range(2, m-1) if q(c, e) + q(c, m-e) > q1]
    S = sum(c); S2 = sum(x*x for x in c)
    F = S*S/((n-1)*q1); G = (n-1)*(S2-q1)/(S*S)
    return viol, F, G, F*(eps-G)
out = {}
gm = [Fr((n-1) + (n-2)*j - j*j) for j in range(n-1)]
opt = [Fr(s) for s in sys.argv[1].split(',')] if len(sys.argv) > 1 else None
for name, c in (('GM29', gm), ('opt', opt)):
    if c is None: continue
    assert all(x > 0 for x in c) and len(c) == n-1
    rows = {}
    for m in list(range(n, 2*n-3)) + [2*n-3]:   # m = 2n-3 represents all m >= 2n-3
        viol, F, G, b = check(c, m)
        rows[m if m < 2*n-3 else f'>={2*n-3}'] = dict(hyp_ok=not viol, viol=viol, F=str(F), G=str(G), bound=str(b), bound_float=float(b))
    out[name] = dict(c=[str(x) for x in c], rows=rows)
print(json.dumps(out, indent=1))
json.dump(out, open('gm_general.json', 'w'), indent=1)
