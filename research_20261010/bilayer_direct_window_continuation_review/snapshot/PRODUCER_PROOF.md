# Saved-input direct-window continuation for all 66 ordinary bilayer intervals

2026-10-10 22:28 UTC / 18:28 America/New_York. Producer candidate pending independent review. No new coupling or physical input is certified here.

Using the new direct time-first 2D finite-window lemma in ../bilayer_direct_window_extension/PROOF.md and its independently reviewed physical premises, the exact scalar continuation gives

 gap >= 4499695659/10^12 = .004499695659

uniformly for every real 0<=g<=1/10 and every periodic integer square side L>=2, with a unique finite-volume ground state. This is conditional on independent review of this continuation. The previously accepted uniform gap is .001945771244. The coupling interval is unchanged.

## Inputs and coverage

Reuse, without optimizing or changing any physical trial vector, the 66 accepted closed interval records:

- ordinary_interval:16 covering[0,.07]
- interval_extension:15 covering[.07,.078]
- interval_joint_extension:2 covering[.078,.08]
- interval_range_0085:16 covering[.08,.085]
- interval_range_009:7 covering[.085,.09]
- interval_range_010:10 covering[.09,.10]

Every complete record is hash pinned in interval_results.json and DEPENDENCIES.json. Existing trial means, complete residuals, parameter-dependent sector cutoffs, low-band endpoints, multiplicities, omitted-spectrum tails and trace-ratio bounds are inherited. This task does not regenerate them. All retained state counts, search dimensions and physical Hilbert dimensions therefore remain those of each source interval.

For each interval, take its saved initial txy edge lower bounds at the common square base n8 and physical beta twice beta_initial. Recheck their validity from the saved exact J1,J2,C0 lower endpoints using a<=G(J1), b<=G(J2*a), c<=G(C0^4*a^2*b). Because these saved trace endpoints apply uniformly throughout the closed coupling interval, all monotone scalar bounds here also hold uniformly.

Continue raw time-first and canonical ladders using the already accepted recurrence/transport/joint-product comparison, retaining at least120 decimal places by downward rounding. At each common state use the maximum of the new direct-window purity and the previously accepted canonical-window purity. Record whichever method is selected. Any certified canonical state with 0<u<=1/500 supplies a terminal all-integer asymptotic bound by exp(beta*gap)*32u<1. Only finite windows strictly before that chosen terminal are included in the final minimum. The optimum among these finitely many exactly verified terminal candidates is retained.

Each interval also retains and takes the minimum with its own six accepted short-size L2,...,7 gap bounds. Every selected path explicitly stores the square physical base, both ladder edge basepoints/endpoints, 517 total finite windows, terminal defect and exact exponential witness. The largest selected path has12 states. First coverage starts at L8, each finite window ends at the next one's start, and terminal asymptotic coverage starts at the final endpoint. Closed parameter intervals are checked to meet exactly, beginning0 and ending1/10.

The limiting interval is [169/2000,339/4000]=[.0845,.08475], from interval_range_0085/lowband/interval_007.json. Its selected asymptotic onset is L16384 at physical beta35840. No interval is weakened relative to its prior accepted lower bound.

## Arithmetic and resources

The imported direct-window replay uses integer-square root enclosures at120 decimal digits. All recurrence outputs are rational lower bounds, and every finite-window and terminal gap is accepted only by exact rational exponential upper-bound inequalities. Floating logarithms propose decimal rational gap values; they do not certify them. Each source interval is processed sequentially and checkpoint.json is updated after each one.

The full66-record pass took6.53 seconds and99,720KiB peak RSS. CPU3, one numerical-library thread,600CPU-second and700MiB address-space caps are enforced by the imported setup. No large contraction, eigensolver, full ED, network operation or remote write is performed. Reproduction writes interval_results_check.json and compares all non-timing certificate data with the frozen result.
