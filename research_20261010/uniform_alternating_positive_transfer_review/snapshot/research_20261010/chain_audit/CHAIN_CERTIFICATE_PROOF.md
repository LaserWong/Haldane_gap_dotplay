# Independent audit and all-size bridge for the spin-one alternating chain

Updated 2026-10-10 13:22 EDT, America/New_York, and 17:22 UTC.

## Result and model

For every integer $M\geq2$, consider the periodic chain

\[
H_M(g)=\sum_{i\in\mathbb Z/M\mathbb Z}
 \mathbf S_{i,R}\cdot\mathbf S_{i+1,L}
 +g\sum_{i\in\mathbb Z/M\mathbb Z}
 \mathbf S_{i,L}\cdot\mathbf S_{i,R},
\]

\[
s=1.
\]

There are $2M$ physical spins and the full Hilbert-space dimension is $9^M$.
The strong coupling is one, so all energies and gap bounds below use that unit.
The finite-size convention retains both distinct strong bonds when $M=2$.

The following bounds have passed independent exact-arithmetic verification.
Each row proves a unique ground state and the stated gap for every integer $M\geq2$.

| Weak coupling $g$ | Trial-support depth | Uniform gap lower bound | Largest trial space | Largest full residual support | Largest full Hilbert space |
| --- | --- | --- | --- | --- | --- |
| $1/10$ | 2 | 0.118954972866 | 453 | 5,205 | 43,046,721 |
| $1/8$ | 3 | 0.068202652189 | 5,205 | 43,294 | 43,046,721 |
| $3/20$ | 3 | 0.014789588586 | 5,205 | 43,294 | 43,046,721 |
| $3/20$ | 4 | 0.017013326349 | 43,294 | 245,870 | 43,046,721 |

Each calculation retains one trial vector.
The trial-space dimensions in the table are linear basis dimensions, not MPS bond dimensions.
No whole-space diagonalization is used.
These are sufficient certificates at the listed couplings, not a maximal coupling threshold or a statement about the uniform $g=1$ chain.

The first two rows promote saved candidates to independently verified all-size statements.
The last two rows also close the previously missing short-size bridge.
In particular, the strongest $g=3/20$ bound now covers every $M\geq2$, rather than only $M\geq16$.

## Independent finite-input verification

The verifier `verify_chain.py` imports no source module from `low_energy`, `audit`, or the archived scalar programs.
Its inputs are the saved rational certificate records and integer trial vectors.
It reconstructs the nine two-spin dimer eigenvectors from explicit integer Clebsch–Gordan columns in the physical spin basis.
Their excitation energies are $0,1,3$, with multiplicities $1,3,5$.
It checks their orthogonality and their exact physical dimer eigenvalue equations.

The individual physical spin operators are built independently before the weak-bond kernel is transformed into the unnormalised dimer basis.
The positive diagonal Gram matrix is retained throughout.
For every stored trial vector, the verifier reconstructs $H v$ on every reached configuration, including all configurations outside the trial support.
With $G$ denoting the diagonal metric, it evaluates

\[
\rho=\frac{v^TGHv}{v^TGv},
\]

\[
R^2=\frac{(Hv)^TG(Hv)}{v^TGv}-\rho^2.
\]

Every stored Rayleigh quotient and full residual square is reproduced as an identical rational number.
The reached-support counts and exact nonzero matrix counts also agree.
The verifier checks the periodic weak-bond multiset independently of the stored graph description.

For each local comparison, it reconstructs the two-dimer matrix

\[
g\,\mathbf S_{i,1}\cdot\mathbf S_{j,0}
 +a(h_i+h_j)+bI,
\]

\[
h_i=\mathbf S_{i,0}\cdot\mathbf S_{i,1}+2I.
\]

Congruence by the positive Gram matrix gives a rational symmetric matrix.
Exact rational LDL elimination in the nine conserved-magnetization blocks yields 81 strictly positive pivots.
This is independent of the producer's floating proposal and fraction-free inertia implementation.
All exact pivots are saved in the audit JSON files.

Each dimer has degree two in the weak-bond cycle, including the $M=2$ convention.
Summing the local inequalities gives the full-Hilbert-space comparison

\[
H_M\geq-2M I+\alpha\sum_i h_i-BI,
\]

\[
\alpha=1-2a>0,
\]

\[
B=Mb.
\]

The coefficients of

\[
(1+3x+5x^3)^M
\]

count every reference eigenvalue, including all magnetic sectors.
The verifier reconstructs these coefficients and checks that their sum is $9^M$, that the ground multiplicity is one, and that the first-excitation multiplicity is $3M$.
The min–max principle therefore gives an ordered comparison for every eigenvalue of $H_M$.
In particular, the second eigenvalue is at least

\[
c=-2M+\alpha-B.
\]

Every stored trial satisfies $\rho<c$.
The variational principle gives an eigenvalue below $c$, while min–max permits at most one.
Thus the ground state is unique and the Temple interval is valid in the full Hilbert space,

