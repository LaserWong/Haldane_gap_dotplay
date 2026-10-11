# Independent whole-moment derivation and review scope

This is a new review directory. Existing producer packages and prior seals are not modified. The initial authorization is a 90-process-CPU-second, CPU7, 256 MiB bounded review, with compilation capped separately at 512 MiB. The review launcher conservatively charges reservations without refund, includes compilation in the 90 seconds, uses an external process-tree CPU/RSS/wall guard, and records wait4 CPU. No complete 8×4 support sweep or cache build is authorized.

## Physical normalization

A rung uses the singlet and Cartesian triplet basis, with the explicit unnormalized columns (0,1,-1,0), (-1,0,0,1), (i,0,0,i), (0,1,1,0). The shifted rung interaction Q=(1+P12)/2 has eigenvalues 0,1,1,1. For adjacent rungs, 2(Sa1·Sb1+Sa2·Sb2)=Pa1,b1+Pa2,b2−I. Conjugating that operator by the two-rung basis, then dividing by four, gives C+C†+D with integer entries. C lowers the triplet count by two; C† raises by two; D preserves it. On two triplets, D is color permutation minus color contraction. Ed in the program is E†=[C,D], the lowering operator; E=[D,C†] raises.

For the ordinary bilayer H′=Q+(g/2)(C+C†+D), g=11/100, T=200H′=200Q+11(C+C†+D). Periodic positive-coordinate bonds are counted as a multigraph: 4×2 and 5×2 have doubled vertical bonds. The intended 8×4 geometry has 32 rungs, 32 rung edges, 64 undirected in-plane rung-neighbor edges, and physical dimension 4^32=2^64. It does not have 64 rung edges.

Let d=200, h=11, m=ψ6, χ=Tψ, z=Tχ, cm=Cm, K=[C,C†], E=[D,C†], N=[C,E], F=[E†,E], L=[[C,K],C†]. All vectors here have real coefficients. In complex notation all cross bilinears below use the relevant real part. Different triplet-number sectors are orthogonal.

## Source and low sectors

The B/L/R/M source has ψ0=c0, ψ2=BcB, ψ4=C†BcL+D C†BcR, ψ6=(C†)^2 BcM. cR and cM are distinct coefficient vectors. Pairing tensors have one, three, and fifteen channels in q=2,4,6. Giving every pair its own distinct color is a dual probe through q=6, so the coefficients are recovered exactly. Their Gram entries are 3 to the number of closed color loops.

χq=dqψq+hDψq+hC†ψ(q−2)+hCψ(q+2). Thus χ8=hC†m and no sector above eight occurs. Define x=C†cm and γ=x+Km=C C†m. Then

n8=||C†m||²=||cm||²+<m,Km>.

zq=dqχq+hDχq+hC†χ(q−2)+hCχ(q+2), q≤6. The q=6 final term is h²γ. This identifies the complete low-sector z images, including targets where m is identically zero. An M-active target filter is therefore invalid for these norms or for Kv.

The first three moments are ||ψ||², <ψ,χ>, and Σ(q≤6)||χq||²+h²n8. The cubic moment adds the low-sector diagonal and adjacent-sector bilinears plus 8dh²n8+h³d8+2h²<χ6,γ>.

## Cubic high-sector correction

Using D C†=C†D+E and C E=E C+N,

<C†m,D C†m>=2<cm,C Dm>−<cm,Dcm>+<Km,Dm>+<m,Nm> = d8.

These are terms 1–4. The first term can be evaluated as 2<x,Dm>, without changing orientation. N need not be Hermitian; N→N† is not an allowed simplification in the v cross term below.

## Complete quartic high sectors

The only sectors above six in z are eight and ten. Define

v=8dhm+hχ6+h²Dm=2dhm+2hχ6−h²C†ψ4.

Then z8=C†v+h²Em. Since C E=E C+N and E†E=EE†+F,

||z8||²=||Cv||²+<v,Kv>+2h²<v,Ecm>+2h²<v,Nm>+h⁴||E†m||²+h⁴<m,Fm>.

These are terms 5–10. They include both oriented cross terms and the signed commutator contribution.

Also z10=h²(C†)^2m. Commuting C through K and using L gives

||(C†)^2m||²=||γ||²+2<cm,C Km>−<cm,Kcm>+||Km||²+<m,Lm>.

These are terms 11–15. In particular the negative K4 term is essential, even though the total is a norm. The complete quartic moment is Σ(q≤6)||zq||² plus terms 5–10 plus h⁴ times terms 11–15. There are no omitted q8/q10 sectors, nor any q12 sector.

## Translation normalization

For any translation-invariant scalar density on q-element supports, each support contributes q incidences to the occupied-site-origin count, while each lattice site is equivalent. Therefore full support sum=(N/q) times the sum on supports containing the origin. This does not require a free translation action and remains valid for stabilized supports. At 8×4 the q4 factor is eight and the q6 factor is 16/3. Exact divisibility or rational accounting is mandatory. All ordered operator embeddings retain multiplicity; there is no additional 1/32 or stabilizer division.

This review must distinguish full small fixtures from sampled 8×4 scalar sums. A sample file marked complete refers only to its assigned sample, not to a completed physical moment.
