# Spin-2 BLBQ (KHH(α)) near AKLT: no-go summary (2026-11-05, America/Chicago)
Model: h = x + α(2/9 x² + 1/63 x³ + 10/7), x = S_i·S_j, spin 2 (α=1 AKLT, α=0 Heisenberg).

1. **Heat-trace bootstrap reuse: NO.** (details DISCRIMINATOR.md)
   - The bootstrap needs eq.13 (Z_L = Tr X^L, X real self-adjoint). The sufficient construction fails ∀α∈(0,1] (PROVED, spin2_aklt/SCOPING §3).
   - iDMRG ξ (χ=64): α=0.6 17.5, 0.7 15.0, 0.8 11.8, 0.9 7.0, 0.95 4.3, 1 1.443 (NUMERICAL). So ξ≲6 only for α≳0.92 (HEURISTIC).
   - QTM top-60: real for α≤0.8; complex multiplets at α=0.9, 0.95, 1 (|r|≈0.03–0.10) (NUMERICAL).
   - The ξ≲6 window and the real-spectrum window don't overlap.
2. **Local gap (Knabe / Gosset–Mozgunov) toward α≈0.9: NO.** (details LOCAL_GAP_PLAN.md)
   - All these theorems assume frustration-free. For α<1 the bond ground space is the J=0 singlet only; no state is a singlet on two adjacent bonds ⇒ frustrated (PROVED).
   - Frustration per bond: 0.068 (α=0.95), 0.132 (α=0.9) ≈ the gap (NUMERICAL, L=8 ED).
3. **Open (not attempted):** explicit stability bounds near AKLT, probably only α≳0.99 (HEURISTIC).

Still stands: spin-1 Heisenberg bootstrap; spin-2 AKLT / VBS-parent certificates (CERT_T0 / ALLM / OPEN).
Plan: PLAN.md.
