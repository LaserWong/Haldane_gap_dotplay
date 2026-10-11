# Bounds clarification after freeze

2026-10-11 01:18 UTC. This addendum supersedes ONLY the tighter amplitude bounds in README.md. No code, results, original manifest, or physical statements are changed. The narrower bounds there counted local actions but did not fully overcount all matching channels that can map into one output matching. Use the following deliberately coarse bounds instead.

Input coefficients have |c|≤2^48 by assertion. Source matching/orbit amplitudes are int32, and can also be bounded directly here: L≤4, M≤24. D4 has at most16 weighted hopping contributions plus6 occupied pairs×3 source matchings×2 output terms×max multiplicity2 =72, so R≤(16+72)×4=352. For D6, at most24 weighted hops plus15 pairs×15 source matchings×2 terms×2 multiplicity=900 give |D6 M|≤924×24=22176. C†R is at most15 pairs×3 source matchings×2 multiplicity×352=31680. These are safely int32 and cover the unchecked sparse-preserve additions in the inherited source routine.

Thus |T|≤14×(31680+22176)×2^48<2^68. Alternatively the generic int32 source bound gives B=|T|<2^84, and suffices for all subsequent guarantees.

For arbitrary scalar-channel magnitude B:
- D6T ≤(24+900)B <2^10 B.
- KT: empty-edge term≤192B; occupied-edge term≤15 pairs×15 source matchings×3 contraction×4 squared multiplicity=2700B; ordered wedges≤6 target sites×4 first neighbors×4 second neighbors×15 source matchings×3 contraction×4 edge-product multiplicity=17280B. Hence |KT|≤20172B<2^15 B.
- CT≤64 edges×15 source matchings×3 contraction×2 multiplicity B=5760B<2^13 B.
- U=1200T+11D6T has |U|<(1200+11×1024)B<2^14 B.

Starting with the conservative B<2^84, every scalar action is <2^99 and hence well inside signed int128. Code also checks new scalar additions/products. All norm/mixed products are converted separately to GMP before multiplication; no norm bound in int128 is used.
