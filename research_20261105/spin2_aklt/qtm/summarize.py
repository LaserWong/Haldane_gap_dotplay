import json,sys
seen=set()
for l in open('qtm_results.jsonl'):
    d=json.loads(l); r=d['ratios']; k=len(r)
    c=[(i,x) for i,x in enumerate(r) if abs(x[1])>1e-8]
    # distinct complex moduli
    groups={}
    for i,x in c:
        key=(round(x[0],4),round(abs(x[1]),4)); groups.setdefault(key,[]).append(i)
    g=sorted(groups.items(),key=lambda t:-(t[0][0]**2+t[0][1]**2))
    lastmod=(r[-1][0]**2+r[-1][1]**2)**.5
    print(f"{d['model']:8s} N={d['N']} b={d['beta']:<3g} k={k:2d} relres={d['max_resid']/abs(d['lam0'][0]):.0e} |r_k|min={lastmod:.3f} real2nd={r[1][0]:+.4f} complex:",
          '; '.join(f"{a:+.4f}±{b:.4f}i(|{(a*a+b*b)**.5:.3f}|,x{len(v)},rank{v[0]})" for (a,b),v in g[:3]) or 'none')
