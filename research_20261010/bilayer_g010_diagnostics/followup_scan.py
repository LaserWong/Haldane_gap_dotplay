exec(open(__file__.replace('followup_scan.py','diagnose.py')).read().split("cases={'baseline':base}")[0])
# Conditional reductions split the two denominator ground widths to identify
# which patch matters. Uppers are fixed trial values, not physical eigenvalues.
cases={}
for i,s in enumerate(shapes[:2]):
 for fraction in [.1,.25,.5,.75,1.0]:
  r=copy.deepcopy(base);lo=F(r[i]['blocks'][0]['eigen_lower'][0]);up=F(r[i]['blocks'][0]['eigen_upper'][0]);r[i]['blocks'][0]['eigen_lower']=[str(lo+F(str(fraction))*(up-lo))];cases[f'ground_{s}_width_reduced_{fraction}']=r
r=copy.deepcopy(base)
for i,s in enumerate(shapes[:2]):r[i]['blocks'][0]['eigen_lower']=json.loads((HERE/f'patch_{s}_g1d10.json').read_text())['blocks'][0]['eigen_lower']
cases['rigorous_weighted_ground_candidate']=r
out={name:scan(r) for name,r in cases.items()}
for name,r in out.items():print(name,r['successes'],r['best'],r['best_partial']['beta'],r['best_partial']['min_defect'],flush=True)
(HERE/'followup_diagnostics.json').write_text(json.dumps(out,indent=2)+'\n')
