from explore_fake import *
import itertools
M = int(sys.argv[1]); sector = sys.argv[2]; big = [F(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 and sys.argv[3] else []
J, N = targets(M); T = J if sector == 'J' else N
ks = list(range(4, M+1))
r = {k: T[k] - sum(b**k for b in big) for k in ks}
print('residual targets', {k: float(v) for k, v in r.items()})
act, res = nnls_out = solve_bulk(r, ks)
print('nnls res', res, 'active', [(round(y,4), round(w,3)) for y, w in act])