\[
e_-:=\rho-\frac{R^2}{c-\rho}\leq E_0\leq\rho=:e_+.
\]

No inference of spectral completeness is made from a small residual or from restriction to total magnetization zero.

## Thermal tails and bootstrap

For any positive inverse temperature $\beta$, define

\[
Q_M=e^{\beta e_+}\operatorname{Tr}e^{-\beta H_M}.
\]

The ground interval and the complete ordered spectral comparison give

\[
1\leq Q_M\leq
 e^{\beta(e_+-e_-)}
 +e^{-\beta(-2M-B-e_+)}
 \left[(1+3e^{-\alpha\beta}+5e^{-3\alpha\beta})^M-1\right].
\]

The subtraction removes only the unique reference ground eigenvalue.
All remaining reference bins bound all remaining ordered physical eigenvalues.
For the saved $M=n,2n$ inputs, the verifier reconstructs

\[
S(n,\beta)\geq
 \frac{e^{-\beta(e_+(2n)-2e_+(n))}}{(Q_n^+)^2},
\]

\[
T(2n,\beta)\geq\frac{1}{(Q_{2n}^+)^2}.
\]

It uses independently implemented rational exponential enclosures, including outward argument compression, a positive Taylor series, a geometric remainder, and range reduction.
All saved twelve-decimal downward-rounded seed endpoints agree exactly.
Accepted and rejected temperatures are both replayed.
Every sequential spatial and thermal update agrees exactly.

The homogeneous Heisenberg cell perturbation is invariant under cell exchange and cell time reversal.
The self-adjoint history-transfer construction described in `audit/AUDIT_REPORT.md` consequently gives

\[
Z_M(\beta)=\operatorname{Tr}X_\beta^M
\]

for every integer $M\geq2$.
The transfer operator can have signed spectrum.
The earlier width restriction $\operatorname{width}(v)\leq0.03$ was used to construct a particular analytic seed.
It is not a restriction on this transfer representation.
The present exact finite-input seeds replace that analytic seed.

Once the audited replay reaches defects at most $u\leq1/100$, the established exact recursion and all-integer interpolation imply the uniform gap

\[
\Delta_M\geq\frac{\log(1/(5u))}{\beta_*}.
\]

This bound holds for every integer $M\geq n_*$.

For every saved accepted gap $d$, the new verifier independently checks the equivalent sufficient inequality

\[
e^{\beta_*d}<\frac1{5u}
\]

using an upper rational enclosure of the exponential.
The strongest saved seed for each row reaches $n_*=8,8,32,16$, respectively.

## A finite-window interpolation lemma

The remaining $g=3/20$ sizes can be controlled before the scalar replay reaches its small-defect acceptance region.
This step requires neither a new trial state nor a new physical Hamiltonian calculation.

Let $n\geq2$ be even and suppose the transfer representation holds for all integer sizes.
Assume

\[
S(n,\beta)\geq1-p,
\]

\[
T(2n,\beta)\geq1-q,
\]

\[
S(2n,2\beta)\geq1-p',
\]

with all three lower bounds in $(0,1]$.
Write

\[
A=(1-p)^2(1-q)>\frac12,
\]

\[
w=\frac{1+\sqrt{2A-1}}2,
\]

\[
r=\frac{1-w}{w}.
\]

Then every integer $n\leq L\leq2n$ obeys

