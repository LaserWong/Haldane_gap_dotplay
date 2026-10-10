# Stage7 provenance and source contract

This is a newly created static extraction. All earlier files remain unchanged. The inherited stage6 manifest and every selected source manifest were verified before extraction and again during replay. Manifest entry totals include overlaps.

| Selected manifest | SHA-256 | Entries checked |
|---|---|---:|
| [research_20261010/overview/SHA256SUMS.json](../overview/SHA256SUMS.json) | 9443c64414f4e67c20d75f4a851e7fc3ec4c56c094b4b061df20bb68d741a12e | 19 |
| [research_20261010/reduced_input_review/MANIFEST_SHA256.json](../reduced_input_review/MANIFEST_SHA256.json) | e5970d2303f65be0b69354417012aaf4925bf2920664d4890fb1e1e6cf2ff7d4 | 63 |
| [research_20261010/bilayer_frontier_review/MANIFEST_SHA256.json](../bilayer_frontier_review/MANIFEST_SHA256.json) | 86deb5c51305376cd81e27fd0af06ce50c28cd27a28b3817a4b7e5b1dc87fc32 | 99 |
| [research_20261010/ordinary_interval_review/MANIFEST_SHA256.json](../ordinary_interval_review/MANIFEST_SHA256.json) | 69b25feba15d9b338c5b06fe546f2c17a331c4630ccf628f8f3f105741d0e667 | 52 |
| [research_20261010/ground_moment_review/MANIFEST_SHA256.json](../ground_moment_review/MANIFEST_SHA256.json) | e981ee1b4157ce0822c464f06883638ea16e3677ca58e4f1991152595ee5d14c | 207 |
| [research_20261010/variational_filter_review/MANIFEST_SHA256.json](../variational_filter_review/MANIFEST_SHA256.json) | 7930d8e7bc07ff6a48372de60de5ce426b42ebcc0844cbcbe38049070a2025b5 | 106 |
| [research_20261010/chain_temperature_review/SHA256SUMS.json](../chain_temperature_review/SHA256SUMS.json) | 67e409eb7113f7e93f07e629f51624ee848fdcf79485b271910058ce5cc43614 | 28 |
| [research_20261010/combined_ground_review/MANIFEST_SHA256.json](../combined_ground_review/MANIFEST_SHA256.json) | 03fd3929b1305971be593c1efa9a3374ff66675bc4543c25f95ff7863846f70a | 329 |
| [research_20261010/interval_extension_review/MANIFEST_SHA256.json](../interval_extension_review/MANIFEST_SHA256.json) | 1af6c2142aa6a3649fd50275a8582add9cfe0a72ff8f21556195185c495eb956 | 123 |
| [research_20261010/overview_stage6/MANIFEST_SHA256.json](../overview_stage6/MANIFEST_SHA256.json) | c12c9c3ac923672a0831858c4e14fb0b80b7c02f700898bd2dfaf482b4bb822f | 37 |
| [research_20261010/joint_ratio_review/LEMMA_REVIEW_MANIFEST.json](../joint_ratio_review/LEMMA_REVIEW_MANIFEST.json) | 18fd9df56ad4023b2f174a3a54d122550670dcf0863176270cd000d48c00fe91 | 13 |
| [research_20261010/joint_ratio_review/CHAIN_REVIEW_MANIFEST.json](../joint_ratio_review/CHAIN_REVIEW_MANIFEST.json) | 0af04a6c84baa0a87c777a5f9e99aad6d5c903821d5ec3e1b21d71ace84684f4 | 57 |
| [research_20261010/chain_low_band_review/MANIFEST_SHA256.json](../chain_low_band_review/MANIFEST_SHA256.json) | 789e7214b7f9382c91a74c23efb6b063547d66d9bf8fe41710fa82aa6c4a7bd3 | 50 |
| [research_20261010/bilayer_polynomial_frontier_review/MANIFEST_SHA256.json](../bilayer_polynomial_frontier_review/MANIFEST_SHA256.json) | 9cb0484af6d424e74e5520d8d995c88d63ab2c6396938634b98acf3927684930 | 163 |
| [research_20261010/interval_joint_review/MANIFEST_SHA256.json](../interval_joint_review/MANIFEST_SHA256.json) | cc57b7779f77d91164ec68d612979817846a1ec91a66ab45c86b243becdabc8d | 37 |
| [research_20261010/interval_range_0085_review/MANIFEST_SHA256.json](../interval_range_0085_review/MANIFEST_SHA256.json) | c14cdb65f0e1b92a6025758e63352e404eef01965f7dde2344a2eaaf86c5a0b9 | 81 |
| [research_20261010/nonperturbative_mps_review/MANIFEST_SHA256.json](../nonperturbative_mps_review/MANIFEST_SHA256.json) | ada056e604879bd0f619baccbbb3dd9925e6d61d61429c2af3345b1dfb20bc3f | 22 |

## Extraction boundaries

- Thermal claims preserve primary JSON numeric pointers and exact fractions. The AKLT theorem is a separately typed reference, whose exact rational gap and size range are read from the accepted claim conditions and supported by the full independent proof.
- The 54 joint-chain paths use min(path M≥8 bound, accepted M=2…7 minimum). The 153 counted-chain paths read their accepted all-M≥2 bound directly. Every derivation is replayed.
- New continuous claims consist of two joint-aware pieces and sixteen range-extension pieces, joining all 31 stage6 pieces. Duplicate whole-union and regime summaries are not counted as additional pieces.
- Only the newest [0,.085] ordinary-bilayer union is drawn in the main figure; earlier accepted union rows remain in the data. All isolated points select the largest exact accepted value at that parameter.
- The final [.082,.085] denominator trial dimensions 59/125 are distinct from retained trace counts 49/97 and the largest filtered numerator bound ≤30.
- The g=.09 third-moment 43D proposal is intentionally excluded. Existing physical .09 input acceptance and failed grids do not authorize a .09 gap marker.
- The reported project main commit is 00593ba445c26b1da625c9afe618e85a2550f70e; no local Git identity is asserted.

All CSVs use exact fraction strings and retain provenance fields. Source paths are project-root-relative. The four historical comparison CSVs are byte-identical to stage6.
