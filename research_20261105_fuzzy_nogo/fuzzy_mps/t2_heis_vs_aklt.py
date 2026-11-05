"""T2 discriminating test (FLOAT64, NOT rigorous):
Periodic spin-1: residual of H_Heis vs best (c, alpha) multiple of H_AKLT
vs exact finite-L AKLT gap. Decides whether naive parent-gap transfer can
work for pure Heisenberg.

Labels: FLOAT (numpy/scipy float64). Bond projector identity is EXACT algebra.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla

OUT = Path(__file__).resolve().parent
S = 1.0
D = 3  # 2S+1


def spin_mats():
    m = np.arange(D) - S
    Sz = np.diag(m.astype(float))
    Sp = np.zeros((D, D))
    for i in range(D - 1):
        Sp[i + 1, i] = np.sqrt(S * (S + 1) - m[i] * (m[i] + 1))
    return Sz, Sp, Sp.T


def bond_operators():
    Sz, Sp, Sm = spin_mats()
    x = np.kron(Sz, Sz) + 0.5 * (np.kron(Sp, Sm) + np.kron(Sm, Sp))
    x2 = x @ x
    I = np.eye(D * D)
    # EXACT: h_AKLT = (1/2)x + (1/6)x^2 + 1/3 = P_{J=2}
    h_aklt = 0.5 * x + (1.0 / 6.0) * x2 + (1.0 / 3.0) * I
    return x, x2, h_aklt, I


def verify_aklt_projector(h_aklt, x):
    ev = np.sort(np.linalg.eigvalsh(h_aklt))
    evx = np.sort(np.linalg.eigvalsh(x))
    return {
        "h_aklt_eigs_rounded": np.round(ev, 10).tolist(),
        "x_eigs_rounded": np.round(evx, 10).tolist(),
        "h_aklt_is_projector_float": bool(
            np.allclose(h_aklt @ h_aklt, h_aklt, atol=1e-12)
            and np.allclose(ev[:4], 0.0, atol=1e-12)
            and np.allclose(ev[4:], 1.0, atol=1e-12)
        ),
    }


def sparse_ham(L: int, h9: np.ndarray) -> sp.csr_matrix:
    """Periodic sum of 2-site bond ops; full Hilbert space (no Sz sector)."""
    dim = D**L
    digits = np.zeros((dim, L), dtype=np.int64)
    states = np.arange(dim, dtype=np.int64)
    tmp = states.copy()
    for s in range(L - 1, -1, -1):
        digits[:, s] = tmp % D
        tmp //= D
    pw = D ** np.arange(L - 1, -1, -1)
    nz = [
        (p, q, float(h9[p, q]))
        for p in range(D * D)
        for q in range(D * D)
        if abs(h9[p, q]) > 1e-15
    ]
    rows, cols, vals = [], [], []
    for i in range(L):
        j = (i + 1) % L
        ab = digits[:, i] * D + digits[:, j]
        for p, q, v in nz:
            ok = np.nonzero(ab == q)[0]
            if ok.size == 0:
                continue
            a2, b2 = divmod(p, D)
            a1, b1 = divmod(q, D)
            new = states[ok] + (a2 - a1) * pw[i] + (b2 - b1) * pw[j]
            rows.append(new)
            cols.append(ok)
            vals.append(np.full(ok.size, v, dtype=np.float64))
    return sp.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(dim, dim),
    )


def extremes_dense(H: np.ndarray):
    ev = np.linalg.eigvalsh(H)
    E0 = float(ev[0])
    Emax = float(ev[-1])
    tol = 1e-8
    above = ev[ev > E0 + tol]
    gap = float(above[0] - E0) if len(above) else 0.0
    E1 = float(ev[1])
    return E0, E1, Emax, gap, ev


def extremes_sparse(H: sp.csr_matrix, k_low: int = 6):
    """Lowest k and highest 1 via Lanczos; gap from lowest two distinct."""
    n = H.shape[0]
    if n <= 900:  # L<=6: 729
        return extremes_dense(H.toarray())
    # Lanczos
    k = min(k_low, n - 2)
    ev_low = np.sort(sla.eigsh(H, k=k, which="SA", tol=1e-12, maxiter=100000)[0])
    ev_hi = sla.eigsh(H, k=1, which="LA", tol=1e-12, maxiter=100000)[0]
    E0 = float(ev_low[0])
    E1 = float(ev_low[1])
    Emax = float(ev_hi[0])
    tol = 1e-7
    above = ev_low[ev_low > E0 + tol]
    gap = float(above[0] - E0) if len(above) else float("nan")
    return E0, E1, Emax, gap, ev_low


def op_norm_centered_from_extremes(lmin, lmax):
    alpha = 0.5 * (lmin + lmax)
    r = 0.5 * (lmax - lmin)
    return r, alpha


def spectral_extremes_of_combo(H_heis, H_aklt, c, dense_ok: bool):
    """λmin, λmax of H_heis - c H_aklt."""
    if dense_ok:
        A = (H_heis - c * H_aklt).toarray()
        ev = np.linalg.eigvalsh(A)
        return float(ev[0]), float(ev[-1])
    A = H_heis - c * H_aklt
    lmin = float(sla.eigsh(A, k=1, which="SA", tol=1e-12, maxiter=100000)[0][0])
    lmax = float(sla.eigsh(A, k=1, which="LA", tol=1e-12, maxiter=100000)[0][0])
    return lmin, lmax


def frobenius_bond_best_c(x, h_aklt, I):
    h = h_aklt

    def ip(A, B):
        return float(np.real(np.trace(A.conj().T @ B)))

    G = np.array([[ip(h, h), ip(h, I)], [ip(I, h), ip(I, I)]])
    rhs = np.array([ip(h, x), ip(I, x)])
    sol = np.linalg.solve(G, rhs)
    c_f, a_f = float(sol[0]), float(sol[1])
    resid = x - c_f * h - a_f * I
    return {
        "c_frobenius": c_f,
        "alpha_frobenius": a_f,
        "bond_resid_Frobenius": float(np.linalg.norm(resid, "fro")),
        "bond_resid_spectral": float(np.linalg.norm(resid, 2)),
        "bond_resid_eigs": np.linalg.eigvalsh(resid).tolist(),
        "note": "EXACT algebra for bond; FLOAT evaluation",
    }


def linear_match_bond_residual(x, h_aklt, I):
    """c=2 matches S·S linear coeff. Residual bond = x - 2 h_aklt - α I, best α."""
    c = 2.0
    R0 = x - c * h_aklt
    ev = np.linalg.eigvalsh(R0)
    alpha = 0.5 * (ev[0] + ev[-1])
    resid = R0 - alpha * I
    return {
        "c": c,
        "alpha": float(alpha),
        "bond_resid_spectral": float(np.linalg.norm(resid, 2)),
        "bond_resid_Frobenius": float(np.linalg.norm(resid, "fro")),
        "bond_resid_eigs": np.linalg.eigvalsh(resid).tolist(),
        "note": "EXACT c=2 from matching coeff of S·S; FLOAT residual",
    }


def optimize_c(H_heis, H_aklt, dense_ok: bool):
    c_grid = np.linspace(-1.0, 5.0, 61)
    best = None
    rows = []
    for c in c_grid:
        lmin, lmax = spectral_extremes_of_combo(H_heis, H_aklt, float(c), dense_ok)
        r, alpha = op_norm_centered_from_extremes(lmin, lmax)
        rec = {"c": float(c), "r": r, "alpha": alpha, "lmin": lmin, "lmax": lmax}
        rows.append(rec)
        if best is None or r < best["r"]:
            best = rec
    c0 = best["c"]
    for scale in (0.2, 0.05, 0.01, 0.002):
        for c in np.linspace(c0 - scale, c0 + scale, 41):
            lmin, lmax = spectral_extremes_of_combo(H_heis, H_aklt, float(c), dense_ok)
            r, alpha = op_norm_centered_from_extremes(lmin, lmax)
            rec = {"c": float(c), "r": r, "alpha": alpha, "lmin": lmin, "lmax": lmax}
            rows.append(rec)
            if r < best["r"]:
                best = rec
                c0 = float(c)
    return best, rows


def run_L(L: int):
    print(f"=== L={L} dim={D**L} ===", flush=True)
    x, x2, h_aklt, I = bond_operators()
    sanity = verify_aklt_projector(h_aklt, x)
    print("bond sanity:", sanity, flush=True)
    bond_frob = frobenius_bond_best_c(x, h_aklt, I)
    bond_lin = linear_match_bond_residual(x, h_aklt, I)
    print("bond frobenius:", bond_frob, flush=True)
    print("bond linear c=2:", bond_lin, flush=True)

    t0 = time.time()
    H_heis = sparse_ham(L, x)
    t1 = time.time()
    H_aklt = sparse_ham(L, h_aklt)
    t2 = time.time()
    print(f"built sparse H in {t1-t0:.2f}s / {t2-t1:.2f}s; nnz={H_heis.nnz}", flush=True)

    dense_ok = H_heis.shape[0] <= 900  # L=6
    E0h, E1h, Emaxh, gap_h, _ = extremes_sparse(H_heis)
    E0a, E1a, Emaxa, gap_a, _ = extremes_sparse(H_aklt)
    print(f"Heis: E0={E0h:.12f} E1={E1h:.12f} gap={gap_h:.12f} Emax={Emaxh:.12f}", flush=True)
    print(f"AKLT: E0={E0a:.12e} E1={E1a:.12f} gap={gap_a:.12f} Emax={Emaxa:.12f}", flush=True)

    heis_op = float(max(abs(E0h), abs(Emaxh)))
    aklt_op = float(max(abs(E0a), abs(Emaxa)))

    t3 = time.time()
    best, grid_rows = optimize_c(H_heis, H_aklt, dense_ok)
    t4 = time.time()
    print(f"best (c,α,r)={best}  optimize_sec={t4-t3:.1f}", flush=True)

    extras = {}
    for name, c in [("linear_coeff_c2", 2.0), ("frobenius_bond_c", bond_frob["c_frobenius"])]:
        lmin, lmax = spectral_extremes_of_combo(H_heis, H_aklt, c, dense_ok)
        r, alpha = op_norm_centered_from_extremes(lmin, lmax)
        extras[name] = {
            "c": c,
            "alpha": alpha,
            "r": r,
            "lmin": lmin,
            "lmax": lmax,
            "r_over_gamma_AKLT": (r / gap_a) if gap_a > 0 else None,
        }
        print(name, extras[name], flush=True)

    # Bond-wise residual amplified: L * ‖residual_bond‖_op as crude upper on ‖∑ resid‖
    # (triangle inequality; not tight). Also compute exact ‖∑(x - c*h - α/L I)‖ via best.
    r = best["r"]
    verdict_numbers = {
        "residual_r": r,
        "gamma_AKLT": gap_a,
        "gamma_Heis": gap_h,
        "opnorm_Heis": heis_op,
        "residual_lt_gamma_AKLT": bool(r < gap_a),
        "r_over_gamma_AKLT": r / gap_a if gap_a > 0 else None,
        "r_over_opnorm_Heis": r / heis_op if heis_op > 0 else None,
        "r_over_gamma_Heis": r / gap_h if gap_h > 0 else None,
        "margin_gamma_minus_r": gap_a - r,
        "triangle_upper_L_times_bond_resid_spectral_c2": L * bond_lin["bond_resid_spectral"],
    }

    return {
        "L": L,
        "dim": int(D**L),
        "label": "FLOAT64_sparse_Lanczos" if not dense_ok else "FLOAT64_dense_eigvalsh",
        "bond_sanity": sanity,
        "bond_frobenius_match": bond_frob,
        "bond_linear_c2": bond_lin,
        "Heisenberg": {
            "E0": E0h,
            "E1": E1h,
            "Emax": Emaxh,
            "gap": gap_h,
            "op_norm": heis_op,
        },
        "AKLT": {
            "E0": E0a,
            "E1": E1a,
            "Emax": Emaxa,
            "gap_gamma_AKLT": gap_a,
            "op_norm": aklt_op,
            "note": "H_AKLT=sum P_J=2; exact GS energy 0; FLOAT E0 ~ machine eps * scale",
        },
        "best_global": best,
        "fixed_c_evals": extras,
        "verdict_numbers": verdict_numbers,
        "timing_sec": {"build_heis": t1 - t0, "build_aklt": t2 - t1, "optimize": t4 - t3},
        "n_grid_evals": len(grid_rows),
    }


def bb_calibration_L6():
    """H(θ)=∑[cosθ x + sinθ x^2] near AKLT angle θ_A=arctan(1/3). FLOAT L=6."""
    x, x2, h_aklt, I = bond_operators()
    theta_A = float(np.arctan(1.0 / 3.0))
    H_ak = sparse_ham(6, h_aklt)
    E0a, _, _, gap_a, _ = extremes_sparse(H_ak)
    points = []
    for th in [theta_A, theta_A + 0.05, theta_A - 0.05, 0.0]:
        h_th = np.cos(th) * x + np.sin(th) * x2
        H_th = sparse_ham(6, h_th)
        best, _ = optimize_c(H_th, H_ak, dense_ok=True)
        E0t, _, _, gap_t, _ = extremes_sparse(H_th)
        points.append(
            {
                "theta": float(th),
                "theta_minus_aklt": float(th - theta_A),
                "is_aklt_angle": bool(abs(th - theta_A) < 1e-14),
                "is_heisenberg_angle_cos1": bool(abs(th) < 1e-14),
                "best_c": best["c"],
                "best_alpha": best["alpha"],
                "residual_r": best["r"],
                "gamma_AKLT": gap_a,
                "gamma_Htheta": gap_t,
                "E0_Htheta": E0t,
                "r_over_gamma_AKLT": best["r"] / gap_a if gap_a > 0 else None,
            }
        )
        print("BB", points[-1], flush=True)
    return {"theta_AKLT_arctan_1_3": theta_A, "points": points, "label": "FLOAT64"}


def main():
    t_all = time.time()
    out = {
        "test": "T2",
        "date_local": "2026-11-05 America/Chicago",
        "model": "periodic spin-1",
        "H_Heis": "sum_i S_i·S_{i+1}",
        "H_AKLT": "sum_i [(1/2)S·S+(1/6)(S·S)^2+(1/3)] = sum_i P_{J=2}",
        "criterion": (
            "YES if exists real c,α with operator-norm residual "
            "‖H_Heis-c H_AKLT-α I‖ < γ_AKLT(L) with meaningful margin "
            "(we require r < 0.5 γ for YES); else NO"
        ),
        "precision": "FLOAT64 (numpy/scipy); not arb/interval certified",
        "results_by_L": {},
    }
    for L in (6, 8):
        out["results_by_L"][str(L)] = run_L(L)

    print("=== BB calibration L=6 ===", flush=True)
    out["BB_calibration_L6"] = bb_calibration_L6()

    r8 = out["results_by_L"]["8"]["best_global"]["r"]
    g8 = out["results_by_L"]["8"]["AKLT"]["gap_gamma_AKLT"]
    r6 = out["results_by_L"]["6"]["best_global"]["r"]
    g6 = out["results_by_L"]["6"]["AKLT"]["gap_gamma_AKLT"]
    yes8 = r8 < 0.5 * g8
    yes6 = r6 < 0.5 * g6
    if r8 < g8 and yes8:
        verdict, reason = "YES", "r < 0.5 γ_AKLT at L=8; naive stability possibly viable"
    elif r8 < g8:
        verdict, reason = (
            "MARGINAL",
            "r < γ_AKLT but margin < 50%; textbook transfer uncomfortable",
        )
    else:
        verdict, reason = (
            "NO",
            "r ≥ γ_AKLT at pure Heisenberg (L=8); naive parent-gap transfer dead",
        )

    out["verdict"] = verdict
    out["verdict_reason"] = reason
    out["summary"] = {
        "L6": {
            "r": r6,
            "gamma_AKLT": g6,
            "r_over_gamma": r6 / g6,
            "strict_lt": bool(r6 < g6),
            "half_margin": yes6,
        },
        "L8": {
            "r": r8,
            "gamma_AKLT": g8,
            "r_over_gamma": r8 / g8,
            "strict_lt": bool(r8 < g8),
            "half_margin": yes8,
        },
    }
    out["total_sec"] = time.time() - t_all
    path = OUT / "T2_results.json"
    path.write_text(json.dumps(out, indent=2))
    print("Wrote", path, flush=True)
    print("VERDICT:", verdict, "|", reason, flush=True)
    return out


if __name__ == "__main__":
    main()
