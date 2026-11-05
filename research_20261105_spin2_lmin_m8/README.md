# Spin-2 M=8 interval-data moment no-go

Updated 2026-11-05 16:43 EST (America/New_York, UTC−5) / 2026-11-05 21:43 UTC.

The theorem document is [CERT_M8.md](CERT_M8.md). Its label is PROVED, computer-assisted, on the trusted base named in that note. The result is contract B-cert-M8. One finite rational integer-weight member of class `F1--F4` lies strictly inside the ten rigorous two-sided boxes for `Z_k` and `P_k` at every integer `k` from 4 through 8. The same witness satisfies `S(256) < 1/sqrt(2)` and `S(300) < 1/sqrt(2)`. The approximate displays are 0.5082725203986761 and 0.5113138102625230. Acceptance is the exact check recorded in `check_cert_result.json`, where `accepted` is true.

This is an interval-data no-go for that fixed length-8 box dataset inside the structural class `F1--F4`. It does not claim `M_min>=26`. It does not claim that the physical spin-2 seeds fail. Sharing a box does not identify the unknown exact moments. The through-M=25 target remains BLOCKED, as `CERT_M8.md` states.

[DISCRIMINATOR.md](DISCRIMINATOR.md) and [PLAN.md](PLAN.md) keep the earlier estimated-data experiment. That experiment is labeled TESTED. It is not the theorem.

The remaining files are the extracted archive. This README is the only file added after extraction. The excluded spectral cache is absent. There is no `*.pkl` file and no `cert/cache` directory. Bytecode caches are absent. No existing repository file is changed. The deposit contains 496 enclosure JSON files under `cert/enc/`.

On 2026-11-05 the 509 SHA-256 digests in [CERT_M8_manifest.json](CERT_M8_manifest.json) were recomputed against the deposited files, and every digest matched. The two hashes named in `CERT_M8.md` also matched.

- `candidate_cert.json` is `886dbe6def9a20002db81644417f17b2246180995e5fffab0ffea597494db363`.
- `cert/enclosures.json` is `74d9d50f1d5996bf48e763e69ccd38e6bf28b0af9f80b185714903611d8135ce`.

The 18 digests under `files` in [manifest.json](manifest.json) likewise matched. Those bind the TESTED estimated-data packet.

Every Python source in this folder was parsed with `python3 -m py_compile` on 2026-11-05. All 13 files compiled. The interval certificates and the exact checker were not rerun for this deposit.

## Files outside the certificate manifest

The enclosure JSON files and the core certificate scripts are hashed inside `CERT_M8_manifest.json`. The table records SHA-256 for the remaining deposited files, including that manifest.

