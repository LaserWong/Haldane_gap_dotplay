"""NUMERICAL. Trotter quantum transfer matrix (QTM) for periodic spin-2 chains, H = sum_j h_{j,j+1}.
Row-to-row:  T_R(eps) = Tr_a R_{aL}...R_{a1},  R = SWAP * exp(-eps h)  (so T_R = Shift*(1 - eps H) + O(eps^2)),
Z_N(L) = Tr (T_R T_R^T)^N,  eps = beta/(2N)   ->  Tr exp(-beta H_L)  as N -> inf.
Column-to-column QTM Q (dim 5^{2N}) with Z_N(L) = Tr Q^L EXACTLY for every L (checked in validate()).
Models: KHH:alpha  (h = x + alpha(2/9 x^2 + 1/63 x^3 + 10/7)),  R35 (h = P3 + 35/9 P4),  P34 (h = P3+P4)."""
import sys, json, time, numpy as np, scipy.linalg as sla, scipy.sparse.linalg as ssla
sys.path.insert(0, '..')
from ed import bond, spin_mats
d = 5
def bond_h(model):
    if model.startswith('KHH:'): return bond('KHH', float(model[4:]))
    if model == 'P34': return bond('P34', 0)
    if model == 'R35':
        Sz, Sp, Sm = spin_mats(); x = np.kron(Sz, Sz) + 0.5*(np.kron(Sp, Sm)+np.kron(Sm, Sp)); I = np.eye(25)
        xs = {J: (J*(J+1)-12)/2 for J in range(5)}
        def P(J):
            M = I.copy()
            for K in xs:
                if K != J: M = M @ (x - xs[K]*I)/(xs[J]-xs[K])
            return M
        return P(3) + 35/9*P(4)
    raise ValueError(model)
def vertices(h, eps):
    w4 = sla.expm(-eps*h).reshape(d, d, d, d)           # w4[x,y,z,t] = <x y| w |z t>
    R = np.einsum('jazt->ajzt', w4)                     # R[a', s', a, s] = <a' s'| SWAP w |a s> = w4[s',a',a,s]
    Vodd = R                                            # V[a_out, s_out, a_in, s_in]
    Veven = np.einsum('asbt->atbs', R)                  # transpose in s: from T_R^T
    return Vodd, Veven
def make_matvec(N, Vodd, Veven):
    Vs = [Vodd if k % 2 == 0 else Veven for k in range(2*N)]
    D = d**(2*N)
    def mv(v):
        X = np.zeros((d, d) + (d,)*0 + (D,), dtype=np.result_type(v, Vodd))
        X = np.einsum('ab,R->abR', np.eye(d), v).reshape(d, d, 1, D)   # (s1, scur, done, rest)
        for k in range(2*N):
            done = d**k; rest = d**(2*N-k-1)
            X = X.reshape(d, d, done, d, rest)                         # (s1, s_k, done, alpha_k, rest)
            V = Vs[k]                                                  # V[alpha'_k, s_k(out/up), alpha_k, s_{k+1}]
            Y = np.tensordot(X, V, axes=([1, 3], [1, 2]))              # (s1, done, rest, alpha'_k, s_{k+1})
            X = Y.transpose(0, 4, 1, 3, 2).reshape(d, d, done*d, rest)
        return np.einsum('aaD->D', X.reshape(d, d, D))
    return mv
def dense_Q(N, Vodd, Veven):
    mv = make_matvec(N, Vodd, Veven); D = d**(2*N)
    return np.array([mv(e) for e in np.eye(D)]).T
def validate(h, beta=1.0, Ns=(1, 2), Ls=(3, 4)):
    """Check Tr Q^L == Tr (T_R T_R^T)^N (dense, small L) and compare with exact Tr exp(-beta H_L)."""
    out = []
    for L in Ls:
        Dq = d**L
        H = np.zeros((Dq, Dq))
        for j in range(L):
            # bond (j, j+1 mod L) via permutation
            perm = list(range(L)); 
            ops = h.reshape(d, d, d, d)
            T = np.eye(Dq).reshape((d,)*L + (Dq,))
            jj = (j+1) % L
            T2 = np.tensordot(ops, T, axes=([2, 3], [j, jj]))          # (x,y, others..., Dq)
            T2 = np.moveaxis(T2, [0, 1], [j, jj]).reshape(Dq, Dq); H += T2
        Zex = np.exp(-beta*np.linalg.eigvalsh(H)).sum()
        for N in Ns:
            eps = beta/(2*N); Vo, Ve = vertices(h, eps)
            # T_R dense: <s'|T_R|s> = sum_a prod_j R[a_j, s'_j, a_{j-1}, s_j]
            R = Vo
            M = np.einsum('xpyq->xypq', R).reshape(d, d, d, d)       # M[a_out, a_in, s', s]
            # build via transfer over aux: tensor A[a0, a_cur, s'..., s...]
            A = np.einsum('ab->ab', np.eye(d)).reshape(d, d, 1, 1)
            for j in range(L):
                A = np.einsum('aeST,feps->afSpTs', A, M).reshape(d, d, A.shape[2]*d, A.shape[3]*d)
            TR = np.einsum('aaST->ST', A)
            ZN = np.trace(np.linalg.matrix_power(TR @ TR.T, N))
            Q = dense_Q(N, Vo, Ve); ZQ = np.trace(np.linalg.matrix_power(Q, L)).real
            # first-order check T_R ~ Shift (1 - eps H)
            out.append(dict(L=L, N=N, Z_exact=Zex, Z_trotter=ZN, Z_QTM=ZQ, rel_QTM_vs_trotter=abs(ZQ-ZN)/abs(ZN),
                            rel_trotter_vs_exact=abs(ZN-Zex)/Zex))
    return out
def leading(N, h, beta, k=24, tol=1e-10):
    eps = beta/(2*N); Vo, Ve = vertices(h, eps); D = d**(2*N)
    if D <= 625:
        ev = np.linalg.eigvals(dense_Q(N, Vo, Ve)); resid = 0.0
        global FULL_IM; FULL_IM = float(np.max(np.abs(ev.imag))/np.max(np.abs(ev)))
    else:
        mv = make_matvec(N, Vo, Ve)
        op = ssla.LinearOperator((D, D), matvec=mv, dtype=float)
        ev, vec = ssla.eigs(op, k=k, which='LM', tol=tol, ncv=max(2*k+1, 50), maxiter=5000)
        resid = max(np.linalg.norm(mv(vec[:, i].real) + 1j*mv(vec[:, i].imag) - ev[i]*vec[:, i]) for i in range(len(ev)))
    ev = ev[np.argsort(-np.abs(ev))][:k]
    return ev, resid
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'validate':
        for model in ['KHH:1', 'KHH:0', 'R35']:
            for r in validate(bond_h(model), beta=float(sys.argv[2]) if len(sys.argv) > 2 else 1.0):
                print(model, json.dumps(r), flush=True)
    else:   # leading model N beta k
        model, N, beta, k = sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
        t0 = time.time(); ev, res = leading(N, bond_h(model), beta, k)
        lam0 = ev[0]; rat = ev/lam0
        rec = dict(model=model, N=N, beta=beta, lam0=[lam0.real, lam0.imag], max_resid=float(res),
                   full_spectrum_max_im_over_lam0=globals().get('FULL_IM'), max_im_ratio_topk=float(np.max(np.abs(rat.imag))),
                   ratios=[[float(z.real), float(z.imag)] for z in rat], sec=time.time()-t0)
        print(json.dumps(rec), flush=True)
        with open('qtm_results.jsonl', 'a') as f: f.write(json.dumps(rec)+'\n')
