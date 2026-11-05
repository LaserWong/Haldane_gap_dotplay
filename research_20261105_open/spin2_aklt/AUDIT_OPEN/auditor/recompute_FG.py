"""Independent recompute of F, G, bound_lo, C_M at n=8. No author imports."""
from fractions import Fraction
import math

# sqrt(21) convergents used by author
s_lo = Fraction(3524, 769)
s_hi = Fraction(6049, 1320)
assert s_lo*s_lo < 21 < s_hi*s_hi

# Closed forms from LM Rem 2.6 / CERT_OPEN
F_lo = Fraction(49, 250) + Fraction(17, 125) * s_lo
G_up = Fraction(-2, 5) + Fraction(4, 35) * s_hi
mu = Fraction(6261, 50000)
bound_lo = F_lo * (mu - G_up)

print("F_lo", F_lo, float(F_lo))
print("G_up", G_up, float(G_up))
print("mu", mu, float(mu))
print("mu - G_up", mu - G_up, float(mu - G_up))
print("bound_lo", bound_lo, float(bound_lo))
print("matches claimed 907760209/740162500000?", bound_lo == Fraction(907760209, 740162500000))
print("matches F_lo 157497/192250?", F_lo == Fraction(157497, 192250))
print("matches G_up 1429/11550?", G_up == Fraction(1429, 11550))

# Independent float computation of LM weights and F,G
import numpy as np
n = 8
bn = 6 * n**3 / ((n-1)*(n-2)*(n-3))
ns = n**(1.5)
an = -(n-1)/ns + math.sqrt(((n-1)/ns)**2 + 1/bn)
xn = bn * an
cs = np.array([ns + xn * ((n-2)*j - j*j) for j in range(n-1)])
print("cs", cs)
print("Ass4.1 mono to mid?", all(cs[j] >= cs[j-1] - 1e-12 for j in range(1, (n-1)//2 + 1)))
print("Ass4.1 symmetry?", np.allclose(cs, cs[::-1]))

def q(x, cs=cs):
    if x <= 0 or x >= len(cs):
        return 0.0
    return float(np.dot(cs[:len(cs)-x], cs[x:]))

qvals = [q(x) for x in range(7)]
print("q(0..6)", qvals)
print("auto monotone?", all(qvals[x] >= qvals[x+1] - 1e-9 for x in range(6)))

c0 = cs[0]
sum_c = cs.sum()
sum_c2 = np.dot(cs, cs)
q1 = q(1)
F = c0 * sum_c / q1
G = (sum_c2 - q1) / (c0 * sum_c)
# paper form
sum_diff2 = sum((cs[j]-cs[j+1])**2 for j in range(n-2))
G2 = (2*c0**2 + sum_diff2) / (2 * c0 * sum_c)
print("F float", F, "closed", 49/250 + 17*math.sqrt(21)/125)
print("G float", G, "G2", G2, "closed", -2/5 + 4*math.sqrt(21)/35)
print("G table LM rounds up to 0.1238; ours", G)

# C_M for M=8..40
fails = []
for M in range(8, 41):
    for e in range(2, M//2 + 1):
        CM = q(e) + q(M - e)
        if CM > q1 + 1e-9:
            fails.append((M, e, CM, q1))
print("C_M failures M=8..40:", len(fails), fails[:5])

# Critical case m=8..15 i.e. M=9..16
print("--- m=8..15 detail ---")
for m in range(8, 16):
    M = m + 1
    margins = []
    for e in range(2, M//2 + 1):
        CM = q(e) + q(M - e)
        margins.append((e, q1 - CM, CM/q1 if q1 else None))
    print(f"m={m} M={M} min_margin={min(x[1] for x in margins):.6e} worst_e={min(margins, key=lambda x:x[1])}")
