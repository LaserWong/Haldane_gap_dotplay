# Bounded optimization plan

The first cost projection uses the exact sum of representative count times
stored sparse edge count over all magnetization sectors. It is not M0 worst-case
timing multiplied by a full-space column count.

1. Algebraic parity: a column at v has only ordinary/Eisenstein integer entries
at rows with the same zero-parity g(w), and only sqrt(6)-scaled entries at the
other rows. Store the one active component or active Eisenstein pair. The
similarity factors are 1 and sqrt(6), with physical squared-norm weights 1 and 6.
Prepare the two corresponding integer CSR operators for seed parity +/-.
2. Exact split matvec: for a power-of-two denominator 2^b, write each signed64
x=2^b h+l with 0<=l<2^b. Then floor(sum a*x/2^b)=sum a*h+floor(sum a*l/2^b).
Both sums fit signed64 under the audited row bounds, avoiding signed128 sparse
multiplications while retaining exactly the original floor. The final
coefficient product still uses signed128. Test bitwise against bigint and the
uncompressed implementation before interpreting performance.
3. Small fixed blocks of columns: stream 1/2/4 columns in row-major order,
sharing CSR edge reads and retaining bounded per-column outputs. Chunk files
identify every completed representative; graph construction is amortized over
chunks. The maximum chunk size will be chosen from measured memory and speed,
not from an assumption of unrestricted RAM.

No full L9/L10 campaign is launched by these tests. Large cost reduction is an
experimental goal, not an established claim.
