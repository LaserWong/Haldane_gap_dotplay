"""Lemma LM': C_M hypothesis + exact F,G for Lemm-Mozgunov open-chain weights at n=8.
PROVED: exact rational/algebraic arithmetic (sympy).
Outputs lm_prime.json.
"""
import json, sympy as sp
from fractions import Fraction

n = 8
bn = sp.Rational(512, 35)          # 6 n^3 / ((n-1)(n-2)(n-3))
ns = 16 * sp.sqrt(2)               # n^{3/2}
an = sp.simplify(-(n-1)/ns + sp.sqrt(((n-1)/ns)**2 + 1/bn))
xn = sp.simplify(bn * an)          # = -16*sqrt(2)/5 + 32*sqrt(42)/35
cs = [sp.simplify(ns + xn * ((n-2)*j - j*j)) for j in range(n-1)]

def q(x):
    if x <= 0 or x >= len(cs):
        return sp.Integer(0)
    return sp.simplify(sum(cs[j] * cs[j + x] for j in range(len(cs) - x)))

q1 = q(1)
s21 = sp.sqrt(21)

# --- Autocorrelation q(1) >= q(2) >= ... >= q(6) (Lemma A.1 of LM; verified exactly) ---
auto = []
for x in range(1, 6):
    d = sp.simplify(q(x) - q(x + 1))
    # form a - b sqrt(21) or a + b sqrt(21); prove >= 0
    t2, t21 = sp.symbols('t2 t21')
    ex2 = sp.expand(d.subs({sp.sqrt(2): t2, sp.sqrt(21): t21, sp.sqrt(42): t2 * t21}))
    poly = sp.Poly(ex2, t2, t21)
    dd = poly.as_dict()
    assert dd.get((1, 0), 0) == 0 and dd.get((1, 1), 0) == 0
    a = sp.Rational(dd.get((0, 0), 0))
    bcoeff = sp.Rational(dd.get((0, 1), 0))
    # d = a + bcoeff * sqrt(21)
    # d = a + bcoeff * sqrt(21). Prove >= 0 over reals.
    if bcoeff >= 0 and a >= 0:
        ok = True
        witness = f"a={a}>=0, b={bcoeff}>=0"
    elif bcoeff >= 0 and a < 0:
        b = bcoeff
        aa = -a
        ok = 21 * b * b >= aa * aa
        witness = f"21b^2-a^2={21*b*b - aa*aa}"
    elif bcoeff < 0 and a >= 0:
        b = -bcoeff
        ok = a * a >= 21 * b * b
        witness = f"a^2-21b^2={a*a - 21*b*b}"
    else:
        ok = False
        witness = "both negative"
    assert ok, (x, d, witness)
    auto.append({"x": x, "ok": True, "witness": witness})

# --- C_M(e) <= q(1) for M=8..13 (finite check); M>=14 by Autocorrelation ---
CM = []
for M in range(8, 14):
    for e in range(2, M // 2 + 1):
        diff = sp.simplify(q1 - (q(e) + q(M - e)))
        t2, t21 = sp.symbols('t2 t21')
        ex2 = sp.expand(diff.subs({sp.sqrt(2): t2, sp.sqrt(21): t21, sp.sqrt(42): t2 * t21}))
        poly = sp.Poly(ex2, t2, t21)
        dd = poly.as_dict()
        assert dd.get((1, 0), 0) == 0 and dd.get((1, 1), 0) == 0
        a = sp.Rational(dd.get((0, 0), 0))
        bcoeff = sp.Rational(dd.get((0, 1), 0))
        assert bcoeff <= 0 and a >= 0
        b = -bcoeff
        ok = a * a >= 21 * b * b
        assert ok, (M, e, a, b)
        CM.append({"M": M, "e": e, "a": str(a), "b": str(b),
                   "a2_minus_21b2": str(a*a - 21*b*b), "ok": True})

# --- Exact F, G ---
c0 = cs[0]
sum_c = sum(cs)
sum_cc = sum(cs[j] * cs[j + 1] for j in range(n - 2))  # = q(1)
F = sp.simplify(c0 * sum_c / sum_cc)
G = sp.simplify((sum(c*c for c in cs) - sum_cc) / (c0 * sum_c))
# Also the paper form via diffs:
sum_diff2 = sum((cs[j] - cs[j + 1]) ** 2 for j in range(n - 2))
G_paper = sp.simplify((2 * c0 ** 2 + sum_diff2) / (2 * c0 * sum_c))
assert sp.simplify(G - G_paper) == 0
F_closed = sp.simplify(sp.Rational(49, 250) + sp.Rational(17, 125) * sp.sqrt(21))
G_closed = sp.simplify(sp.Rational(-2, 5) + sp.Rational(4, 35) * sp.sqrt(21))
assert sp.simplify(F - F_closed) == 0
assert sp.simplify(G - G_closed) == 0

# Rational bounds via sqrt(21) convergents
s_lo = Fraction(3524, 769)   # s_lo^2 < 21
s_hi = Fraction(6049, 1320)  # s_hi^2 > 21
assert s_lo * s_lo < 21 < s_hi * s_hi
F_lo = Fraction(49, 250) + Fraction(17, 125) * s_lo
G_up = Fraction(-2, 5) + Fraction(4, 35) * s_hi
mu = Fraction(6261, 50000)
assert G_up < mu
bound_lo = F_lo * (mu - G_up)
assert F_lo == Fraction(157497, 192250)
assert G_up == Fraction(1429, 11550)
assert bound_lo == Fraction(907760209, 740162500000)

out = {
    "n": 8,
    "xn": str(xn),
    "F_exact": "49/250 + 17*sqrt(21)/125",
    "G_exact": "-2/5 + 4*sqrt(21)/35",
    "F_lo": str(F_lo),
    "G_up": str(G_up),
    "mu": str(mu),
    "bound_lo": str(bound_lo),
    "bound_lo_float": float(bound_lo),
    "autocorrelation": auto,
    "CM_finite": CM,
    "CM_covers_all_M_ge": 8,
    "criterion_covers_m_ge": 8,
 "published_LM_covers_m_ge": 16,
 "LM_prime_covers_m_ge": 8,
}
json.dump(out, open("lm_prime.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ["F_lo", "G_up", "mu", "bound_lo", "bound_lo_float",
                                        "CM_covers_all_M_ge", "criterion_covers_m_ge"]}, indent=1))
print("CM cases checked:", len(CM), "all ok")
print("PROVED lm_prime.json")
