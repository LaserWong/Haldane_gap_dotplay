# Spin-2 M=8 interval-data no-go certificate

**Label: PROVED (computer-assisted, with the declared trusted base).**
Contract B-cert-M8, the bounded contract B in PLAN.md, not contract C.
The existing durable pipeline reached DONE on November 5, 2026, at 3:37 PM CST (America/Chicago). No L8 spectral certification was restarted; enc/ and cache/ were retained.

## Exact theorem

Fix beta=64 and a=4.761248=4761248/1000000 exactly. For the periodic spin-2 Heisenberg ring define

    Z_k = exp(-64 a k) Tr exp(-64 H_k^Z),
    P_k = exp(-64 a k) Tr exp(-64 H_k^P),

where H^P has the closing-bond XY coupling sign-flipped (pi seam). Let D_8 be the ten separate two-sided rational intervals in cert/enclosures.json, for Z_k,P_k at every integer k=4,...,8. They enclose the physical traces.

Class F1--F4 means exactly: compact self-adjoint transfer spectra; integer J/N multiplicities with J_L=sum_J w x^L, N_L=sum_N w x^L, Z_L=J_L+3N_L and P_L=J_L-N_L; a positive simple J Perron atom strictly dominating all other moduli; and Z_L,P_L>0 for every integer L>=4. No cross-beta, inverse-spectrum, physical-realizability or extra SU(2) restrictions are assumed.

**Theorem.** A single finite rational integer-weight member of F1--F4 has all ten moments strictly inside D_8 and simultaneously satisfies

    S(256)=Z_512/Z_256^2 < 1/sqrt(2),
    S(300)=Z_600/Z_300^2 < 1/sqrt(2).

Consequently F1--F4 plus these two-sided interval data cannot soundly force the seed S(n)>1/sqrt(2), at either n=256 or n=300. Any sound rule from only these premises must also apply to this fake, contradicting its exact verified seed inequalities.

This is an **interval-data no-go**, not a theorem for the unknown exact point-valued moments or every possible tighter enclosure. Sharing a box does not mean sharing the physical exact value. It does not assert that the physical long-chain S fails. It establishes insufficiency of this fixed length-8 box dataset in this structural information model. **It does NOT claim M_min>=26**, nor a minimum data length beyond classical exact diagonalization.

## Explicit witness and proof

The full exact witness is candidate_cert.json, section atoms. Every exported decimal is interpreted as an exact finite rational and every multiplicity string as an integer. There are eight J entries and six N entries, with potentially enormous but finite multiplicities. A diagonal operator with one J copy and three N copies per weight is finite-dimensional, hence compact and self-adjoint. Its sector traces have the required formulas.

The first J atom is t=1.00001 with weight one. The second is b=0.999 with weight one. Every other modulus is <=0.95 and strictly less than t. The verifier checks positive integer weights and strict simple Perron dominance. No real multiplicity relaxation survives export.

check_cert.py uses Python integers and Fraction for all decisions, independently of the fitter's numerical operations. It verifies strict membership in every rational Z/P box, including the very small odd-length moments; cancellation is evaluated exactly, not by floating subtraction. The displayed box positions are approximately 0.5, but these diagnostics are not proof premises.

For all-length positivity define

    B_L = sum_bulk,J w |x|^L + 3 sum_bulk,N w |x|^L.

The verifier checks Z_L,P_L>0 exactly for 4<=L<14 and establishes B_14<t^14. Since every bulk |x|<t, B_L<t^L for every L>=14. Both Z_L and P_L are bounded below by t^L+b^L-B_L>0, since the factor 3 dominates the N coefficient in either trace. Thus F4 is proved at every length, not only through the input data or seed lengths.

Finally it checks the exact inequalities 2 Z_(2n)^2 <= Z_n^4 for n=256,300. Positivity makes these equivalent to S(n)<=1/sqrt(2). An additional exact replay verifies strict `<` for both. The common decimal denominator cancels. This completes the finite-witness proof and the soundness obstruction.

## Accepted results

| n | S(n), approximate display | Threshold |
|---|---:|---:|
| 256 | 0.5082725203986761 | 1/sqrt(2)=0.7071067811865475... |
| 300 | 0.5113138102625230 | same |

check_cert_result.json has accepted=true; every Boolean check is true; F4_tail_from=14; F4_prefix_failures is empty. The displayed decimals are summaries; acceptance uses exact integer/rational inequalities.

## Trusted base and box rigor

The trusted computational base comprises cert/blocks2.py, the spin-2 Weyl+Ostrowski port cert/cert2.py, cert/run2.py, cert/assemble2.py, Python, NumPy/SciPy, python-flint/Arb/FLINT, and the specified binary64 rounding model for float-mode blocks. This is not a formal-kernel certificate.

The Hamiltonian is represented as A+sqrt(6)B with integer sparse A,B. Exact checks cover Hermiticity, twisted-translation commutation/order, Sz conservation and spin flip. Sector/block dimensions with multiplicities sum to 5^L. Bloch entries are evaluated from exact rational phases and radicals using Arb/Acb.

For spin 2 each bond has spectrum {-6,-5,-3,0,4}, including a unitarily twisted bond; therefore ||H+LI||<=5L. cert2.py uses c=-L, Hn=5L. With orthogonality defect eta and residual bound r, delta=5L eta+r sqrt(1+eta); Weyl and Ostrowski enclose each ordered eigenvalue about trial l_i with error eta |l_i+L|+delta. The stale spin-1 explanatory comment at lines 11--12 is not used; the spin-2 constants are implemented at line 52.

