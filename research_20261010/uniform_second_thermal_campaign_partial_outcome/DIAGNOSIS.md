# Terminal partial thermal campaign: exact diagnosis and repair boundary

2026-10-11 00:04 UTC. NO RESTART. Sole authorized ledger remains immutable at uniform_second_thermal_campaign_run/ledger.json. Terminal BUDGET_RESERVATION_EXHAUSTED; charged16207 of21600CPU seconds,5393 remaining. Original wallstop06:00UTC unchanged. Both unknown-attempt reservations7320 each are retained in full; no refund/reset/alternate ledger is proposed.

## Completed evidence

Sixteen complete producer cases, all lengths4..11, both I/P seams, independently aggregated W matches published integers.990 complete batch files preserved. The independent reviewer had already checked completed-case identities, physical matrix/orbit coverage and interval reconstruction. No L12 full thermal certificate exists. Therefore the full18-premise n36 scalar result remains conditional.

L12I has256 of11595 representative columns complete (16 of733 batches);11339 representatives/717 batches remain. L12P has192 complete (12 batches);11403 representatives/721 batches remain. Representative multiplicities/whole Hilbert coverage are distinct from the number of computed columns; partial sums cannot stand in for full traces. Completed certificates are copied read-only here; CAMPAIGN_STATE_SHA256.json pins the entire terminal state, including all990 batch files, ledger and logs.

## Failure mechanism

The frozen supervisor invokes frozen campaign.py with --cpu-budget120 and --max-new-batches32. campaign.py computes used CPU for its current compute phase and remaining=int(120-used)-1, then sets the NEXT child hard cap=min(120,remaining). It starts the child whenever remaining>=1, without requiring enough allowance for an entire batch. Thus this was a scheduling-boundary failure, not a thermal arithmetic disagreement.

L12I saved116.495635 childCPU seconds in16 successful batches, whose durations were6.806..8.978seconds. Before the next batch, parent overhead makes remaining<=2seconds. L12P saved114.881077seconds in12 batches, durations7.973..11.627seconds; next allowance<=4seconds. Each next child returned-9, exactly compatible with exhausting this artificially shortened CPU limit. The runner asserted and the watchdog killed its group. The supervisor conservatively retained each full7320 reservation as UNKNOWN_CHARGED. Committed earlier costs+these reservations gave16207, so no new7320 reservation fitted5393. It stopped normally and did not restart.

The prior fault tests exercised failed children and accounting, but missed this ordinary multi-batch boundary. Any repair must add a scaled nonthermal sequence test where several legal-duration batches approach a short invocation allowance. Correct behavior is successful checkpoint-preserving yield BEFORE launching an underfunded batch, not killing it and charging an unknown whole invocation.

## Measured remaining cost, not a guarantee

Current recorded mean full childCPU/batch is7.28098sec(I),9.57342sec(P). Accounting for actual sparse-entry counts across all magnetizations rather than multiplying by worst-block time gives remaining kernel estimates3175sec(I),4288sec(P). Per-batch setup estimates add548sec and609sec, respectively. Total remaining estimate8621CPU seconds, plus repeated case metadata revalidation and supervisory fees. Kernel wall-time was used as a single-core CPU proxy, so this is planning evidence, not a rigorous runtime bound. A conservative planning range is approximately2.4–3CPU hours for both final cases.5393 remaining ledger seconds are only1.50hours, before reservation headroom. Existing-kernel full completion is therefore NOT expected under the unchanged remaining budget. A scheduler repair alone cannot be advertised as finishing both.

## Smallest prospective repair (not implemented or authorized)

A new independently reviewed continuation supervisor could append explicit root-approved continuation bindings/event to the SAME ledger, retaining every old attempt and16207 charges. It must not silently edit the frozen terminal state or replace prior bindings. Root must authorize this state transition; this report grants no permission.

The frozen arithmetic runner/kernel and their checkpoint identities can remain untouched. One safe bounded invocation design is max_new_batches8 with a large internal allowance1000, plus a supervisor hook enforcing a fixed40CPU-second cap on each metadata/compute child, while retaining120 caps on runner/watchdog. At most8 compute children can spend320CPU seconds; runner CPU<=120, so the runner's internal remaining allowance stays above120 throughout. It stops after eight complete checkpoints without ever shortening a child's cap at the invocation boundary. This avoids the discovered path by a deterministic bound, not a timing guess. Any genuinely >40-second child still fails safely and incurs conservative charge.

For n12, conservative reservation becomes26 metadata children plus8 compute children, each42 seconds including slack, plus122 for runner and122 for watchdog:1672 seconds. Two such reservations3344 fit5393 (after a new122-second supervisor overhead charge). Successful terminal wait4 refunds remain exactly as reviewed; unknown attempts retain full charge. This is smaller than the old7320 reservation. Limits may be shortened further only with new measured fixtures and independent review. Another approach is a genuinely revised runner that yields whenever remaining<fixed_child_cap+bookkeeping reserve. Either requires the new scaled boundary regression and no thermal launch during gate review.

Because the existing frozen runner/source/binary/coefficients remain unchanged in the bounded-invocation design, old exact checkpoint identities need no arithmetic migration. A changed lifetime/CPU hook is a new supervisory binding and must be explicitly reviewed. The mathematical remaining-cost obstacle still stands: this design permits safe partial progress, not expected completion of both L12 cases within5393. Root can choose to leave the partial campaign stopped rather than spend scarce allowance without completing the thermal premise.
