# Exact fourth-moment sparse physical fixture

Frozen 2026-10-11 00:23 UTC (2026-10-10 20:23 EDT). This package preserves the completed producer run; recovery did not rerun or change fixture.cpp, its executable, or its numerical output. Independent review is pending at this seal.

## Scope and normalization

Ordinary spin-half periodic square bilayer, N=8 and N=10 rungs on 4×2 and 5×2 tori. The graph is x-major i=2x+y. Each positive-direction periodic bond is included; the width-two vertical bonds have multiplicity two, and every rung has weighted degree four. There are 2N weighted rung edges and 4N physical intralayer spin-half bonds. H′=Q+(g/2)A, A=C+C†+D, g=11/100. The exact integer operator is T=200H′=200Q+11A. Full Hilbert dimensions are 4^8=65536 and 4^10=1048576. No diagonalization is used. This is a localized one-vector fixture, not the accepted 57-dimensional seed space or an MPS calculation.

Each rung uses orthonormal labels 0=s, 1=t+, 2=t0, 3=t−. On a rung edge C annihilates (t0,t0) with coefficient +1 and (t+,t−),(t−,t+) with coefficient −1; C† is its adjoint. D swaps a singlet with a triplet and acts as spin-one exchange on two triplets. Thus A is twice the physical sum of the two intralayer spin-half exchanges. The independent reviewer uses a Cartesian-triplet convention and checks this identity against the physical four-spin operator.

Write P_ab for the unnormalized singlet pair t0_a t0_b−t+_a t−_b−t−_a t+_b on otherwise empty rungs. The exact trial is

ψ=3|0>−2P_01|0>+P_01P_23|0>−P_01P_23P_45|0>+2P_02P_13P_46|0>.

Its norm squared is 165 on both graphs, with occupation q≤6. Put m=ψ6, χ=Tψ, z=Tχ. The outputs store unnormalized integer moments <χ,z> and ||z||². Physical normalized moments are m_k=<ψ,T^kψ>/(165·200^k). All signs and orientations are retained.

## Normal-order identities exercised

Set K=[C,C†], E=[D,C†], E†=[C,D], Nop=[C,E], L=[[C,K],C†], γ=C†Cm+Km. The exact m3 high-sector identity is

<C†m,D C†m>=2<Cm,C Dm>−<Cm,D Cm>+<Km,Dm>+<m,Nop m>.

All coefficients here are real. This must not be symmetrized by changing an individual non-Hermitian operator orientation. The lower occupation sectors and q6↔q8 term are added exactly to obtain <χ,Tχ>.

For d=200,h=11 define v=8dh m+hχ6+h²Dm. Then

z8=C†v+h²Em,
||z8||²=||Cv||²+<v,Kv>+2h²<v,E Cm>+2h²<v,Nop m>+h⁴(||E†m||²+<m,[E†,E]m>).

The q10 component is z10=h²(C†)²m, with

||z10||²/h⁴=||γ||²+2<Cm,C Km>−<Cm,K Cm>+||Km||²+<m,Lm>.

For each q≤6, the program reconstructs zq from χq, adjacent lower sectors and γ, compares the entire sparse vector with direct T²ψ, and adds its exact norm. All displayed terms are saved individually in terms_4x2.json and terms_5x2.json. This includes both oriented q8 interference pieces, the negative q10 K term, the [E†,E] expectation and L.

## Exact results

4×2: direct and normal m3 numerator 194614254120; direct and normal m4 numerator 219823916814456. Sector q8 contributes 462298904100 and q10 contributes zero. The q10 identity cancels nonzero terms exactly to zero.

5×2: direct and normal m3 numerator 195536812812; direct and normal m4 numerator 222050079503448. Sector q8 contributes 2178426373992; q10 contributes 452758284, with unscaled double-creation norm 30924. Thus the q10 test is nonvacuous.

The q8 interference totals are −8988722160 and −61300919328. The unscaled [E†,E] expectations are −61656 and −5688; L expectations are 41568 and −33612; negative q10 K contributions are −7896 and −44652. Assertions detect dropping the interference or L terms.

## Exact arithmetic and resources

Sparse amplitudes are int64 with checked int128 additions; inner products are int128. For these fixtures the trial coefficient l1 norm is at most 99. Each C,C†,D has absolute column sum at most 60; T at most 2660. Every amplitude involved in at most four basic operator factors, including expanded commutators, is bounded conservatively below 2^40. With at most 4^10 states, every inner product is below 2^100, inside signed int128. This argument is specific to these fixtures, not a bound for large optimized coefficients.

Saved cumulative wall time is .299015 seconds and peak RSS 5784 KiB; log reports 3810/17650 maximum intermediate sparse states for the two sizes. The provided reproduction wrapper pins CPU3, limits the physical executable to 5 CPU seconds and 100 MiB address space, and compiles separately under a 512 MiB limit. Resource values are historical output, not an independently measured replay. Compilation is not a physical support run.

## Limitations and next gate

The normal-order expressions are algebraically suitable for avoiding large q10 enumeration, but this small fixture evaluates nested commutators through direct sparse whole-operator compositions. It DOES create q8/q10 intermediate states to compare against the direct physical answer. It does not implement optimized connected-motif local operators, generic translation-normalized q6 matching lookup, or prove their future cost. No new 8×4 contraction was made. There is no new .11 energy endpoint or all-size gap certificate.

Next: independent Cartesian-basis physical verification and term-by-term comparison of this frozen package. Only afterward derive and fixture connected local motif actions and measure their reduced counts/cost before any proposed full-support pass. Existing generic-m4-envelope obstruction remains unchanged.
