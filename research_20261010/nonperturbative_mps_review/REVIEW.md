# Independent review of the nonperturbative MPS assessment

Updated 2026-10-10 17:01 EDT / 21:01 UTC.

## Verdict

**PASS for the four new claims within their stated scope.** The review independently reconstructs the AKLT local operators, the D26 MPS norm and Heisenberg insertion, the exact small-chain Rayleigh quotients, and the all-temperature scalar exclusions. It supplies a direct all-length AKLT uniqueness proof and an explicit four-site-to-periodic counting argument, including the shortest claimed length L=5.

The assessed directory is `../nonperturbative_mps_assessment`. Its frozen manifest SHA-256 is `95a37af759e80d9030b2f99ac7d86c26b6cd6085e5746a883514b9d66b7e4eb7`. All 17 manifest entries were verified. No assessed, frozen, root, or GitHub files were changed. The shared snapshot has no Git metadata. The original Haldane manuscript PDF is absent and was not read.

### Accepted claims

1. The untwisted space/time initialization applies to uniform integer-spin Heisenberg chains, with even starting spatial length, a consistent extensive energy shift, and certified upper traces at the smaller size and both temperatures. A physical MPS Rayleigh contribution supplies only a lower numerator. It does not replace the upper I/P/C or sector moments in the existing filter proof.
2. The fixed archived D26 one-Rayleigh numerator at lengths 12 and 16 cannot start a successful certificate at denominator sizes 6 and 8 through the specified G updates, for any beta>0. This remains true with exact denominator traces. Immediate canonical conversion and the fixed continued time-first order both fail. The additional review checks also exclude a one-off canonical conversion after any completed positive time-first cycle before that failure.
3. For the explicitly normalized periodic AKLT Hamiltonian H=sum P2, the Pauli D=2 state is nonzero, genuinely entangled, and the unique ground state for every L>=3. Exact four-site positivity and periodic bond counting prove gap>=1/10 for every L>=5. Exactly 3^L-1 omitted states then have energy at least 1/10.
4. The exact realignment value -1/3 on Q=diag(1,-1,0) obstructs the current same-real-factor sufficient transfer construction in the Cartesian real structure, including scalar and onsite adjustments. It does not exclude all other thermal transfer constructions or inequalities.

### Conditional or inherited statements

- The old spin-1 gap bound 0.005908566393 for L>=1920 and its full finite I/P/C input validation are inherited background, not newly re-certified here.
- The spin-2 D124 witness, its contracted lengths, and its previously certified heat data are inherited background. This review checks the integer-spin algebraic extension, not a spin-2 numerical campaign.
- Matching the archived D26 matrices to the absent original manuscript is outside this review. Their interpretation as a legitimate physical trial state follows directly from the explicit matrices rebuilt here and does not need that manuscript.
- A thermal-bootstrap application of AKLT and a quantitative transfer of its spectral count to the bilinear Heisenberg model remain open. The independent AKLT gap certificate itself does not depend on those missing steps.

### Rejected overextensions

No primary claim above was rejected. The following stronger conclusions are not supported and must not be substituted for them.

- Replacing required upper seam or sector moments by an untwisted MPS lower trace.
- Treating the all-beta screen as an exclusion of adaptive order changes, sharper squaring inequalities, richer numerator spaces, larger seeds, all MPS methods, or a physical gap.
- Applying the uniqueness count to periodic L=2, whose Hamiltonian is 2P2 and has a four-dimensional kernel.
- Identifying the four-dimensional AKLT MPS norm transfer with a complete thermal transfer.
- Promoting the negative realignment witness to a universal impossibility theorem.

## 1. Untwisted ordering and the role of seam moments

In a real orthogonal integer-spin representation, the spin generators have the form S_alpha=i A_alpha with real antisymmetric A_alpha. The antiferromagnetic interaction obeys -S dot S=sum A_alpha tensor A_alpha. The positive bond-history expansion therefore gives a real symmetric Hilbert-Schmidt kernel. Bounded local matrices and a finite exponential history measure justify absolute convergence and cyclic contraction. For one consistently shifted family,

    Z_L(t)=Tr exp[-t(H_L+aL)]=Tr X_t^L,  L>=2.

