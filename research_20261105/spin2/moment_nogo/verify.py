# EXACT verification (fractions.Fraction only) of the fake spectra in fakes.json against the spin-1 certificate inputs.
import json, sys
from fractions import Fraction as F
from data import Z, P, BETA
cert = json.load(open('/workspace/haldane_chat_bundle/audit_copy/research_20261010/uniform_smaller_second_initialization/certificate_w12_Z1.json'))
ANCH = {r['anchor_length']: F(r['shifted_Rayleigh']) for r in cert['rows']}   # Z_L(beta) >= exp(-beta*R_L)
fk = json.load(open('fakes.json'))
def expup(x):  # rigorous upper bound of e^x for 0<=x<=1
    assert 0 <= x <= 1; return 1 + x + x*x
def dec(q, d=12): return f"{float(q):.{d}g}"
report = {}
for M, sp in fk.items():
    M = int(M)
    J = [(F(a), w) for a, w in sp['J']]; N = [(F(a), w) for a, w in sp['N']]
    top = max(a for a, _ in J)
    assert sum(1 for a, w in J if a == top) == 1 and dict(J)[top] == 1, 'simple top'
    others = [a for a, _ in J if a != top] + [a for a, _ in N]
    pf = all(abs(a) < top for a in others)                                    # Perron-Frobenius: strict top, simple, in J
    mult_ok = all(isinstance(w, int) and w >= 1 for _, w in J + N)
    def Jm(L): return sum(w*a**L for a, w in J)
    def Nm(L): return sum(w*a**L for a, w in N)
    def Zm(L): return Jm(L) + 3*Nm(L)
    def Pm(L): return Jm(L) - Nm(L)
    inside = {}
    for k in range(4, M+1):
        z, p = Zm(k), Pm(k)
        inside[k] = (Z[k][0] <= z <= Z[k][1], P[k][0] <= p <= P[k][1])
    data_ok = all(a and b for a, b in inside.values())
    nxt = {}
    for k in range(M+1, 13):
        z, p = Zm(k), Pm(k)
        nxt[k] = (Z[k][0] <= z <= Z[k][1], P[k][0] <= p <= P[k][1], dec(z, 6), dec((Z[k][0]+Z[k][1])/2, 6), dec(p, 6), dec((P[k][0]+P[k][1])/2, 6))
    anch = {L: Zm(L) >= expup(-BETA*R) for L, R in ANCH.items()}
    # positivity Z_L>0, P_L>0 for all L>=4: exact for 4<=L<Lstar, tail for L>=Lstar via top^L>=1 > bad(L) (bad decreasing in L)
    badZ = [(a, w) for a, w in J if a != top and a < 0] + [(a, 3*w) for a, w in N if a < 0]
    badP = [(a, w) for a, w in J if a != top and a < 0] + [(a, w) for a, w in N]
    def bad(lst, L): return sum(w*abs(a)**L for a, w in lst)
    assert top >= 1
    Ls = 4
    while bad(badZ, Ls) >= 1 or bad(badP, Ls) >= 1: Ls += 1
    pos_ok = all(Zm(L) > 0 and Pm(L) > 0 for L in range(4, Ls))
    S = {n: Zm(2*n)/Zm(n)**2 for n in (16, 32)}
    report[M] = dict(PF=pf, integer_multiplicities=mult_ok, data_k4_to_M=data_ok, anchors=anch, positivity_all_L_ge_4=pos_ok, Lstar=Ls,
                     S16=dec(S[16]), S32=dec(S[32]), K32_upper=dec(S[32]**2), top=str(top), next_data=nxt,
                     S32_below_0707=S[32]**2 < F(1,2), S16_below_0707=S[16]**2 < F(1,2))
    print(M, {k: v for k, v in report[M].items() if k != 'next_data'})
    print('   next-length data (Zin,Pin,Z',"Zmid,P,Pmid):", nxt)
json.dump({str(k): {kk: (str(vv) if not isinstance(vv, (bool, dict, int)) else vv) for kk, vv in v.items()} for k, v in report.items()}, open('verify_out.json', 'w'), indent=1, default=str)