Modes have different certification mechanisms:
- hp: 60-digit mpmath trial eigensystem, followed by exact FLINT integer Gram/residual checks with 180-bit dyadic scales.
- exact: LAPACK trial eigensystem, followed by exact FLINT integer Gram/residual checks (SV=60, SH=56).
- float: binary64 trial eigensystem and Gram/residual computations, with explicit gamma_n rounding and underflow error bounds and Arb matrix-entry error bounds. This is certified floating computation under the stated IEEE-754/BLAS rounding model, not raw float eigenvalues.
- empty: zero-dimensional block.

Assembly sums exponentials of all eigenvalue balls outward at 256-bit precision and exports outward rational endpoints. All ten moments_contain_exact flags are true. Precisely, the code checks containment of exact Tr H and overlap with an Arb enclosure of exact Tr H^2. That consistency test alone is not spectral certification; the proof relies on the block construction, exhaustive decomposition and spectral error bounds.

A scoped additional audit, cert/audit_dH.py, reconstructs hp dyadic entry approximations and reevaluates exact block entries at 256 bits. It uses conjugate-entry intersections and the general norm bound sqrt(max row sum * max column sum), avoiding an assumption that the rounded hp matrix is Hermitian. All 184 hp blocks satisfy this bound below their stored dH_up. No L8 eigensystems were rerun and no enc/cache files were altered by this audit. Earlier, coarser same-precision audit bounds were inconclusive for ten blocks; refinement discharged those comparisons without changing their certified boxes.

Table rel_radius is the assembler's internal ball relative radius. Exported rational endpoint rounding can widen the final box (especially at L4). Only the rational endpoints define D_8.

| Trace | rel_radius | hp | exact | float | empty | moments_contain_exact |
|---|---:|---:|---:|---:|---:|---|
| Z4 | 2.021040319180e-35 | 25 | 0 | 0 | 2 | true |
| P4 | 1.949583117745e-35 | 21 | 0 | 0 | 2 | true |
| Z5 | 6.098441991288e-11 | 19 | 12 | 0 | 2 | true |
| P5 | 6.240030479631e-11 | 19 | 12 | 0 | 2 | true |
| Z6 | 1.479017170591e-10 | 17 | 32 | 0 | 3 | true |
| P6 | 1.419933339339e-10 | 15 | 28 | 0 | 3 | true |
| Z7 | 5.741664793401e-07 | 17 | 28 | 12 | 3 | true |
| P7 | 5.917681382216e-07 | 17 | 28 | 12 | 3 | true |
| Z8 | 1.149389232071e-05 | 18 | 23 | 40 | 4 | true |
| P8 | 1.137463582175e-05 | 16 | 21 | 36 | 4 | true |

## Integrity and replay

Accepted check hashes (SHA-256):

- candidate_cert.json: 886dbe6def9a20002db81644417f17b2246180995e5fffab0ffea597494db363
- cert/enclosures.json: 74d9d50f1d5996bf48e763e69ccd38e6bf28b0af9f80b185714903611d8135ce

CERT_M8_manifest.json binds the checker, certificate results, block files, core scripts, scoped audit and replay environment. candidate_cert.json records Python/NumPy/SciPy/mpmath versions. No randomness is used. NNLS/Newton are proposal mechanisms only; solver convergence is not a proof premise.

Minimal replay, without restarting certification:

```bash
cd /workspace/runs/spin2_lmin
python3 check_cert.py
python3 -c 'import check_cert as c; assert all(c.checks.values()); assert all(2*c.z(2*n)**2 < c.z(n)**4 for n in (256,300)); print("strict seed failures verified")'
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 cert/audit_dH.py
```

Optional full replay from existing enc files, not regeneration of spectral blocks:

```bash
cd /workspace/runs/spin2_lmin/cert
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 assemble2.py 4 5 6 7 8
cd ..
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 fit_cert.py
python3 check_cert.py
```

These commands rewrite derived outputs; preserve the current packet first. The exact checker replay succeeded in a fresh Python process. Reassembly of all existing L4--8 blocks and refitting were also executed successfully during document preparation and reproduced identical candidate/enclosure hashes. Pipeline output remains in finish_m8.status, finish_m8.out, cert/assemble_L8.log, fit_cert.log and check_cert.log; additional replay output is in check_cert_replay.log.

## Audit profile, limitations and blockers

Reviewed scope/quantifiers, rational data membership, integer weights, compactness, simple Perron modulus, odd-length cancellation, all-length positivity and the geometric tail, denominator cancellation and strict seed comparisons. The construction is an abstract admissible spectrum, not asserted to be a physical spin-2 Hamiltonian.

Verification basis: exact-rational witness checking plus trusted interval-certified physical traces. The entry-norm cross-check uses a separate bound but shares the block construction and Arb; there is no fully independent end-to-end Hamiltonian implementation, formal proof-assistant verification, external human review or novelty claim. PROVED here is a computer-assisted conclusion relative to the declared trusted base, not community acceptance.

No blocker remains for this fixed D_8 interval-data theorem. The stronger through-M=25 / M_min>=26 target remains BLOCKED: no through-25 certified data packet and compatible witness are supplied here. The exact-point-moment problem is also not settled by box membership.
