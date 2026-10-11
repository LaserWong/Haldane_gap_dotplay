# Split R/M planning and bounded cached reoptimization

## Results and scope

Exact positive-LDL Gram pivots prove dimensions21 on4x4 and57 on8x4/8x8 for B,L,R,M. These are genuinely independent spans, not merely formal column counts. The existing16/43/43 basis ties the R/M coefficients. All F,S,V,W,X,Y,Z geometry comes from the sealed independent third_moment_review; no physical contraction was needed for new Gram or H matrices.

At g=.12, the exact rational upper-energy gains over freshly reoptimized16/43/43 are1.1652873e-6,2.1596434e-6,3.1024256e-6. At .11 they are6.9747390e-7,1.3197539e-6,1.9863191e-6. Full rational vectors and expectations are in reoptimization.json. Floating eigensolvers only proposed vectors; final norms and energies use exact fractions. No Ritz-optimality or residual claims are made.

The trial still has maximum q6. Its complete H image has q8, computable with the same signed commutator. For independent coefficients cR,cM, replace the scalar image formulas by

 q4: (4d cL+h cB)L +(h cL+4d cR)R +h(D4R cR+CM cM),
 q6: (h cL+6d cM)M +h(C†R cR+D6M cM),
 q8 norm: h²[||CM cM||²+<M cM,[C,C†]M cM>].

The q0/q2 images follow the cached complete B rows and their diagonal Gram; q2 includes CR cR, not CM. Existing code uses one cu in both R/M positions and must be changed consistently. Simply doubling the vector length without these changes is incorrect. Geometry support counts and R cache remain unchanged; complete single-vector runs should be comparable to prior4x4(.14s) and8x4(4.75s), but this has not been benchmarked. No new residual is authorized or launched here.

## Point source validity and trace-input diagnostic

At .11 and.12, assess_deficit.py evaluates accepted fixed-g=.105 complete coupling polynomials at the new point and checks positivity of variance, global r1-minus-Rayleigh, even r2-minus-Rayleigh and every fixed-z=.1 odd counting denominator. At .12 minimum odd r2−theta margins are.1341650596 on4x4 and.0484007142 on8x4. Thus stability/counting gates remain valid at these particular points. This is not a whole coupling interval proof.

A valid improvement to the retained odd lower energies is their maximum with the global r1 reference: after global uniqueness and the even ground, every odd eigenvalue is at least r1. This improves6/32 modes at .11 and28/32 at .12. Without it, the fixed odd Temple endpoints become unnecessarily poor; deficit_without_reference_floor.json preserves that diagnostic. All reported final deficits use this floor. Tails retain the accepted complete count and reference at the actual coupling.

Using the accepted fixed-ground polynomials and the new numerator upper, the additional numerator improvement sufficient to meet the SAME saved reference-startup ratio targets at beta9.4 is exactly rounded upward to .0014096333 at.11 and.0093999958 at.12. Under the explicitly hypothetical replacement of both ground energies by the new split Rayleigh uppers, the sufficient deficits remain .0004709766 and.005232356. These are chosen sufficient-target deficits, not necessary conditions or finite-basis impossibility theorems. Four temperatures8,9.4,11,13 were assessed; initial-cycle positivity does not establish continued bootstrap success.

The actual admissible ground interval widths (new upper minus saved-polynomial lower) are .0001107204/.0006202186 at.11 and.0010567247/.0029800973 at.12 for4x4/8x4. At .12,beta11 the hypothetical zero-ground-width diagnostic still needs about.0032985652 further numerator improvement for the same target. This is far larger than the added57D numerator gain3.1e-6. Thus adding R/M freedom solely for Rayleigh improvement is not compelling; residual-aware optimization in the current space deserves priority.

The independently accepted short bridge gives L2..7 a positive gap through.1528, so it does not block these .11/.12 tests. There is no new all-size certificate in this package.

## Resources and recovery

Rank check: .05 CPU-scale seconds,9.5MiB RSS. Cached rational reoptimization: about5.7 wall seconds, bounded CPU3/120sec/256MiB. Initial broad import exceeded256MiB address-space mapping and was replaced by AST extraction of the four needed saved scalar functions. All subsequent runs remained under the cap. Initial float diagnostic underflow was resolved by log-space sufficient-deficit evaluation; exact witnesses at beta9.4 are stored separately. Failed exploratory attempts did not alter predecessor packages.

For the more useful complete-H² matrix plan, see sibling bilayer_residual_pencil_plan. No new support contractions are present here.
