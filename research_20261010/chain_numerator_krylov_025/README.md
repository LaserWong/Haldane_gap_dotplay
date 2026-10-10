# Assess a new M8 numerator with small Krylov spaces

Updated 2026-10-10 17:59 America/New_York (EDT) / 21:59 UTC.

## Result: a verified bounded failure, not a global impossibility

At g=1/4, new exact numerator-only Rayleigh trials improve the saved two-vector M8 input, but cannot reach the necessary target for the reviewed early-window route.

| New trial space | Rayleigh improvement over saved best | Remaining δ=ρ8−2ρ4 |
|---|---:|---:|
| ψ,Hψ (dimension 2) | 0.000272000801604 | 0.0153541430553 |
| ψ,Hψ,H²ψ (dimension 3) | 0.000299768733462 | 0.0153263751234 |
| Both old directions plus Hψ,H²ψ (dimension 4) | 0.000303676444195 | 0.0153224674127 |

Displayed values are approximate; exact rational quantities are saved. Exact positive LDL pivots of H_trial−λG_trial, with λ=2ρ4+19/1250, show that every nonzero coefficient vector in each entire listed space has Rayleigh quotient above λ. Thus no different coefficient optimization within these spaces can meet the necessary δ<0.0152. The independently reviewed all-temperature early-window obstruction consequently continues to apply even with an exact M4 denominator. An additional sufficient-path scan is unnecessary because this exact necessary condition fails for the whole spaces.

This excludes only these finite trial spaces with the specified one-term Rayleigh/time-first/transported-[8,16] recipe. It does not bound the full M8 ground energy, rule out another trial direction or numerator contribution, or imply absence of a physical gap. No denominator expansion is performed.

Precision correction: the exact necessary improvement from the original saved best is 0.00042614385686183293… . A rigorous strict decimal statement is >0.000426143856861; 0.000426143856862 is an approximate rounded value. Earlier frozen prose is unchanged; all new target tests use exact λ and δ.

## Exact physical construction

The model is the periodic alternating spin-one chain, strong coupling 1 and weak coupling 1/4. M8 contains 16 physical spins with full dimension 43,046,721. The starting ψ is the previously certified rational combination of the two saved depth4 trial vectors on 43,294 configurations.

Each eight-dimer configuration is packed in 32 bits using four bits per local label. Exact physical action uses the accepted spin-one Clebsch–Gordan kernel, the complete strong energies 0,1,3 and all eight periodic weak links. GMP arbitrary-precision integers prevent overflow or truncation. The integer Hamiltonian denominator is 144.

- φ=144Hψ has 243,475 nonzero configurations.
- χ=144²H²ψ has 935,927 nonzero configurations, below the exact graph upper bound 939,326.
- A separate full action on one original saved direction supports the combined four-dimensional matrix. It has 243,438 nonzero configurations.

All images are saved explicitly. First moments of the image trial are contracted only over its own support, which is sufficient for a Rayleigh quotient. No full H³ψ output, filtered residual, isolation, or largest-seed omitted-state tail is built. Although a centered image appears as an algebraic trial direction, this is not being used as a new residual certificate.

Exact moments through order 5 provide the three-dimensional Krylov Gram and first-moment matrices. Direct metric overlaps and a separate original-direction image give the four-dimensional matrices. Exact Gram LDL orthogonalization conditions the floating coefficient proposal; the final Rayleigh quotient and target-exclusion pivots are rational. These search dimensions and configuration supports are not MPS bond dimensions.

## Budget and replay

Every numerical process uses one CPU, one BLAS thread, a 700MiB address-space ceiling during numerical work and a 600CPU-second hard limit. Initial Python cost probing was deliberately conservative. The installed-GMP C++ probe justified proceeding without installing software.

- First image plus energy contraction: 7.62CPU seconds,25MiB RSS
- Exact next-image graph: 1.29CPU seconds,54MiB RSS
- Second image plus energy contraction: 56.84CPU seconds,96MiB RSS
- Combined four-dimensional matrix evaluation: 13.16CPU seconds,321MiB RSS
- Full saved images replayed independently in Python integer arithmetic:about 25CPU seconds
- Highest contracted energy replayed by upper-triangle enumeration rather than the producer's full-column enumeration: 13.88CPU seconds

The physical kernel is reconstructed from immutable inherited sources. All three full image files pass Python-integer equality replay. Their norms and moment linkages are checked exactly; the degree 5 energy agrees with the separate triangular contraction. All reported Rayleigh values and whole-span exclusions are replayed algebraically. External independent review is separate.

## Files

- probe.json / cpp_probe.json / second_probe.json / second_support.json: pre-launch cost and support checks
- packed_input.txt / packed_old_direction.txt: exact original trial combinations and Hamiltonian kernel
- full_image.txt / second_image.txt / old_direction_image.txt: complete explicit new images
- full.json / second.json: exact contracted moments
- rayleigh.json / rayleigh_three.json / rayleigh_four.json: exact trials and whole-space target-exclusion pivots
- image_verification.json / energy_replay.json / certificate_verification.json: producer verification
- contract.cpp: portable GMP source; requires installed g++ and GMP headers/libraries
- REPRODUCE.sh: clean sibling replay; all earlier freezes remain unchanged
- FROZEN_MANIFEST.json / EXTERNAL_INPUT_SHA256.json: package and inherited input seals

No root files, previous archives or GitHub state were changed.
