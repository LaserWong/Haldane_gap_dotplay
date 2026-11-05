# T2 results — Heisenberg vs AKLT residual (Story B discriminator)

**Date:** 2026-11-05 America/Chicago  
**Verdict: NO** — naive parent-gap transfer is dead for **pure** Heisenberg.  
**Precision:** FLOAT64 (numpy/scipy dense eigvalsh at L=6; sparse Lanczos extremes at L=8). Not arb/interval certified. Heisenberg ED matches `runs/spin2/ed_small_S1.json`.

Artifacts:
- `runs/fuzzy_mps/t2_heis_vs_aklt.py`
- `runs/fuzzy_mps/T2_results.json`
- `runs/fuzzy_mps/T2_run.log`

---

## Criterion

YES iff ∃ real \(c,\alpha\) with
\[
r=\|H_{\mathrm{Heis}}-c\,H_{\mathrm{AKLT}}-\alpha I\|_{\mathrm{op}} < \gamma_{\mathrm{AKLT}}(L)
\]
with meaningful margin (we required \(r<0.5\,\gamma\) for YES).

Also report the **local bond** residual (the quantity stability/interval theorems actually use).

Definitions (spin-1, periodic):
- \(H_{\mathrm{Heis}}=\sum_i S_i\cdot S_{i+1}\)
- \(h_{\mathrm{AKLT}}=\tfrac12 S\cdot S+\tfrac16(S\cdot S)^2+\tfrac13=P_{J=2}\) (EXACT projector; FLOAT-checked)
- \(H_{\mathrm{AKLT}}=\sum_i h_{\mathrm{AKLT}}(i,i+1)\); exact GS energy 0

---

## Headline numbers (FLOAT)

| L | dim | \(\gamma_{\mathrm{AKLT}}\) | \(\gamma_{\mathrm{Heis}}\) | best \(c\) | best \(\alpha\) | residual \(r\) | \(r/\gamma_{\mathrm{AKLT}}\) | \(r/\|H_{\mathrm{Heis}}\|\) |
|---|-----|-----------------------------|----------------------------|------------|-----------------|----------------|----------------------------------|------------------------------|
| 6 | 729 | 0.347865729345 | 0.720627362624 | **2.0** | −7.879152869606 | **1.879152869606** | **5.40** | 0.218 |
| 8 | 6561 | 0.349849122179 | 0.593555254375 | **2.0** | −10.454582216654 | **2.454582216654** | **7.02** | 0.217 |

AKLT FLOAT \(E_0\sim 10^{-14}\)–\(10^{-15}\) (consistent with exact 0).  
Heisenberg \(E_0(L=6)=-8.617423181814\), \(E_0(L=8)=-11.336956077897\) (match prior ED).

**Global comparison:** \(r>\gamma_{\mathrm{AKLT}}\) at both L, by factor ~5–7. Margin \(\gamma-r\) is **negative** (−1.53 at L=6, −2.10 at L=8).  
\(r\) grows with L (extensive residual) while \(\gamma_{\mathrm{AKLT}}\) stays ~0.35 → ratio worsens with L.

---

## Bond algebra (EXACT + FLOAT)

Heisenberg bond \(=x=S\cdot S\). AKLT bond \(=\tfrac12 x+\tfrac16 x^2+\tfrac13\).

| choice of \(c\) | method | bond \(\alpha\) | \(\|x-c h-\alpha I\|_2\) | \(\|\,\cdot\,\|_F\) |
|---|---|---|---|---|
| \(c=2\) | match linear \(S\cdot S\) coeff (EXACT) | −1.5 | **0.5** | 1.5 |
| \(c=2.25\) | Frobenius / HS best on bond | −1.25 | 0.75 | 0.866 |

At \(c=2\): \(x-2h=-\tfrac13 x^2-\tfrac23\); after optimal shift, spectrum is \(\{-1/2\}\cup\{+1/2\}\) (EXACT).  
So **local deformation strength \(\delta=1/2\)**.

