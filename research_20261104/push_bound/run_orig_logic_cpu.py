# Copy of runs/watertight/auditor/run_orig_logic.py plus ONE optional, count-asserted resource-only substitution (CPU_LIMIT env).
# Run the ORIGINAL (git HEAD a99fa21) audit_scalar.py / audit.py source with an explicit, minimal list of
# textual substitutions (input/output FILE NAMES, CPU affinity, and -- for audit.py -- the hard-coded gap literal).
# Every substitution must match exactly the stated number of times; no arithmetic/acceptance line is altered.
import sys, os
R = '/workspace/haldane_chat_bundle/runs/watertight/auditor/orig_audit/research_20261010'
mode, tag = sys.argv[1], sys.argv[2]          # mode: scalar|allsizes ; tag: baseline|w12_Z1
gap = sys.argv[3] if len(sys.argv) > 3 else None
def sub(src, a, b, n=1):
    c = src.count(a); assert c == n, (a, c); return src.replace(a, b)
if mode == 'scalar':
    path = R + '/uniform_smaller_second_initialization_review/audit_scalar.py'
    src = open(path).read()
    src = sub(src, "os.sched_setaffinity(0,{4})", "os.sched_setaffinity(0,{6})")
    if os.environ.get('CPU_LIMIT'):  # RESOURCE-ONLY substitution (push_bound): CPU-seconds cap 60 -> CPU_LIMIT; no arithmetic/acceptance change
        src = sub(src, "resource.setrlimit(resource.RLIMIT_CPU,(60,60))", "resource.setrlimit(resource.RLIMIT_CPU,(%d,%d))" % ((int(os.environ['CPU_LIMIT']),)*2))
    if os.environ.get('DIGITS'):   # rounding-grid precision only: down/up/power stay directed & self-checking for any B
        src = sub(src, "B=10**140", "B=10**" + str(int(os.environ['DIGITS'])))
    if tag != 'baseline':
        src = sub(src, "cert=js(A/'certificate.json')", f"cert=js(A/'certificate_{tag}.json')")
    src = sub(src, "(P/'scalar_results.json')", f"(P/'ORIG_scalar_results_{tag}.json')")
    src = sub(src, "(P/'SCALAR_INPUT_SHA256.json')", f"(P/'ORIG_scalar_inputs_{tag}.json')")
else:
    path = R + '/uniform_gap_0248_all_sizes_review/audit.py'
    src = open(path).read()
    src = sub(src, "os.sched_setaffinity(0,{7})", "os.sched_setaffinity(0,{6})")
    src = sub(src, "R/'uniform_smaller_second_initialization_review/scalar_results.json'",
              f"R/'uniform_smaller_second_initialization_review/ORIG_scalar_results_{tag}.json'")
    if tag != 'baseline':
        num, den = gap.split('/')
        src = sub(src, "cert=js(A/'certificate.json')", f"cert=js(A/'certificate_{tag}.json')")
        src = sub(src, "proposal=js(A/'cached_prefix.json')", f"proposal=js(A/'cached_prefix_{tag}.json')")
        src = sub(src, "gap=F(31,1250)", f"gap=F({num},{den})")
        src = sub(src, "'31/1250'", f"'{gap}'", 3)   # strongtail check, combined_claim, output label
    src = sub(src, "(P/'results.json')", f"(P/'ORIG_results_{tag}.json')")
    src = sub(src, "(P/'INPUT_SHA256.json')", f"(P/'ORIG_inputs_{tag}.json')")
code = compile(src, path, 'exec')
exec(code, {'__file__': path, '__name__': '__main__'})
