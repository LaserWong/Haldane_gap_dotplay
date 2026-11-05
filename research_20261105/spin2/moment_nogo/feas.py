from explore_fake import *
LAM = F(100001,100000)
def feasible(M, sec, big, c=0.99):
    J, N = targets(M); T = J if sec == 'J' else N
    ks = list(range(4, M+1)); r = {k: T[k] - sum(b**k for b in big) for k in ks}
    act, res = solve_bulk(r, ks, c=c, ngrid=1201)
    return res < 1e-7
def bis(M, sec, sign, withlam):
    lo, hi = 0.0, 0.995
    for _ in range(14):
        m = (lo+hi)/2; big = ([LAM] if withlam else []) + [F(sign*m).limit_denominator(10**6)]
        if feasible(M, sec, big): lo = m
        else: hi = m
    return lo
if __name__=='__main__':
 for M in (6, 7, 8, 9, 10, 11, 12):
  print(M, 'J+t', round(bis(M, 'J', 1, True), 4), 'J-t', round(bis(M, 'J', -1, True), 4), 'N+s', round(bis(M, 'N', 1, False), 4), 'N-s', round(bis(M, 'N', -1, False), 4), flush=True)
