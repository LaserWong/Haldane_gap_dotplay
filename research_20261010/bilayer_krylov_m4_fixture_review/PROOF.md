# Independent small-geometry fourth-moment fixture

Scope: ordinary bilayer H'=Q+(g/2)A, g=11/100, integer T=200H'=200Q+11A, periodic4×2 and5×2 rung tori with weighted parallel edges. These fixtures test the proposed normal ordering on full physical small geometries. They do not compute the8×4 optimized witness's moments, prove a production cost estimate, or certify a new energy/gap.

## Independent physical representation

The reviewer uses sparse Cartesian rung states, separately from the producer's magnetic triplet states. The normalized rung basis is s=(up down−down up)/sqrt2, tx=(down down−up up)/sqrt2, ty=i(up up+down down)/sqrt2, tz=(up down+down up)/sqrt2. An exact16×16 local check obtains Aedge directly from the two physical spin-half layer exchanges: Aedge=Player1+Player2−I. Basis transformation divides the unnormalized tensor inner product by4. Every local matrix entry is compared exactly with the independent Cartesian action.

In Cartesian coordinates C† creates the sum of equal-color triplet pairs, C annihilates it, and D hops a singlet/triplet or acts on two triplets as swap minus trace. The equal-color pair Ω is the same vector as t0t0−t+t−−t−t+ in the magnetic convention. Complex arithmetic is confined to the16×16 basis check, with Gaussian integers of very small magnitude exactly representable; all physical support contractions use Python arbitrary-precision integers.

Graph sites use index x*2+y. Each site supplies positive horizontal and vertical edges. Repeated vertical edges are retained, hence weighted degree4, including on the two-row torus. Neither translation symmetry nor a projected Hilbert space is assumed.

The common unnormalized singlet trial is ψ=3vac−2Ω01+Ω01Ω23−Ω01Ω23Ω45+2Ω02Ω13Ω46. Each pairing has disjoint endpoints. It has even occupation q≤6 and is an SU(2) singlet. The Cartesian implementation is separately written and does not call the producer's action code.

## Exact checks

Let m=ψ6, χ=Tψ, K=[C,C†], E=[D,C†], N=[C,E], L=[[C,K],C†]. All commutators are implemented with their ordered signs. The checker compares:

1. The four separate terms 2< Cm,C Dm>, −<Cm,D Cm>, <Km,Dm>, <m,Nm> against <C†m,D C†m>.
2. The complete third moment <χ,Tχ> against the sum of lower-sector diagonal/cross terms and the normal-ordered q8 contribution.
3. Every q≤6 component of Tχ against its normal-ordered image, replacing the q8-to-q6 contribution by 121(C†Cm+Km).
4. For v=17600m+11χ6+121Dm, the q8 component C†v+121Em against direct (Tχ)8. Its norm is checked from separate ||Cv||², <v,Kv>, both oriented interference terms 242<v,ECm> and242<v,Nm>, and14641(||E†m||²+<m,[E†,E]m>).
5. The five q10 base terms ||C†Cm+Km||², 2<Cm,CKm>, −<Cm,K Cm>, ||Km||², <m,Lm> against ||(C†)²m||². Multiplying by14641 gives the actual q10 norm of Tχ.
6. The sum of all sector norms, including q10, against the direct fourth moment ||T²ψ||².

The4×2 geometry cannot occupy q10 and tests exact cancellation among its q10 terms. The5×2 geometry must have strictly positive q10 norm. Dropping that sector cannot pass. Saved term comparisons also retain the negative K4 contribution and signed nested-commutator values, rather than merely checking a positive total. Dividing integer moments by norm(ψ)*200^k gives the normalized physical moments of H'.

## Limits and next gate

These checks validate the physical local conventions and normal-order identities on the specified trial vectors and geometries. The earlier symbolic review proves the free-algebra identities for arbitrary vectors. The fixture computes sparse small-system raising images directly; it does not yet implement a q≤6-only production motif engine or establish its cost. In particular, a full8×4 exactm4 run requires a separate implementation, explicit amplitude/product overflow bounds, measured motif/cache counts, and a new resource authorization. No projected H² substitution is made.