The L=2 contraction uses two distinct bond histories and reproduces the parallel-bond convention. No odd-length sign claim is needed to initialize the argument. At an even n, the weights lambda(X_t)^n are nonnegative. Consequently both

    P_x(n,t)=Z_2n(t)/Z_n(t)^2 <=1,
    P_t(n,t)=Z_n(2t)/Z_n(t)^2 <=1

are ordinary purities. A fixed normalized state with total Rayleigh quotient R at 2n gives exp(-2 beta R)<=Z_2n(2 beta). Any complete upper traces U0>=Z_n(beta) and U1>=Z_n(2 beta) yield

    J_lower=exp(-2 beta R)/U0^4,
    C_lower=exp(-2 beta R)/U1^2.

All extensive shifts cancel from these ratios. With G(z)=1-(1-z)^2/(2z^2), the square identities give

    a=G(J_lower), b=G(C_lower^2 a).

These bound P_t(2n,2 beta) and P_x(2n,4 beta), respectively. They are a staircase. Canonical conversion at base (2n,2 beta) gives S=a sqrt(b), T=a^2 b. This follows from e c^2>=a^2 b and c,e<=1, where c and e are the canonical space/time entries. G is increasing for 0<z<=1 because G'(z)=(1-z)/z^3. Every use requires positive preceding lower arguments.

I/P/C denote seam rotations and their character combinations denote transfer sectors. They are not doubling directions. The old positive filter lambda^6(-2+10 lambda^2)^2 has a positive tenth-moment coefficient. Its upper bound still needs an upper tenth sector moment. Variationality supplies no replacement upper bound. This is a direction-of-inequality issue rather than a dimensional issue.

## 2. Independent D26 and all-beta tests

`rebuild_d26.py` reconstructs all 26-dimensional local matrices from the archived scalar parameter table, constructs the orthonormal spin-z physical bond operator, and sums its matrix elements into the two-site insertion. The rebuilt difference blocks are byte-identical to the archived blocks. Direct product-basis amplitudes at L=2 and L=3 independently match their norm and total physical Heisenberg expectation, including both L=2 bonds.

`contract_d26.cpp` uses sequential multiplication by T, unlike the producer's exponentiation schedule. It obtains the exact U_L and V_L at L=12,16,20. All six integers agree with the frozen output. The relevant total energies are R=2n U_2n/V_2n, not just the per-site quotient.

`independent_uniform.py` embeds each stored small trial vector in the entire 3^n spin-z basis and applies the physical Hamiltonian there. It independently obtains the stored exact Rayleigh quotient alpha_n and checks Tr H_n=0. The nonzero supports are 141 and 1107. They are trial support sizes, not complete low-energy multiplicities.

For beta>0, trace Jensen and trial Jensen give

    Z_n(beta)>=3^n,  Z_n(beta)>=exp(-beta alpha_n).

Writing delta=R-2 alpha_n gives delta=0.365339682084205... at n=6 and delta=0.227135956266657... at n=8. Both are strictly positive rational numbers. For the fixed lower-numerator recipe,

    J_lower<=min(exp(-2 beta R)/3^(4n), exp(-2 beta delta)),
    C_lower<=exp(-2 beta delta).

These bound what the recipe can certify. They do not upper-bound the actual physical ratio using a variational numerator.

Splitting beta at 3/4 and 31/40, respectively, proves J_lower<29/50 and J_lower<71/100. Independent rational Taylor bounds with geometric remainders certify both halves. The optimistic C=1 canonical replay fails on the first spatial update at n=6 and the fifth at n=8. None enters the accepted defect region before failure.

For beta<=1/2, the dimension term gives J_lower<2/5 and G(J_lower)<0. For beta>=1/2, exp(-delta)<4/5 bounds C_lower. The stronger optimistic time-first replay fails at its first further cycle for n=6 and second for n=8. The exact positive pairs before those failures decrease componentwise. Independently converting each such pair to canonical form also fails, so the phrase “delaying conversion” is valid for a one-off conversion at these completed cycles. Arbitrary mid-cycle or repeated adaptive changes remain outside the result.

