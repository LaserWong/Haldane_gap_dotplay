## (b) Headline dual-check (from existing indep_chain + a_uniform)
indep_chain (exact Fraction, separate from repo audit_scalar):
  ckrun_FULL_W17.log: gap 63033/2500000 ACCEPTED ('asym from L=2228224 beta=802816 windows=17 u>0:True', 0.9576926444664424) cpu 5.7s
  ckrun_W17_d20000_and_reject.log: gap 63033/2500000 ACCEPTED ('asym from L=2228224 beta=802816 windows=17 u>0:True', 0.9576926444664424) cpu 17.8s
  ckrun_W17_d20000_and_reject.log: gap 250057/10000000 ACCEPTED ('asym from L=2228224 beta=802816 windows=17 u>0:True', 0.9795593942795794) cpu 17.2s
  ckrun_W17_d20000_and_reject.log: gap 31517/1250000 REJECTED ('asym from L=2228224 beta=802816 windows=17 u>0:True', 1.320351537065016) cpu 5.6s
  ckrun_Z1_W17.log: gap 250057/10000000 ACCEPTED ('asym from L=2228224 beta=802816 windows=17 u>0:True', 0.9795593942795794) cpu 5.6s
  run_FULL_W15.log: gap 126049/5000000 ACCEPTED asym from L=557056 beta=200704 u=0 windows=15 factor 0.9940352135770729 cpu 62.6s
  run_FULL_W16.log: gap 252121/10000000 ACCEPTED asym from L=1114112 beta=401408 u=0 windows=16 factor 0.9949949417423365 cpu 278.8s
  run_Z1_W15.log: gap 250023/10000000 ACCEPTED asym from L=557056 beta=200704 u=0 windows=15 factor 0.9996614047192522 cpu 62.6s
  run_Z1_W16.log: gap 50009/2000000 ACCEPTED asym from L=1114112 beta=401408 u=0 windows=16 factor 0.9666967445497292 cpu 279.5s
a_uniform/cert12.py (independent W=12 exact re-derivation):
  Z>1 W 12 2497/100000 True asym from L=69632 beta=25088 u=1.71653e-273 windows=12 0.9914067933026973
  full W 12 25177/1000000 True asym from L=69632 beta=25088 u=9.4083e-276 windows=12 0.9783577870077593

Recommendation: headline 63033/2500000 = 0.0252132 is now dual-checked by
  (1) patched repo FULL checker (push_bound/certs/full_W17)
  (2) indep_chain.py FULL W=17 DIGITS=20000
Conservative dual-checked floor also: 25177/1000000 via cert12 + repo at W=12.
Do NOT extend cert12 to W=15-17 (not cheap under 600s); indep_chain already covers W=17.
