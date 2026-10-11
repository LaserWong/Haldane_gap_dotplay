# Independent variable-coupling algebra (design review, pending frozen schema)

Fix the accepted source ψ and χ=T0ψ at g0=11/100, T0=200Q+11(C+C†+D). The trial columns are ψ,χ; changing g does not change either vector. For H′(g)=Q+(g/2)(C+C†+D), define a=g/22 and b=1−100g/11. Then H′(g)=aT0+bQ exactly. The Gram matrix is [[m0,m1],[m1,m2]].

Define q00=<ψ,Qψ>,q01=<ψ,Qχ>,q11=<χ,Qχ>,r00=<ψ,Q²ψ>,r01=<ψ,Q²χ>,r11=<χ,Q²χ>,s0=<ψ,Qz>,s1=<χ,Qz>, where z=T0χ. The first moment matrix is

[[a m1+b q00, a m2+b q01],
 [a m2+b q01, a m3+b q11]].

The second moment matrix is

[[a²m2+2ab q01+b²r00, a²m3+ab(q11+s0)+b²r01],
 [a²m3+ab(q11+s0)+b²r01, a²m4+2ab s1+b²r11]].

All quantities are unnormalized inner products; no independent normalization is applied to the second trial column. The pencil transformation for scaled/orthogonalized columns is a congruence applied consistently to every matrix. Generalized eigenvalues/bounds require their own exact Gram/rank/sector checks.

The old22 accumulators are stored separately by sector, so q00,q01 and r00,r01 follow by weighting their m0/m1 entries with q or q². q11,r11 similarly weight ||χq||², and include the missing q8 contributions8h²n8 and64h²n8, with h=11.

Only s0,s1 require two additional low-sector bilinears if they are not otherwise reconstructed. Compute q<ψq,zq> and q<χq,zq> at every q≤6 target. ψ has no q8 component, so s0 needs no high-sector correction. For s1 the q8 correction is

8<χ8,z8>=8(8dh²n8+h³d8+h²<χ6,γ>)
=1548800 n8+10648 d8+4 cross6,

where d=200 and cross6=242<χ6,γ> is the existing accumulator. χ has no q10 component. This correction must be included exactly once, after sector normalization. Low-sector weighted bilinears must include m-zero targets; χ or z may be nonzero there.

These formulas are an independent derivation to compare with the forthcoming24-field implementation. They are not evidence that its schema or numerical outputs already pass. Fixed-g two-dimensional trial-space pencils are not a full58D augmentation or a new endpoint/gap certificate.
