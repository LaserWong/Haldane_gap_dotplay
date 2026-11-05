#!/usr/bin/env python3
"""Finish decisive attacks without heavy Prop4.6 n=6."""
import json, glob, os
import numpy as np
from numpy.linalg import eigh, eigvalsh
from fractions import Fraction

print("boot", flush=True)

def SS_dot(s):
    d = int(2*s+1)
    m = np.arange(s, -s-1, -1, dtype=float)
    Sp = np.zeros((d,d))
    for i, mi in enumerate(m):
        js = np.where(np.isclose(m, mi+1))[0]
        if len(js)==1:
            Sp[js[0], i] = np.sqrt(max(0.0, s*(s+1)-mi*(mi+1)))
    return (np.kron(np.diag(m),np.diag(m)) + 0.5*(np.kron(Sp,Sp.T)+np.kron(Sp.T,Sp))).real

def projector_Stot(s, forbidden_St):
    SS = SS_dot(s)
    w, V = eigh(SS)
    P = np.zeros_like(SS)
    for St in forbidden_St:
        target = 0.5*(St*(St+1) - 2*s*(s+1))
        idx = np.where(np.isclose(w, target, atol=1e-7))[0]
        assert len(idx) == int(2*St+1), (St, len(idx))
        for i in idx: P += np.outer(V[:,i], V[:,i])
    pw, pV = eigh((P+P.T)/2)
    pw = np.clip(np.round(pw), 0, 1).astype(float)
    return (pV*pw) @ pV.T

def embed_open(h, i, m, d):
    return np.kron(np.kron(np.eye(d**i), h), np.eye(d**(m-i-2)))

def open_H(h, m, d):
    return sum(embed_open(h, i, m, d) for i in range(m-1))

def gap_ker(H, tol=1e-7):
    w = np.sort(eigvalsh((H+H.T)/2))
    pos = w[w > tol]
    return (float(pos[0]) if len(pos) else 0.0), int(np.sum(w <= tol))

h1 = projector_Stot(1, [2])
g1 = {}
for m in range(2, 8):
    g, k = gap_ker(open_H(h1, m, 3))
    g1[m] = g
    print(f"spin1 m={m} gap={g:.8f} ker={k}", flush=True)

def q_of(cs, x):
    if x<=0 or x>=len(cs): return 0.0
    return sum(cs[j]*cs[j+x] for j in range(len(cs)-x))

