# Stage6 accepted review provenance

Snapshot 2026-10-10T19:18:08.857188+00:00.

Each listed manifest was checked entry by entry before inclusion. `overview_data.json` records the exact SHA-256 of every directly referenced source. This verifies integrity and association with sealed reviews, not a new independent proof audit.

| Review directory | Manifest SHA-256 | Verified files |
|---|---|---:|
| [overview](../overview/README.md) | `9443c64414f4e67c20d75f4a851e7fc3ec4c56c094b4b061df20bb68d741a12e` | 19 |
| [reduced_input_review](../reduced_input_review/README.md) | `e5970d2303f65be0b69354417012aaf4925bf2920664d4890fb1e1e6cf2ff7d4` | 63 |
| [bilayer_frontier_review](../bilayer_frontier_review/README.md) | `86deb5c51305376cd81e27fd0af06ce50c28cd27a28b3817a4b7e5b1dc87fc32` | 99 |
| [ordinary_interval_review](../ordinary_interval_review/README.md) | `69b25feba15d9b338c5b06fe546f2c17a331c4630ccf628f8f3f105741d0e667` | 52 |
| [ground_moment_review](../ground_moment_review/README.md) | `e981ee1b4157ce0822c464f06883638ea16e3677ca58e4f1991152595ee5d14c` | 207 |
| [variational_filter_review](../variational_filter_review/README.md) | `7930d8e7bc07ff6a48372de60de5ce426b42ebcc0844cbcbe38049070a2025b5` | 106 |
| [chain_temperature_review](../chain_temperature_review/README.md) | `67e409eb7113f7e93f07e629f51624ee848fdcf79485b271910058ce5cc43614` | 28 |
| [combined_ground_review](../combined_ground_review/README.md) | `03fd3929b1305971be593c1efa9a3374ff66675bc4543c25f95ff7863846f70a` | 329 |
| [interval_extension_review](../interval_extension_review/README.md) | `1af6c2142aa6a3649fd50275a8582add9cfe0a72ff8f21556195185c495eb956` | 123 |

Previous sealed overview data SHA-256: `23e8f2e3731c1e3acedc5e13814fc169b3282dc545e848e60461f4dc88eb60aa`.

All prior overview artifacts were left unchanged. The stage6 manifest excludes itself and Python bytecode caches to avoid circular checksums and machine-local cache state.
