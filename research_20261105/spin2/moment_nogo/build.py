# Propose a fake sector measure: big atoms (given) + bulk clusters with integer weights; solve positions in high precision.
from explore_fake import *
def propose(r, ks, c=0.99, ngrid=1601):
    act, res = solve_bulk(r, ks, c=c, ngrid=ngrid)
    if res > 1e-8: return None, res
    nodes, wts = [], []
    for y, w in act:
        if w >= 0.999: nodes.append(y); wts.append(int(round(w)))
        else:  # replace fractional atom by a unit atom with the same top moment
            nodes.append(y*w**(1/ks[-1])); wts.append(1)
    return (nodes, wts), res
def solve(r, ks, nodes, wts):
    n = len(nodes); p = len(ks)
    order = sorted(range(n), key=lambda i: -wts[i]*abs(nodes[i])**ks[0])  # free = heaviest at low order
    free = order[:p] if n > p else list(range(n))
    if n < p:  # add small extra clusters
        raise ValueError('too few nodes')
    def Fn(*x):
        pos = [mp.mpf(v) for v in nodes]
        for j, i in enumerate(free): pos[i] = x[j]
        return [sum(wts[i]*pos[i]**k for i in range(n)) - mp.mpf(r[k].numerator)/r[k].denominator for k in ks]
    x0 = [mp.mpf(nodes[i]) for i in free]
    sol = mp.findroot(Fn, x0, tol=mp.mpf(10)**-45, maxsteps=500)
    sol = [sol] if p == 1 else [sol[j] for j in range(p)]
    pos = [mp.mpf(v) for v in nodes]
    for j, i in enumerate(free): pos[i] = sol[j]
    return pos
def fake_sector(M, T, big, c=0.99):
    ks = list(range(4, M+1))
    r = {k: T[k] - sum(b**k for b in big) for k in ks}
    prop, res = propose(r, ks, c=c)
    if prop is None: return None, res
    nodes, wts = prop
    # need at least p nodes: split heaviest clusters if needed
    while len(nodes) < len(ks):
        i = max(range(len(nodes)), key=lambda i: wts[i])
        w = wts[i]; nodes.append(nodes[i]*0.97); wts.append(w//2); wts[i] = w - w//2
    pos = solve(r, ks, nodes, wts)
    return list(zip(pos, wts)), res
if __name__ == '__main__':
    M = int(sys.argv[1]); sector = sys.argv[2]; big = [F(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 and sys.argv[3] else []
    J, N = targets(M); T = J if sector == 'J' else N
    out, res = fake_sector(M, T, big)
    print(M, sector, 'res', res)
    if out: print([(mp.nstr(p, 8), w) for p, w in out])
