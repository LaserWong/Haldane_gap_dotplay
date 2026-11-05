from build import *
M = int(sys.argv[1]); sector = sys.argv[2]; big = [F(x) for x in sys.argv[3].split(',')] if sys.argv[3] else []
J, N = targets(M); T = J if sector == 'J' else N
for c in [0.9, 0.95, 0.97, 0.99, 0.8, 0.85, 0.75, 0.7, 0.6]:
    for ng in [801, 1201, 2001]:
        try:
            out, res = fake_sector(M, T, big, c=c) if ng == 1601 else None, None
        except Exception: pass
        try:
            ks = list(range(4, M+1)); r = {k: T[k] - sum(b**k for b in big) for k in ks}
            prop, res = propose(r, ks, c=c, ngrid=ng)
            if prop is None: continue
            nodes, wts = prop
            while len(nodes) < len(ks):
                i = max(range(len(nodes)), key=lambda i: wts[i]); w = wts[i]; nodes.append(nodes[i]*0.97); wts.append(w//2); wts[i] = w-w//2
            pos = solve(r, ks, nodes, wts)
            if all(abs(p) < c+0.02 for p in pos):
                print('OK', c, ng, [(mp.nstr(p, 8), w) for p, w in zip(pos, wts)]); sys.exit()
        except Exception as e: print('fail', c, ng, str(e)[:60])
