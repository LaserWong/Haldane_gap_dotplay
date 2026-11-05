"""PROVED (exact rational algebra, sympy): projectors on bond total spin J for two spin-2 sites
as polynomials in x = S_i.S_j, using x = (J(J+1) - 12)/2 on the J-subspace (J=0..4: x=-6,-5,-3,0,4)."""
import sympy as sp, json
x = sp.symbols('x')
xs = {J: sp.Rational(J*(J+1)-12, 2) for J in range(5)}
P = {J: sp.expand(sp.prod([(x-xs[K])/(xs[J]-xs[K]) for K in xs if K != J])) for J in xs}
H = sp.expand(P[3]+P[4])
out = {f"P{J}": str(sp.Poly(P[J], x).all_coeffs()[::-1]) for J in P}
out["P3+P4 (coeffs c0..c4 of x^k)"] = str(sp.Poly(H, x).all_coeffs()[::-1])
# normalised so the linear coefficient is 1:
c1 = sp.Poly(H, x).coeff_monomial(x)
out["(P3+P4)/c1"] = str([sp.nsimplify(c/c1) for c in sp.Poly(H, x).all_coeffs()[::-1]])
out["c1"] = str(c1)
# check values
out["check"] = {J: str(H.subs(x, xs[J])) for J in xs}
print(json.dumps(out, indent=1)); json.dump(out, open('poly.json','w'), indent=1)