def CM_ok(cs, M):
    q1=q_of(cs,1)
    for e in range(2, M//2+1):
        if q_of(cs,e)+q_of(cs,M-e) > q1+1e-9: return False, e
    return True, None

def FG(cs):
    c0,sc,q1=cs[0],sum(cs),q_of(cs,1)
    return c0*sc/q1, (sum(c*c for c in cs)-q1)/(c0*sc)

print("=== LM' bound spin-1 ===", flush=True)
viol=[]
for n in [4,5,6]:
    for wtag,cs in [("eq",[1.0]*(n-1)),
                    ("sym",[1.0+0.5*((n-2)/2-abs(j-(n-2)/2)) for j in range(n-1)]),
                    ("ramp",[1.0+0.3*j for j in range(n-1)]),
                    ("edgeheavy",[2.0]+[1.0]*(n-2) if n>2 else [2.0])]:
        F,G=FG(cs); mu=min(g1[k] for k in range(2,n+1))
        if mu<=G+1e-12:
            print(f"n={n} {wtag} vacuous mu={mu:.5f} G={G:.5f} F={F:.5f}", flush=True); continue
        bound=F*(mu-G)
        for m in range(n, min(2*n+2, 8)):
            okCM,ef=CM_ok(cs,m+1)
            if not okCM:
                print(f"n={n} m={m} {wtag} C_M fail e={ef}", flush=True); continue
            gm=g1[m]; ok=gm+1e-7>=bound
            print(f"n={n} m={m} {wtag}: bound={bound:.6f} gap={gm:.6f} {'OK' if ok else 'VIOL'} n>m/2={n>m/2} CMok", flush=True)
            if not ok: viol.append((n,m,wtag,bound,gm))
print("VIOLATIONS", viol, flush=True)

print("=== Knabe op ineq spin-1 ===", flush=True)
def make_B(h, m, d, l_start, cs, M):
    B = np.zeros((d**m, d**m))
    for j,c in enumerate(cs):
        bond = (l_start + j) % M
        if 1 <= bond <= m-1:
            B += c * embed_open(h, bond-1, m, d)
    return (B+B.T)/2

def check_knabe_op(h,d,m,cs):
    M=m+1
    H=open_H(h,m,d)
    Bs=[make_B(h,m,d,l,cs,M) for l in range(M)]
    S2=sum(B@B for B in Bs)
    q1=q_of(cs,1); sc2=sum(c*c for c in cs)
    alpha=1.0/q1; beta=alpha*sc2 - 1.0
    okCM,_=CM_ok(cs,M)
    Op = H@H + beta*H - alpha*S2
    Op=(Op+Op.T)/2
    wmin=float(eigvalsh(Op).min())
    return okCM, wmin, alpha, beta

for m in [4,5,6,7]:
    for wtag,cs in [("sym",[1.0,1.2,1.0]), ("eq",[1,1,1]), ("ramp",[1,1.2,1.4])]:
        if len(cs)!=3: continue
        okCM,wmin,a,b=check_knabe_op(h1,3,m,cs)
        print(f"m={m} {wtag} CMok={okCM} λmin={wmin:.4e} {'PSD' if wmin>=-1e-6 else 'NOTPSD'} α={a:.4f} β={b:.4f}", flush=True)

# Attack: does equal-weight LM' with n>m/2 give false lower bound? (already covered)
# Attack: c0 = min weight vs first weight - CERT uses min
print("=== c0 = min vs endpoint ===", flush=True)
cs_asym=[0.5,1.0,1.5,1.0,0.5]  # n=6
print("FG with c0=cs[0]", FG(cs_asym))
cs2=[1.5,1.0,0.5,1.0,1.5]
print("FG with c0=cs[0] (larger)", FG(cs2))
# Correct LM uses min
cmin=min(cs_asym)
Fcorr = cmin*sum(cs_asym)/q_of(cs_asym,1)
Gcorr = (sum(c*c for c in cs_asym)-q_of(cs_asym,1))/(cmin*sum(cs_asym))
print("FG with c0=min", Fcorr, Gcorr)

print("=== author float_ed ===", flush=True)
fed=json.load(open('/workspace/haldane_chat_bundle/runs/spin2_aklt/open/float_ed_open_3to10.json'))
print(json.dumps(fed, indent=1)[:2000], flush=True)

print("=== bound arithmetic ===", flush=True)
s_lo=Fraction(3524,769); s_hi=Fraction(6049,1320)
F_lo=Fraction(49,250)+Fraction(17,125)*s_lo
G_up=Fraction(-2,5)+Fraction(4,35)*s_hi
mu=Fraction(6261,50000)
bound=F_lo*(mu-G_up)
print("bound", bound, float(bound), "match", bound==Fraction(907760209,740162500000), flush=True)
print("F_lo", F_lo, float(F_lo))
print("G_up", G_up, float(G_up))
print("mu-G", mu-G_up, float(mu-G_up))

# C_M for author weights
print("=== author C_M for M=9..40 ===", flush=True)
# from CERT_OPEN / lm_prime.json
lp=json.load(open('/workspace/haldane_chat_bundle/runs/spin2_aklt/open/lm_prime.json'))
print("lm_prime keys", list(lp.keys()), flush=True)
print(json.dumps({k:lp[k] for k in list(lp)[:20]}, indent=1, default=str)[:2500], flush=True)

# cert spot
print("=== cert spot ===", flush=True)
arb='/workspace/haldane_chat_bundle/runs/spin2_aklt/open/arb'
print("arb listing", sorted(os.listdir(arb))[:30], flush=True)
for pat in ['cert_n7_*_t6261_50000.json','cert_n8_*_t6261_50000.json','cert_n3_*_t6261_50000.json',
            'cert_arb_n7_*_t6261_50000.json','*n7*t6261*']:
    files=sorted(glob.glob(os.path.join(arb, pat)))
    print(pat, len(files), files[:3], flush=True)

# walk for any cert json
allc=sorted(glob.glob('/workspace/haldane_chat_bundle/runs/spin2_aklt/open/**/*.json', recursive=True))
print("all open json count", len(allc), flush=True)
for p in allc[:40]:
    print(" ", p.replace('/workspace/haldane_chat_bundle/runs/spin2_aklt/open/',''), flush=True)

print("DONE", flush=True)
