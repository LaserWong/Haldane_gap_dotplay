# Exact compressed and blocked kernel audit

This extends PROOF.md without changing its target, polynomial, or error budget.
The mathematical parity invariant removes coordinates that are identically
zero. Define p(w)=number of zero spins mod 2 and, for column v,
D_v(w)=1 when p(w)=p(v), sqrt(6) otherwise. Write X(w)=D_v(w) U(w).
The integer sparse operator is D_v^-1 (512P) D_v. Its real/Eisenstein
coefficients for a ring edge (a,b,c,d) are
 a+f b, c+f d, where f=1 if p(w)!=p(v), and f=6 otherwise.
The new graph stores the two seed-parity cases in int16 coefficients.
The physical norm is sum_w D_v(w)^2 |U(w)|^2, with exact weights 1 or 6.
Coordinate floors in this representation are exactly the corresponding active
coordinate floors in the original four-component representation. Therefore
every integer column and norm is bitwise identical after reinserting zeros.
This is a change of representation, not an approximation.

## Exact signed64 split product

For divisor 2^b, b=8 or 9, write a signed integer x=2^b h+l, 0<=l<2^b.
For arbitrary signed integer coefficients a_j,
 floor(sum_j a_j x_j /2^b)=sum_j a_j h_j+floor(sum_j a_j l_j/2^b).
The signed64 kernel accumulates the high and low sums separately. At row-L1
bound R and coordinate bound B from PROOF.md, absolute partial sums are bounded
by R(B/256+2) and R*511. The implementation checks the first plus B against
INT64_MAX and the second against INT64_MAX. This also covers the recurrence
subtraction, intermediate products, and intermediate expressions such as
(a-b)*v. Final coefficient accumulation still uses signed128, with its earlier
range proof. Compilation uses C++20, whose signed right shift rounds toward
negative infinity; static assertions also check the negative shift and low-bit
identities used by the implementation.

## Blocking

Each sparse row holds Bc independent columns, Bc in {1,2,4,8}. Every lane has its
own seed parity, recurrence, accumulator, and norm. Reusing a graph edge across
lanes changes no addition order within a given lane. A final short block is
padded with zero seeds; padded lanes are neither reported nor counted. The
computation prints and flushes one complete norm per representative. The
benchmark wrapper writes a successful result only after the expected count
and a zero exit status. A production campaign would need the same atomic
per-chunk protocol before a long run; one has not yet been authorized/launched.

The optional phase branch merely specializes the frequent zero-imaginary edge
case. Integer sums are unchanged; this branch needs its own bitwise validation.

## Verified tests and scope

`validate_compressed.py` compares all emitted integer coordinates with the
uncompressed UBSan executable on L3 M0 and L4 M0/M-1, all three twists, block
sizes 1/2/4/8, multiple batches and short final batches. Earlier independent
Python-bigint tests verify the uncompressed result. These tests supplement the
algebraic proof; they do not replace it or certify an uncomputed large trace.
A diagnostic tiny eigensolver was limited to magnetization blocks of dimension
at most 85; no L9/L10 eigensolver or full-spectrum computation is used.

The benchmark build currently retains both the full and compressed CSR graphs
while computing, so peak memory is deliberately conservative. It can release
the old graph after conversion in a production loader, but this additional
memory saving has not been used in the reported results.
