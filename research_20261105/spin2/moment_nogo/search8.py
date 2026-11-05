from feas import feasible, LAM, F
import itertools
M = 8
best = []
Js = [0.85, 0.87, 0.89]
for a in [0.0, 0.85, 0.88, 0.9]:
    for b in [0.93, 0.94, 0.95, 0.96, 0.97]:
        bigN = ([F(a).limit_denominator(1000)] if a else []) + [F(-b).limit_denominator(1000)]
        if not feasible(M, 'N', bigN): continue
        for t in Js:
            if not feasible(M, 'J', [LAM, F(t).limit_denominator(1000)]): continue
            def Z(L): return 1.00001**L + t**L + 3*((a**L if a else 0) + (-b)**L)
            pos = min(Z(L) for L in range(9, 200, 2))
            S = Z(64)/Z(32)**2
            print(a, b, t, 'minZodd(no bulk)', round(pos, 3), 'S32', round(S, 4), flush=True)
