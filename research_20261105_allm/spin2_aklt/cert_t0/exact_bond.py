"""PROVED-grade (exact sympy algebra over Q(sqrt6)) + INTERVAL-CERTIFIED rounding (python-flint arb).
Builds the spin-2 bond operator h = P3+P4 on C^5 (x) C^5 in the product basis |m1 m2>, m = 2,1,0,-1,-2 (index k -> m=2-k? see M below),
checks exactly: h^2 = h, h = h^T, rank 16, [h, Sz1+Sz2] = 0, SU(2) invariance ([h, S+_1+S+_2] = 0),
KHH(1) identity  x + (2/9)x^2 + (1/63)x^3 + 10/7 = 10(P3/7 + P4),
rationality of the boson-rescaled matrix  ht_pq = h_pq * w_p * w_q,  w_(m1,m2) = sqrt((2+m1)!(2-m1)!(2+m2)!(2-m2)!),
and writes: float64 h_hat (nearest-rounded) with a rigorous entrywise error bound, and the exact rational ht."""
import sympy as sp, json, math
from flint import arb, ctx
ctx.prec = 300
S = 2; M = [ -2, -1, 0, 1, 2 ]          # basis index k <-> m = M[k]  (same convention as ed.py: m = k - 2)
d = 5
Sz = sp.diag(*[sp.Integer(m) for m in M])
Sp = sp.zeros(d, d)
for k in range(d-1):
    m = M[k]; Sp[k+1, k] = sp.sqrt(S*(S+1) - m*(m+1))
Sm = Sp.T
I5 = sp.eye(d); kron = lambda A, B: sp.Matrix(sp.kronecker_product(A, B))
x = kron(Sz, Sz) + sp.Rational(1, 2)*(kron(Sp, Sm) + kron(Sm, Sp))
I25 = sp.eye(25)
xs = {J: sp.Rational(J*(J+1)-12, 2) for J in range(5)}
def proj(J):
    P = I25
    for K in xs:
        if K != J: P = P*(x - xs[K]*I25)/(xs[J]-xs[K])
    return P.applyfunc(sp.expand)
P = {J: proj(J) for J in range(5)}
h = (P[3] + P[4]).applyfunc(sp.nsimplify).applyfunc(sp.expand)
chk = {}
chk['h2_eq_h'] = (h*h - h).applyfunc(sp.expand) == sp.zeros(25, 25)
chk['symmetric'] = h == h.T
chk['rank'] = h.rank()
SzT = kron(Sz, I5) + kron(I5, Sz); SpT = kron(Sp, I5) + kron(I5, Sp)
chk['comm_Sz'] = (h*SzT - SzT*h).applyfunc(sp.expand) == sp.zeros(25, 25)
chk['comm_Splus'] = (h*SpT - SpT*h).applyfunc(sp.expand) == sp.zeros(25, 25)
chk['sum_P_eq_I'] = (sum((P[J] for J in range(5)), sp.zeros(25, 25)) - I25).applyfunc(sp.expand) == sp.zeros(25, 25)
khh1 = (x + sp.Rational(2, 9)*x*x + sp.Rational(1, 63)*x*x*x + sp.Rational(10, 7)*I25).applyfunc(sp.expand)
chk['KHH1_eq_10(P3/7+P4)'] = (khh1 - 10*(P[3]/7 + P[4])).applyfunc(sp.expand) == sp.zeros(25, 25)
# boson weights
wsite = [sp.sqrt(sp.factorial(2+m)*sp.factorial(2-m)) for m in M]
wp = [wsite[a]*wsite[b] for a in range(d) for b in range(d)]
ht = sp.zeros(25, 25); rational = True
for p in range(25):
    for q in range(25):
        v = sp.nsimplify(sp.expand(h[p, q]*wp[p]*wp[q]))
        ht[p, q] = v
        if not v.is_rational: rational = False
chk['ht_rational'] = rational
# rigorous rounding of h to float64
u = 2.0**-53
hhat = [[0.0]*25 for _ in range(25)]; maxerr = arb(0); maxrel_ok = True
six = arb(6).sqrt()
for p in range(25):
    for q in range(25):
        e = sp.expand(h[p, q]); a, b = sp.Rational(0), sp.Rational(0)
        a = e.subs(sp.sqrt(6), 0); b = sp.expand((e - a)/sp.sqrt(6))
        assert a.is_rational and b.is_rational, (p, q, e)
        val = arb(int(a.p))/arb(int(a.q)) + arb(int(b.p))/arb(int(b.q))*six
        f = float(sp.N(e, 40))
        err = abs(val - arb(f))
        if not (err.upper() <= (abs(val)*u).upper() + arb(2)**-1074): maxrel_ok = False
        hhat[p][q] = f
        maxerr = max(maxerr, err.upper(), key=lambda z: float(z.upper()) if hasattr(z,'upper') else float(z))
chk['hhat_within_u_relative'] = maxrel_ok
chk['hhat_max_abs_err_upper'] = float(arb(maxerr).upper().mid()) * (1+1e-15) + 1e-320
print(json.dumps(chk, indent=1))
assert all(v for k, v in chk.items() if isinstance(v, bool)) and chk['rank'] == 16
json.dump(dict(M=M, hhat=hhat, checks=chk,
               ht=[[str(ht[p, q]) for q in range(25)] for p in range(25)],
               h_exact=[[str(sp.expand(h[p, q])) for q in range(25)] for p in range(25)]),
          open('bond_exact.json', 'w'), indent=0)
print("wrote bond_exact.json")