The separate beta=21/2 cooling demonstrations reproduce J_lower=C_lower=0.000462743350338407... and 0.008284536832150347.... They use Z_n(2 beta)<=Z_n(beta)^2. They do not misidentify an archived beta trace as an independently computed 2 beta trace.

## 3. Exact AKLT normalization and local proof

`independent_aklt.py` starts from Cartesian spin generators (S_a)_bc=-i epsilon_abc. It verifies S^2=2I, forms B=S dot S, and constructs

    h=(B^2+3B+2I)/6=P2=(I+F)/2-|Omega><Omega|/3.

Thus h is a rank-five projector, with coefficient one in the many-body Hamiltonian. A convention using B+B^2/3+2I/3 would instead equal 2h and would rescale every gap by two. Neighboring h terms are checked to be noncommuting.

The independent positivity test does not reuse the producer's rational pivots. It writes the full local operator in the product basis, checks its occupation-parity decomposition, and uses integer characteristic polynomials of each block. For a real symmetric matrix M, nonnegative elementary symmetric coefficients ensure that (-1)^d det(-xI-M) has no positive root. Hence M has no negative eigenvalue. The number of trailing zero coefficients gives the nullity.

With B4=6 H4_open, the test proves

    5 B4^2-12 B4 >=0,

which is exactly 180[(H4_open)^2-(2/5)H4_open]>=0. The full local dimension is 81 and the maximum block dimension is 21. The kernel dimension is four. Open lengths 2 and 3 and periodic lengths 3,4,5 are independently checked. The periodic L=5 test also directly verifies H5^2-(1/10)H5>=0, independently of the general counting argument below.

## 4. Ground-space counting without a large-system diagonalization

The local kernel relations on amplitudes are

    ...aa... = ...bb...,
    ...ab... = -...ba...  for a!=b.

They are the homogeneous Clifford-word relations x^2=y^2=z^2=q and xy=-yx, with q central. Bubble sorting and cancellation reduce every degree-L word to at most four normal forms. For L=2k the forms are q^k and q^(k-1)xy, q^(k-1)xz, q^(k-1)yz. For L=2k+1>=3 they are q^k x, q^k y, q^k z and q^(k-1)xyz. Their Pauli realizations are linearly independent. This gives the complete four-dimensional open ground space for every L>=2.

Periodic seam constraints reduce that dimension to one.

- For even L=2k>=4, fix distinct b,c and let a be the third letter. Apply the equal-diagonal seam relation to the word a q^(k-2) b c a, replacing the two end a's by b's. The two words reduce to opposite signs of q^(k-1)bc. Every two-letter normal form therefore has zero amplitude.
- For odd L=2k+1>=3, choose a!=b and apply the seam relation to a q^(k-1) b a. Replacing the end a's by b's equates -q^k b with q^k b. Every one-letter normal form therefore has zero amplitude.

Only one normal form remains in either parity. The periodic Pauli trace state is nonzero and annihilated by every h, so that last degree of freedom is present. The ground state is unique for every L>=3. At L=2 the doubled bond still has kernel dimension four and is explicitly excluded.

