import json, math
P = json.load(open('T1_proxy.json')); Tl = json.load(open('T1_tolerance.json'))
S6, S8 = json.load(open('results/spectrum_L6.json')), json.load(open('results/spectrum_L8.json'))
rows = []
for L in (6, 8):
    for chi in (8, 16, 32, 64, 128, 256, 512, 1024, 0):
        for mode in ('ladder', 'tebd'):
            try: r = json.load(open(f'results/{mode}_L{L}_chi{chi}.json'))['rows']
            except FileNotFoundError: continue
            if len(r) < 7: continue
            x5, x6 = r[5], r[6]; zex = lambda x: float(x['Z_exact'].split()[0].strip('['))
            d = dict(mode=mode, L=L, chi=chi or 'inf', eta0_rel=r[0]['eta_true'] / r[0]['normY'],
                     eta_beta=x5['eta_true'], Zex_beta=zex(x5), Zlo_beta=x5['Z_lo_true'], Zhi_beta=x5['Z_hi_true'],
                     eta_2beta=x6['eta_true'], Zex_2beta=zex(x6), Zlo_2beta=x6['Z_lo_true'], Zhi_2beta=x6['Z_hi_true'],
                     apriori_exact_rel_2beta=x6.get('delta_exact', math.nan) / x6['normY'],
                     apriori_anders_rel_2beta=x6.get('delta_anders', math.nan) / x6['normY'])
            n = L // 2
            for v in ('true', 'exact', 'anders', 'bond', 'fro'):
                k = f'{mode}|n{n}|chi{chi or "inf"}|{v}'
                if k in P: d[f'slack_{v}'] = P[k]['slack']
            rows.append(d)
spec = {L: {k: S[k][str(L // 2)]['need'] for k in S} for L, S in ((6, S6), (8, S8))}
json.dump(dict(rows=rows, middle_cut_chi_needed=spec, tolerance=Tl,
               labels=dict(eta_true='PROVED (arb + IEEE standard model)', Z_exact='PROVED (arb)', slack='PROXY (FEASIBILITY spent log-slack)',
                           apriori_anders='FLOAT (Anderson cluster E0 by float ED)', apriori_exact='ORACLE/FLOAT', tolerance_L256='ESTIMATE')),
          open('T1_results.json', 'w'), indent=1, default=str)
f = lambda x: 'n/a' if x is None or (isinstance(x, float) and math.isnan(x)) else (f'{x:.3g}' if isinstance(x, float) else str(x))
print('| mode | L | chi | eta0/|E0| | Z_lo(β) | Z_hi(β) | Z_ex(β) | Z_lo(2β) | Z_hi(2β) | Z_ex(2β) | slack true | slack exact-E0 | slack Anderson | slack bond | slack fro |')
print('|' + '---|' * 15)
for d in rows:
    print('|', ' | '.join(f(d.get(k)) for k in ('mode', 'L', 'chi', 'eta0_rel', 'Zlo_beta', 'Zhi_beta', 'Zex_beta', 'Zlo_2beta', 'Zhi_2beta', 'Zex_2beta',
                                                   'slack_true', 'slack_exact', 'slack_anders', 'slack_bond', 'slack_fro')), '|')
