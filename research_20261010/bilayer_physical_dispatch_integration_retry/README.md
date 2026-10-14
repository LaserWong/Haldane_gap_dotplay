# Physical dispatcher integration test

The new authorized 30-second integration test passed and remains fully charged at 30/30. The original failed 30-second gate and the 8-second profile gate remain immutable. Pinned control source revision 427344a2dd4593ed37ba559c41e9c0b1797dd21962235f6c6d1a6bd1a57ff8be was frozen before execution.

Two reference batches reproduce every one of 24 accepted aggregate fields for 64 q6 targets and 16 q4 targets. The four singleton q0/q2/q4/q6 targets then pass the actual physical worker, digest/output verifier, dispatcher loop, incremental reservation/adoption and canonical committed receipt path. Two controller lifetimes commit two chunks each, preserving the first two on restart. All four committed rows occur exactly once in final partial assembly.

The fixture adapter changes only the four-row plan, explicitly non-production job kind, hard singleton allowlist and finalizer interception. The test invokes the full finalizer, which must reject incomplete coverage before reading the accepted m0/m1/m2 controls. Partial normalization is tested through the actual pencil consumer with 3x integer accumulators, dividing exported exact matrices by 3, against separately assembled rational sector weights 1,1,8,16/3 and moment identities. These partial diagnostics are not full moments. Test authority/control files are fixture-only, not production authority.

Memory profile 64 MiB supervisor /64 MiB controller /128 MiB native succeeds. Their virtual-memory soft caps sum to 256 MiB. The additional outer observer is included in the independently sampled 256 MiB resident-memory aggregate. The four processes therefore do not have a combined virtual-memory cap of 256 MiB. Observed whole-tree RSS 55,095,296 bytes.

Actual outer wait4 tree CPU 1.131952 seconds, outer self .131393, wall 1.226291. Phase 0 tree .935442 and phase 1 .196510 include supervisor/controller/worker CPU. Within those, controller self times .137225359 and .067796936. Supervisor self .094384 and .060784. These nested measurements overlap and must not be added again. All 30 seconds stay charged.

No unexpected failure or retry occurred in this new gate. Both sessions verified inherited lock and reaped their children. Production remains blocked until independent control review and explicit production authority. Full accepted 57D m0/m1/m2 control input and final complete-coverage check remain mandatory.