Compare to gaps:
- \(\delta=0.5 > \gamma_{\mathrm{AKLT}}(L=8)\approx 0.350\)
- \(\delta=0.5 >\) Affleck et al. infinite-volume lower bound \(0.1\) (same normalization)
- Triangle upper bound \(L\delta\): 3.0 (L=6), 4.0 (L=8) — consistent with measured global \(r\approx 1.88\)–\(2.45\) (cancellations help a bit, not enough)

Global optimum over \(c\) **coincides** with the linear-coeff choice \(c=2\) (Frobenius \(c=2.25\) is slightly worse globally).

---

## BB calibration (L=6, FLOAT) — near AKLT only

Bilinear-biquadratic \(H(\theta)=\sum[\cos\theta\,x+\sin\theta\,x^2]\).  
AKLT angle \(\theta_A=\arctan(1/3)\approx 0.32175\). Exact scale: \(H_{\mathrm{AKLT}}=\kappa H(\theta_A)+(L/3)I\) with \(\kappa=\sqrt{10}/6\), so \(c_\star=1/\kappa=6/\sqrt{10}\approx 1.8973666\).

| \(\theta-\theta_A\) | best \(c\) (grid) | \(r\) | \(r/\gamma_{\mathrm{AKLT}}\) |
|---|---|---|---|
| 0 (AKLT) | 1.8974 | ~1e-4 (grid); **9e-15 at exact \(c_\star\)** | ~0 |
| ±0.05 | ~1.86 / 1.93 | 0.297 | **0.854** |
| \(-\theta_A\) (Heisenberg) | 2.0 | 1.879 | **5.40** |

Calibration OK: residual vanishes on the AKLT ray. Already at \(|\Delta\theta|=0.05\), global \(r\sim 0.85\,\gamma_{\mathrm{AKLT}}\) — uncomfortable for textbook stability. Pure Heisenberg is far outside that neighborhood.

---

## Verdict

### **NO** for naive pure-Heisenberg Story B

1. Best global residual at L=8 is \(r\approx 2.45\) versus \(\gamma_{\mathrm{AKLT}}\approx 0.350\) (\(r/\gamma\approx 7\)).
2. Local bond residual after best linear match is \(\delta=1/2\gtrsim\gamma_{\mathrm{AKLT}}(L)\) and \(\gg 0.1\).
3. \(r/\|H_{\mathrm{Heis}}\|\approx 0.22=O(1)\), not a small relative deformation.

**Mechanism (one paragraph).**  
AKLT and Heisenberg differ by a finite biquadratic piece on every bond: after matching the \(S\cdot S\) coefficient (\(c=2\)), the residual bond is \(-\frac13(S\cdot S)^2+\mathrm{shift}\) with operator norm exactly \(1/2\). Finite-L ED confirms the globally optimal \((c,\alpha)\) is this same \(c=2\), with extensive residual \(r\sim O(L)\) already several times the AKLT gap at L=6 and L=8. Stability / interval theorems need a **local** perturbation ≪ parent gap; here \(\delta=1/2\) is not small compared to \(\gamma_{\mathrm{AKLT}}\). The BB scan shows the residual only collapses on the AKLT ray itself — so Story B can live in a thin neighborhood of AKLT (expensive constants, modest novelty per INTERVAL_SCOPING) but **not** at pure Heisenberg without a new mechanism (fuzzy parent of Heisenberg, non-AKLT parent, martingale with approximate MPS, etc.).

---

## What this does / does not kill

| Claim | Status after T2 |
|---|---|
| Naive transfer: \(\gamma_{\mathrm{Heis}}\ge c\gamma_{\mathrm{AKLT}}-\|H_{\mathrm{Heis}}-c H_{\mathrm{AKLT}}\|\) at pure Heis | **Killed** (right-hand side negative) |
| Interval theorem in a small BB neighborhood of AKLT | Still open / expensive; calibration consistent |
| Xiao-style fuzzy parent of Heisenberg (non-AKLT) | Untouched — different \(H_P\) |
| Story A (thermal bootstrap) | Untouched |