| File | SHA-256 |
| --- | --- |
| `CERT_M8_manifest.json` | `01c05ee1b51dbb6af48ee01687284a0991c52febb8a018a1844f6786077c371e` |
| `DISCRIMINATOR.md` | `a6f8522a3b89db67d2b3213883b7a8f616dbb44ec32730e4c89434c36ec3073c` |
| `candidate.json` | `79ef23bac92fb7c3954d2be889343234c3969f4c6efcc57e647f911f55ecbd3e` |
| `candidate_grid095.json` | `44210ae98c9b940fc26f6f7adc0c162bd0583d42e60fba4f3c26cf16c5135c2a` |
| `cert/assemble_L7.log` | `7c51b95b66dc1d81270adf183f4c11811a0ae0ca930fa7d7211f8a3ad2084a8d` |
| `cert/assemble_L8.log` | `43997285f574fedbfb12813f18d6a27956f445767d9a49104ad7b24cf492f41a` |
| `cert/audit_dH.log` | `a05be74b4860ce1cecd2a1aa0f96181f92e0bd779470fac5df45b97f186773c2` |
| `cert/cert_spin1_orig.py` | `a5573b2a7f0b5ef99f07c19cf5955383f8496bfadffcd96171c133e2aaf1844c` |
| `cert/run_L4.log` | `2ae7e33a0c31fa3a5943726e4ca782ddf0b50fe84c173faae91cbdcd95da5b06` |
| `cert/run_L5.log` | `b3595c28cad91a9efd6bfaf931b4609d08b113217efc6aabd8f88f06334efefa` |
| `cert/run_L6.log` | `5ab086d40e3a7df670956ea7cc392880391fd1f795057fb396edd1431a955dc2` |
| `cert/run_L7.log` | `46cb8b5235ddd28ddcdcfc4eac982e0917784071713f7102fe118cfe41eb8850` |
| `cert/run_L8.log` | `da5faf5af65e87c6b341454df3943d33eff10a2950c1a58e854e5a21018a7cda` |
| `cert/run_L8_highsz.log` | `810d20aa492b51455c23312c007af7b12994eb9723286a98d13e70ef68779281` |
| `cert/run_L8_midsz.log` | `bac9656c47765c97cb3bc3c784d40acc8e4cfbabd82436f0da1427d18d802e7b` |
| `cert/run_L8_sz4.log` | `431a2844ff55d0c864dfba717deebcf988f2cd6ccaa1491921c554941620fa9a` |
| `cert/run_L8_sz56.log` | `dd85faaf348b48ea11848c42457631890c33061d61773c054c660a104197e914` |
| `check_candidate.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `check_candidate.py` | `43af0cab092a86b0b2ddd637b1873adf65ec0753e40eea28fa51b041b88993d7` |
| `check_cert.log` | `42a57a06a87716da00e3be28c5705010b32fe9ac733554200bc0bc3bfca194e6` |
| `check_cert_replay.log` | `42a57a06a87716da00e3be28c5705010b32fe9ac733554200bc0bc3bfca194e6` |
| `check_integer.log` | `0a29bf2570572b8faec8732d73345513b87e97bf8cdbaae8bf515126ccdefc07` |
| `check_integer.py` | `d9f18e9d1947ce5c05b4d3952802da550524ee9cc9aeca538803ff27dbc8b44f` |
| `check_integer_result.json` | `c867c5290bb67e94a10c82948114906ab1a6a889a791a0d063b932c73b705fe2` |
| `ed_estimates.json` | `fe78476a625a1c3d19c401f61c76d0d1f9ecdec9fac5613db74af8399bb77c00` |
| `ed_estimates_symmetric_start.json` | `b954c9b31d6cc90b221aea9736526846907a199e467387bf6c1c7d1011a352b9` |
| `ed_helpers.py` | `4516a38ec7a817d77df699a8c7160490ea11c07528bd9b32c2e9ee66470501b8` |
| `estimate_data.log` | `6e7c6675d43e2e15475e810b7a389a9645da3fc6bc740a8b2758dab05b055928` |
| `estimate_data.py` | `5b21509f1c2531f1cad9d1f5ffbd168c18f7bd62b3030f9c29ac0cd696b26c57` |
| `estimate_data_symmetric_start.log` | `f44e0c83fd4af02fdc548cfaecc0871bab3a71b907defa5f7b4274b73c626246` |
| `finish_m8.out` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `finish_m8.sh` | `bcec9d96edd8809f0b0c9db2b1bc7199e52ac87509180612b759d0e399e037aa` |
| `finish_m8.status` | `1d776a24b744a50776ad3e394d7c6e6d326d0c286cfc2fbcbcbf4571508530f4` |
| `fit_cert.log` | `e783295848ea2a365225974248e3141ef417cdd857a09034fc8ca4b961935603` |
| `fit_fake.log` | `03368abe55ef83d446562e82152a988cba146f302ad3a428e906a0d379dbc065` |
| `fit_fake.py` | `fbd7da9548f19d7550a4159fb21d4631a217e754798510276816c0e09c9913f4` |
| `fit_fake_grid095.log` | `9e99960284e199b89553402c9237f7e0371ea813cbf7ba052804f19f8c0501e8` |
| `manifest.json` | `d913c8e2a825b8b86521d2ecfef5a0b6ae2ee900a6dee2a1261d84afb6e3e7bb` |
| `strict_seed_replay.log` | `962a44dfb8e9a2452b6f33d38a3b5dd0225394e8019d5de0ce849ba8b50ed2b0` |