The modern parent-intersection theorem provides an independent cross-check. Its hypotheses and size bound agree with L0=ell=2 and Int(2,3), verified here by rank-four Pauli spans and the exact three-site kernel. The statement and the AKLT example were checked in the primary article [Schuch, Molnár and Pérez-García, Simple Hamiltonians for Matrix Product State models, arXiv:2503.10767v2](https://arxiv.org/html/2503.10767v2), around Eq. (3). This is a check of that source, not of the absent original Haldane manuscript.

The norm transfer has eigenvalues 3,-1,-1,-1, giving norm 3^L+3(-1)^L. Every nonzero trace amplitude has squared magnitude four. The number of nonzero amplitudes is therefore [3^L+3(-1)^L]/4. A one-site reduced density matrix is I/3 by rotation invariance, also checked exactly at L=3,4,5,6. The state is entangled. D=2, the one-dimensional retained span, and the exponentially large amplitude support are distinct quantities.

## 5. Four-site-to-periodic gap and shortest wrapping

Let h_i act on cyclic bond (i,i+1), and define A_i=h_i+h_(i+1)+h_(i+2). For every L>=5, each A_i is an open four-site Hamiltonian tensored with identities. The local inequality gives

    sum_i A_i^2 >= (2/5) sum_i A_i = (6/5) H.

Every bond occurs in three windows. Every adjacent unordered bond pair occurs in two. Every pair at cyclic bond distance two occurs in one, including at L=5. All remaining pairs occur in zero. Therefore

    H^2+(1/2)H-(1/2)sum_i A_i^2 >=0.

To see the sign, adjacent anticommutators cancel. A distance-two anticommutator has coefficient 1/2 and every more distant anticommutator has coefficient one. Such pairs act on disjoint sites, so their products are positive. No unexamined negative overlapping-bond remainder remains. The coefficient counting is also tested explicitly at every L from 5 to 20, while the cyclic-distance argument proves the general case.

Combining the inequalities gives H^2>=(1/10)H. Frustration freeness and the uniqueness established above then give gap(H)>=1/10 for every periodic L>=5.

This is the n=4 specialization of Knabe's criterion. The primary source [Gosset and Mozgunov, Local gap threshold for frustration-free spin systems, Theorem 1](https://arxiv.org/pdf/1512.00088) states the required range m>n, with nearest-neighbor translation-invariant projector terms and nonempty kernel. The m>2n condition elsewhere in the same paper belongs to its improved Theorem 3 and is not required here. The independent count above resolves that distinction directly for the claimed L=5 onset.

## 6. Complete omitted spectrum and transfer obstruction

The Hilbert dimension is 3^L. Removing the one exact zero state leaves exactly 3^L-1 eigenstates counted with multiplicity. All have energy at least 1/10 for L>=5. Hence

    1<=Z_L(beta)<=1+(3^L-1) exp(-beta/10).

The independent rational bound exp(-x)<=(1+x/4096)^(-4096) verifies upper tails below 0.000761603 at L=8,beta=160 and 0.001742971 at L=16,beta=240. Both traces are below 1.01. These are separate finite examples, not a thermal-bootstrap staircase.

For the existing same-real-factor transfer proof, realignment of -h would need to be positive semidefinite. Its quadratic form on Q=diag(1,-1,0) is exactly -1/3. An identity shift contributes (Tr Q)^2=0. A one-site adjustment contributes a factor Tr Q=0. Real orthogonal basis changes preserve the obstruction. Thus this sufficient construction fails in the stated real structure. The result does not address different structures, enlarged transfer representations or a replacement inequality.

The Pauli norm transfer contracts one state's norm. It has no beta dependence and omits every excitation. Its existence proves no identity Tr X_beta^L=Z_L(beta). The AKLT omitted-state certificate remains a valid entangled-reference example despite that separate missing thermal-transfer step.

## 7. Reproduction and remaining work

Run `./REPRODUCE.sh` in a disposable copy of this review directory if the sealed review outputs must remain unchanged. It reads the sibling assessment and archived scalar parameters but writes only review outputs. The script pins one allowed CPU, limits virtual memory to 1 GiB, and executes all stages sequentially. It requires Python, SymPy, NumPy, g++, and GMP. No eigensolver, full spin-2 campaign, or large-length many-body matrix is used.

`aklt_independent_results.json` contains full characteristic-polynomial coefficients, small periodic checks, wrapping counts, and thermal examples. `uniform_independent_results.json` contains exact Rayleigh values and every optimistic failure. `d26_rebuild_results.json` and `d26_fresh.out` record the independently rebuilt contractions. `INPUT_SHA256.json` records consumed source identities. `CLAIM_VERDICTS.json` gives machine-readable scope. `MANIFEST_SHA256.json` and `SEAL.json` seal this review.

The useful next scientific question remains either a sharper certified denominator at a larger uniform-chain seed, a genuinely richer numerator, or a new AKLT thermal spatial inequality. Merely improving denominator precision at the excluded n=6/8 seeds cannot rescue this fixed one-vector recipe. No such new campaign was launched in this review.
