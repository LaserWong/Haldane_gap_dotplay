# Independent refined short-size bridge

Scope: ordinary periodic spin-1/2 bilayer, rung exchange one, equal intralayer coupling g, positive-direction edges counted with multiplicity. Only integer L=2,...,7 are covered here. No all-size or bootstrap conclusion follows from this package.

## Physical trial and exact local factors

Set H'=H+3N/4=Q+(g/2)A, where A=2 times the sum of the two layer exchanges on each weighted graph edge. Let Omega be the normalized rung-singlet product and B=A Omega. On two rungs, A=P02+P13-I follows from 2 S_i.S_j=P_ij-I/2. The independent code constructs these physical swaps, converts them to the unnormalized rung basis (s,t+,t0,t-), and keeps its exact metric (2,1,2,1). Relative to the vacuum metric, the local pair amplitudes are (-2,1,-2) in the (+,-),(0,0),(-,+) channels; their squared norm is3. This is an exact physical four-spin calculation, not a projected effective Hamiltonian assumption.

For combined edge weights w_e, write S=sum w_e², M=sum w_e³ and T=sum over unordered triangles of the three-edge weight product. Different pair supports are orthogonal, so <B|B>=<Omega|A|B>=3S. The diagonal local pair contribution is -6 per weighted cube. Off-diagonal pair-support contributions require one shared vertex and the third graph edge: each triangle supplies six oriented pair transitions of amplitude3, hence18T. Thus <B|A|B>=-6M+18T. The independent program additionally contracts the complete sparse B support against every physical graph edge for every L=2,...,7 and verifies this identity directly.

L2 has four distinct edges of weight2: S16,M32,T0, pair slope k=-2. L3 has18 unit edges and6 triangles: S18,M18,T6, k=0. L4,...,7 have S=M=2L², T0, k=-1. No bipartiteness assumption enters; odd L and L3 triangles are retained. The physical Hilbert dimensions are4^(L²), while the Rayleigh trial dimension is only2.

Since B has precisely two triplet rungs, the orthonormal trial basis Omega,B/sqrt(3S) gives

 R(g)=[[0,g sqrt(3S)/2],[g sqrt(3S)/2,2+kg]], k=(-M+3T)/S.

Its lower eigenvalue U=(2+kg-sqrt((2+kg)²+3Sg²))/2 is an upper bound on the true ground energy of H'. No residual or exact-eigenvector claim is needed for this upper bound.

## Full-Hilbert second-level lower bound

The accepted quadratic-boson proof is copied with its immutable manifest. The independent local calculation also checks, by exact semidefinite elimination in the rung metric, A_pres+Q_i+Q_j>=0. Summing the weighted-degree-four graph yields the preserving comparison (1-2g)Q. The physical creation term is the hard-core compression of the bosonic pair term with K=(g/2) adjacency tensor J, where J is an orthogonal color matrix. This embeds the entire physical space of dimension4^N into3N boson modes, not one symmetry sector.

Weighted degree4 implies ||K||=2g, and half Tr(K²)=3g²S/4. For0<=g<1/4, alpha=1-2g>2g, so diagonal oscillator frequencies are at least delta=sqrt(1-4g). Their vacuum shift is at least Eb=-(3g²S/4)/(alpha+delta)=(3S/16)(2g-1+delta). Ordered min-max under finite hard-core compression gives lambda_j(H')>=lambda_j(Eb+delta Qref). Reference shell0 has multiplicity1; shell1 has3N. Consequently the second eigenvalue of the COMPLETE physical Hamiltonian obeys lambda2(H')>=C(2g-1)+(C+1)delta, C=3S/16. No retained trial-space count is substituted for a full-Hilbert count.

Subtracting U gives the certified gap function F_L(g). If F_L(g)>0, a ground trial lies strictly below the full second-level lower bound; hence the physical ground is unique and its gap is at least F_L(g). Shifting H by3N/4 cancels from the gap. Negative lambda2 or U individually do not impair this argument.

## Fixed rational interval certificates

Every saved interval also specifies a single rational trial Omega-tB. Its norm is1+3St² and its exact Rayleigh mean is3S[(2+kg)t²-gt]/(1+3St²), affine in g. The full lambda2 comparison minus this fixed affine mean is concave, so its minimum on[0,b] is at one of the two endpoints. Both endpoints and the fixed trial norm/means are checked independently. This verifies the actual saved fixed-trial interval certificates, in addition to the optimized envelope proof below. The additional positive ranges[0,.1525] and[0,.1528] have downward gap bounds .006136044669 and .000696608341 respectively. Negative diagnostic ranges remain failed bounds.

The unexecuted three-state proposal is checked only as a budget: its current two-state shortfalls follow from exact trial eigenvalue lower endpoints versus the chosen sufficient target. Its upper support count9[binom(98,2)-49binom(4,2)]=40131 is verified. No three-state computation or universal no-go is inferred.

## Continuous monotonicity, roots and rounding

Let D=(2+kg)²+16Cg². For k=-2,0,-1 and g>=0,
 D-4(1-4g)=(4k+16)g+(k²+16C)g²>=0.
Thus D^(3/2)>=8 delta³. Direct differentiation gives
 F_L(0)=1, F_L'(0)=-2,
 F_L''(g)=-4(C+1)/delta³+32C/D^(3/2)<=-4/delta³<0.
Therefore every F_L is strictly decreasing throughout[0,1/4), and its minimum on a closed interval[0,b] occurs at b. This proves the continuous result rather than inferring it from a point scan. The exact positive and negative endpoint signs bracket a unique zero for each of these fixed comparison functions. L7's upper root endpoint is smaller than every other lower root endpoint, establishing it as the first failure of this particular short-bridge method. A negative bound beyond its zero says nothing about the actual physical gap.

Independent square-root enclosures use288 bits, stronger than the producer224 bits, and verify all saved directed endpoints. For the ground U upper endpoint, the square-root LOWER endpoint must be subtracted. For the lambda2 lower endpoint, the delta LOWER endpoint must be added. These produce a rigorous gap lower endpoint. Endpoint g=3/20 verifies the downward decimal bound .050426624396 uniformly for all six sizes and every real0<=g<=.15. Positive/negative test points and all six root brackets are checked independently. The limiting root is near .152838312159836, a fixed-method limitation only.

## Reproduction and limits

The checker imports no producer code. It independently reconstructs physical swaps, weighted graphs, every sparse moment, local preserving positivity,288-bit directed bounds, all root brackets and monotonicity coefficient signs. Three deliberately incorrect energy/gap endpoints are rejected. REPRODUCE.sh checks immutable hashes and compares scientific results from a fresh directory. CPU4, at most120CPU seconds and100MiB per batch. No root, producer or remote files are modified.

The producer’s separate PROSE_ERRATUM.json is hash-pinned. The outward decimal lower bracket is .15283831215983547, rather than the nearest-rounded .15283831215983548 in the frozen prose; the upper is .15283831215983637. Both corrected decimal directions are checked against the saved rational bracket. The original displayed decimal lower also has a positive sign, checked independently, but is not its outward rounding. No numerical certificate changes.
