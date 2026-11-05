# EXACT toy checks (Fraction): Thm 1 one-sided fake, Prop 2 two-sided filter certificate despite rho>=1.
from fractions import Fraction as F
def mom(sp, L): return sum(w*a**L for a, w in sp)
# ---- Thm 1 toy
J = [(F(1), 1), (F(19,20), 2), (F(-1,2), 3)]; N = [(F(3,10), 2), (F(-2,5), 1)]
M = 6; A = [(F(19,20), 2)]; t = F(99,100)
rho = sum(w*(a/1)**M for a, w in A); print('Thm1 toy rho_M^+ =', float(rho))
Jf = [(F(1), 1), (t, 1), (F(-1,2), 3)]
Z = lambda Js, L: mom(Js, L) + 3*mom(N, L); P = lambda Js, L: mom(Js, L) - mom(N, L)
up_ok = all(mom(Jf, k) <= mom(J, k) and Z(Jf, k) <= Z(J, k) and P(Jf, k) <= P(J, k) for k in range(4, M+1))
L1 = next(L for L in range(4, 10**4) if mom(A, L) <= t**L)
lo_ok = all(Z(Jf, L) >= Z(J, L) and P(Jf, L) >= P(J, L) for L in range(L1, L1+400))  # monotone tail: sum_A a^L/t^L decreasing
pos_ok = all(Z(Jf, L) > 0 and P(Jf, L) > 0 for L in range(4, 400))
S = lambda Js, n: Z(Js, 2*n)/Z(Js, n)**2
print('upper bounds k<=M preserved', up_ok, 'L1 =', L1, 'lower bounds L>=L1 preserved (checked to L1+400; tail monotone)', lo_ok, 'positivity', pos_ok)
for n in (8, 16, 32): print('  n', n, 'S true', float(S(J, n)), 'S fake', float(S(Jf, n)))
# ---- Prop 2 toy: sigma = {1} + w*{9/10}, w=2, M=6 => rho_6 = 2*(9/10)^6 >= 1
w = 2; sig = [(F(1), 1), (F(9,10), w)]; m = {k: mom(sig, k) for k in (4, 5, 6)}
print('Prop2 rho_6 =', float(w*F(9,10)**6))
filt = m[6] - F(9,5)*m[5] + F(81,100)*m[4]   # = sum lambda^4 (lambda-9/10)^2
print('filter value', filt, '= top contribution', F(1)**4*(F(1)-F(9,10))**2)
# any spectrum with these exact moments, top >= 1 (anchor) and lambda^4(lambda-0.9)^2 >= 0 termwise has top^4(top-0.9)^2 <= 1/100 => top=1,
# all other atoms in {0, 9/10}; m4 then fixes the 9/10-multiplicity: (m4-1)/(9/10)^4 =
print('forced multiplicity', (m[4]-1)/F(9,10)**4)
