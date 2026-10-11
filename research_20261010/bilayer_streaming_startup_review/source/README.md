# Streaming startup successor: bounded producer test passed

This README and JOB_BINDING.json give the CURRENT successor identity. PROPOSAL.md retains the prior launch-contract history followed by an explicit streaming-generation amendment; its earlier job-directory and source-seal references are historical, not a second launch recipe.

Current source: bilayer_streaming_hash_revision. Current prepared directory: bilayer_full_m4_production_run_streaming. Proposed job845b55d815552ca70bb870f0efd6be20a94850f952e63a87dc7a0338553e8a0e. No successor authority, active CONTROL_SESSIONS ledger or worker store has been created. The metadata test creates only an empty OUTER_LOCK in the prepared directory.

Predecessor db32cbc51cf71726756f7910921ef26b684e6c3020a8e8f0a0e5eecd17d24556 is terminal FAILED_PREINNER; failure seal0dd76472806a818c4489fac4b093b7636468dc33771bbb0c8fa6ae3b9875aa32 preserves authority, failed pin-memory traceback and220 no-refund control charge. Those two records are carried verbatim as mandatory pinned successor inputs. Total21600 remains unchanged; control pool1200 remains unchanged. Existing220 +fresh220 +standard inner690 =1130, leaving70. No additional production retry authority is implied.

Root separately authorized a5-CPU-second metadata test. Actual outer.run, production_supervisor.launch and physical_session.run each reached their own actual startup verify_pins call, streamed all26 FINAL pinned files under actual AS64MiB, and deterministically raised a test-only stop immediately after successful verification. This exercised the30,894,944-byte Python binary in every startup context. In-memory fixture authority merely permits reaching that boundary; no authority file was written and os.fork was replaced with a hard test refusal in the child. The external parent enforced3 seconds child CPU plus2 own; child OS99/100 reproduces the actual outer startup profile, not the test CPU budget. Each startup recorded actual limits and VmPeak40,882,176 bytes.

All hash reads were65536 bytes (1605 calls across the three checks); a mutated Python pin was rejected. Child wait4 .339098 CPU; external self .125606755; wall .352797518; sampled childRSS13,762,560. Full5/5 remains charged. No physical workers were launched. This is a successful bounded metadata composition test, not a renewed production approval.

One engine.verify_pins helper uses file_sha256 with64KiB blocks. All outer/physical/supervisor pin maps call it. Remaining read_bytes calls are /proc cmdline, small normalized output JSON and synthetic benchmark evidence, not whole pinned files; runtime output hashing also uses streaming. Source/required-input bytes are fully pinned; numerical executable and algebra are unchanged.

Independent review and a specific successor launch decision remain required. The allowed staged cap chain stays100→400→2945. Only launch_watchdog.sh may launch after reviewed durable new reservations and authority.
