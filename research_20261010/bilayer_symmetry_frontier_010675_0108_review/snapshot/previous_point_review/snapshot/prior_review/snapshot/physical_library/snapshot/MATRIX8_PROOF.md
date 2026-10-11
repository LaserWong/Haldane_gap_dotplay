# Independent complete43D8x4 second-moment matrix

Accepted scope: the complete second-moment matrix J(g)=<basis,H'(g)^2 basis> for the current B15,L14,U14=R14+M14 physical basis on8x4, for all real g as a polynomial identity. This is a43-dimensional trial basis in physical dimension4^32=2^64. It includes the COMPLETE q8 image of q6 trial components. No higher-coupling ground lower endpoint or all-size gap is certified by this package.

## Independent full support stream

The new reviewer checker is built from the immutable independently accepted scalar support engine. It does not include or execute producer code. The exact matching enumeration, loop-count Gram, local swap/cap forms, graph and pair-orbit conventions are preserved. New unprojected column-array functions lift the accepted scalar actions to all14 U columns. They compute q4 P and CM, q6 T, and the signed commutator as direct bilinear forms. Checked matrix accumulation is added. The source generator is supplied so this relationship can be reproduced exactly.

Before its full pass, the shared reviewer checker reproduced every entry of all four4x4 matrices established by the earlier15 independent polarization runs. Three additional independent8x4 scalar runs, on U0,U13 and U3+U10, benchmarked and corroborated the lifted array algebra. The scalar engine and new shared engine are separate implementations of the contractions.

One complete shared pass processed all4495 fixed-origin q4 supports and169911 fixed-origin q6 supports. Translation invariance gives exact factors N/4 and N/6 with divisibility checked. There is no physical q6 cache or q8 support enumeration. Every one of784 entries in PP,TT,CMCM and the signed COMM matrix agrees with the frozen producer. The raw COMM matrix is checked for exact symmetry before any symmetrization. Its entries are not replaced by an absolute value or clipped to positivity.

The code retains q6 supports even when all M amplitudes vanish. There are96705 such supports here, and the separately saved TT contribution has trace4505303808 after translation scaling. It is positive semidefinite and nonzero; removing these supports would change the complete matrix. Skipping the commutator on a zero LEFT M family is valid because that bilinear contribution is exactly zero, but does not justify skipping T.

The exact hard-core identity is
 (C†M)*(C†M)=(CM)*(CM)+M*[C,C†]M.
The right-hand commutator includes negative occupied-edge and occupied-center terms. The checker evaluates them with their signs and then proves the COMPLETE q8 Gram CMCM+COMM is positive semidefinite. It does not require COMM itself to be positive.

## Mixed identities and complete coupling polynomial

The prior fixture proof is copied and pinned. In its notation, the full U image has orthogonal q2,q4,q6,q8 components tCR,4R+tP,6M+tT,tC†M, with t=g/2. Thus
 J_UU=16V+36W+t[8X+10(Y+Y*)+12Z]
       +t²[S*Gpair^(-1)S+PP+TT+CMCM+COMM].
The q2 pair-orbit basis is complete for the invariant singlet q2 image, so the first term in the quadratic coefficient is exact, not an omitted-image approximation.

All H'(B,L) images lie exactly in the current basis. Their independent coordinate map W obeys GW=K[:,B,L]. Therefore their full second-moment rows are W*K and the old principal block is W*GW. This reconstructs every mixed block without contracting43 image columns. The reviewer reconstructs the first-moment and Gram matrices from independently accepted geometry, checks positive Gram rank43, and verifies every identity exactly.

The resulting polynomial coefficients are Q²,(QA+AQ)/2,A²/4. Every entry of all three43x43 coefficients agrees with the frozen producer export. Formal extraction points g=0,+1,-1 are algebra only; no bosonic stability inference is made at those formal points. The polynomial identity is tested at additional rational g. Complete J and J-KG^(-1)K are checked PSD at g=0,.105,-1/3. The latter is nonzero, demonstrating why the projected square KG^(-1)K cannot replace complete H², even at g=0 for the mixed U basis.

The old independently verified optimized.105 vector reproduces its complete second-moment polynomial coefficient by coefficient, not merely one number. The three fresh scalar forms reproduce every new block, q8 norm, M-zero TT norm, and full moment after exact q0/q2 assembly. These tests are corroboration in addition to the independent all-entry support pass, not a substitute for it.

## Sector pencil and global ground obligations

Every basis vector is exactly an SU(2) singlet with even triplet parity: pair singlets and the SU(2)-invariant even-preserving/creation operations defining L,R,M preserve those properties. Rational coefficients preserve the sector. The finite basis is nevertheless not invariant under H', as the positive omitted-image Gram demonstrates.

For an exact even-singlet vector and ell<a, a negative quadratic witness in
 P(ell)=J-(a+ell)K+a ell G
proves E0>ell ONLY after establishing that the full untruncated applicable sector has at most one level below a. In this model a=r2 is a sector cutoff, not a full-Hilbert second-eigenvalue lower bound. A Rayleigh value below full-Hilbert r1 separately identifies the unique global ground in the even-singlet sector. The complete reference count plus3N verified mutually orthogonal odd-mode/spin directions below r2 then exhausts the low band, so every other even-singlet level is at least r2.

Under these hypotheses, if E0<=ell, all spectral products (E-a)(E-ell) are nonnegative. A negative expectation is impossible, proving the lower endpoint. Equivalently the normalized expectation is variance-(rho-ell)(a-rho). The audit checks equality at the prior accepted.105 Temple lower endpoint and strict opposite signs at ell shifted by±10^-6. New couplings still require fresh cutoffs, exact negative witnesses, odd modes and global-ground counting. All-size claims additionally require the full thermal and scalar continuation audits. A PSD pencil excludes only that finite-span/cutoff test; it is not a universal no-go.

## Arithmetic safety and resources

Unprojected local arrays are stored as signed64-bit integers, but each update checks multiplication/addition overflow and additionally requires the result to lie in signed32-bit range. Direct initial L/M formulas are small sums of edge weights/products (weights1 or2), independently bounded by24. Every outer contraction checks both amplitudes within32-bit range and the Gram-weight factor within±4096; the product is promoted to signed128 bits before multiplication. Each accumulator addition is overflow checked.

A conservative independent bound for a commutator entry is: less than2^74 per term, fewer than2^18 q6 supports, fewer than2^8 matching pairs, and fewer than2^7 separate local commutator terms per support. Thus the absolute sum is below2^107; translation multiplication by N=32 stays below2^112, safely inside signed128 bits. q4 terms have smaller counts. Signed terms are bounded by absolute sums, so cancellation is never needed for safety. These are matrix bounds, independent of prior large-coefficient scalar bounds.

Three scalar benchmark runs cost10.81CPU seconds and13.5MiB;105 polarizations were rejected as unnecessarily expensive after a498.9-second projection. The new shared checker passed its4x4 test in.43CPU seconds and a partial8x4 sample in.27CPU seconds. The partial sample was never used as a physical certificate. Its24.1-second full estimate was only a timing guide. The actual full independent pass used28.63CPU seconds and13.3MiB peak RSS under60CPU seconds/250MiB. Exact43x43 assembly used6.28seconds and25.8MiB.

REPRODUCE.sh validates immutable files, regenerates and rebuilds the independent checker, performs a fresh complete support pass, reruns exact matrix analysis, and compares scientific output. No producer, root or remote files are changed.