\[
T(L,\beta)\geq
 C:=(1-p)(1-q)(1-p')(1-r).
 \tag{1}
\]

If $C>1/2$, its Gibbs state has a unique largest eigenvalue and hence a unique ground state.
The finite-size gap satisfies

\[
\Delta_L\geq\frac{\log(C/(1-C))}{\beta}.
 \tag{2}
\]

To prove Eq. (1), set $Y=X_{2\beta}$.
The physical bound $T(n,\beta)\leq1$ gives

\[
S(n,2\beta)\geq S(n,\beta)^2T(2n,\beta)\geq A.
\]

Since $n$ is even, the normalized eigenvalues of $Y^n$ form a probability distribution.
Its largest weight $w_0$ is unique and exceeds $1/2$.
Its purity is at most $w_0^2+(1-w_0)^2$, so $w_0\geq w$.
The corresponding eigenvalue $\mu_0$ of $Y$ is the unique eigenvalue of maximal absolute value.
It must be positive, since otherwise sufficiently large odd traces of $Y$ would be negative, contradicting $Z_m(2\beta)>0$ for all odd $m\geq3$.
Thus

\[
\sum_{j>0}|\mu_j/\mu_0|^n
 =\frac{1-w_0}{w_0}\leq r<1.
\]

For every $L\geq n$, the corresponding $L$-power tail is at most $r^{L/n}\leq r$.
The normalized $2n$-power spectrum has purity at least $1-p'$, so its largest weight is at least $1-p'$.
For $t=L/(2n)\in[1/2,1]$, these facts imply

\[
Z_L(2\beta)\geq
 [(1-p')Z_{2n}(2\beta)]^t(1-r).
\]

Hölder interpolation of the absolute eigenvalues of $X_\beta$ gives

\[
Z_L(\beta)\leq
 Z_n(\beta)^{2-2t} Z_{2n}(\beta)^{2t-1}.
\]

The endpoint powers $n$ and $2n$ are even.
The odd-size upper bound follows from the absolute spectrum and therefore does not assume transfer positivity.
Dividing the previous two inequalities yields

\[
T(L,\beta)\geq
 S(n,\beta)^{2-2t}T(2n,\beta)^t(1-p')^t(1-r).
\]

Every displayed exponent is in $[0,1]$, which proves Eq. (1).
For Eq. (2), the largest Gibbs weight is at least $C>1/2$.
The ratio of the second largest weight to the largest is at most $(1-C)/C$.

## Exact short-size bridges

The product of strong-bond singlets has energy expectation $-2M$.
The same local form bound used above therefore gives

\[
\Delta_M\geq1-2a-Mb.
\]

Using each eight-dimer certificate's $a,b$, the minimum for $2\leq M\leq7$ is as follows.

| $g$ | $a$ | $b$ | Gap lower bound through $M=7$ |
| --- | --- | --- | --- |
| $1/10$ | $4/25$ | $10809994061/250000000000$ | $94330041573/250000000000=0.377320166292$ |
| $1/8$ | $1/5$ | $422265393/7812500000$ | $1731642249/7812500000=0.221650207872$ |
| $3/20$ | $6/25$ | $12971992873/200000000000$ | $13196049889/200000000000=0.065980249445$ |

For $g=1/10$ and $g=1/8$, the bootstrap already covers all integer $M\geq8$, so these local bounds finish the proof.

For the depth-four $g=3/20$ certificate, the saved $\beta=56$ seed after one update gives $n=8$, $\beta=112$, and

\[
p=\frac{39656465973}{10^{12}},
\]

\[
q=\frac{4471380797}{500000000000},
\]

\[
p'=\frac{553159287}{125000000000}.
\]

Here

\[
A=\frac{457006077346339069695437124335106987}{500000000000000000000000000000000000}.
\]

The exact integer-square-root check proves

\[
\sqrt{2A-1}\geq
 \frac{909958410799832257246799256247}{10^{30}}.
\]

This gives the rational dominant-weight and tail bounds

\[
w\geq\underline w
 =\frac{1909958410799832257246799256247}{2\times10^{30}},
\]

\[
r\leq\overline r
 =\frac{90041589200167742753200743753}{1909958410799832257246799256247}.
\]

Substituting the rational upper tail into Eq. (1) yields

\[
T(L,112)\geq C_4
 =\frac{53889081096057441545975996112687682818262621240974865627096877391}
 {59686200337494758038962476757718750000000000000000000000000000000}
 >0.90287337426980
\]

for every integer $8\leq L\leq16$.
The independent rational exponential enclosure verifies

\[
e^{112(19906846147/10^{12})}<\frac{C_4}{1-C_4}.
\]

Consequently the gap throughout this window is at least $0.019906846147>0.01990$.
It exceeds the large-size gap $0.017013326349$.
Together with the $M\leq7$ local estimate, this proves the depth-four all-size result.

For the depth-three $g=3/20$ certificate, the same construction gives the following independently verified windows.

| Integer cell sizes | Inverse temperature | Thermal-purity lower bound, display | Certified window gap |
| --- | --- | --- | --- |
| $8\leq M\leq16$ | 112 | 0.8476862623493034 | 0.015326501218 |
| $16\leq M\leq32$ | 224 | 0.9760394642846504 | 0.016549530751 |

The exact rational purity values and square-root enclosures are stored in its independent audit JSON.
Both window bounds exceed $0.014789588586$, which is already valid for all integer $M\geq32$.
The local estimate covers $M\leq7$, completing that row as well.

## Reproduction and scope of the audit

From the repository root, run

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python research_20261010/chain_audit/verify_chain.py
```

The script uses Python integers, `fractions.Fraction`, and NumPy only to read the saved integer `.npz` vectors.
It does not call an eigensolver.
The local basis, Hamiltonian action, LDL positivity test, exponentials, and sequential scalar replay are independently implemented.
The finite-window proof above was also checked independently by the parent researcher.

The final four-certificate replay took 17.52 seconds wall time on this shared executor.
Its peak reported RSS was 87.63 MiB, with BLAS threads set to one and the process address space limited to 2 GiB.
Individual wall times and actual resource measurements are in `summary.json`.
An earlier full replay took 14.24 seconds, illustrating ordinary shared-machine timing variation.
These figures describe verification of existing integer trial artifacts, not the cost of proposing the original trial states.

All new artifacts are under `research_20261010/chain_audit`.
The pre-existing scientific archive is unchanged.
The source records remain historically labelled as conditional or provisional, since this audit does not rewrite baseline files.
The theorem statements in this document supply the explicit scope upgrade.

This is an executable exact-arithmetic mathematical certificate, not a formal proof-assistant verification.
The audit establishes the listed finite-coupling statements and does not assert optimality of the gaps, support dimensions, seed sizes, or coupling range.
