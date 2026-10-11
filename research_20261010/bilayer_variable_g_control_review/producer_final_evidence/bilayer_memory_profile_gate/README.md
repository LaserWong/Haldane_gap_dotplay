# Bounded native memory profile: pass

Authorized8 CPU seconds, fully charged8/8. CPU6, no full support/cache. The accepted64-q6 target batch completed under128 MiB native address-space cap and reproduced all24 aggregate fields exactly. Native wait4 CPU .511223 seconds. Sampled maximum VmPeak/VmSize38,637,568 bytes; sampled native RSS20,398,080 bytes. Status sampling is not a final-exit VmPeak certificate; successful execution under the hard AS cap establishes this batch fits128 MiB.

Observer status VmPeak38,637,568 bytes explains why32 MiB was too brittle. Observer/outer soft AS64 MiB, native128 MiB, sum256 MiB while native active. Hard ceilings permit children to set their authorized larger soft limits. Overall sampled resident peak42,930,176 bytes including outer/observer/native, externally guarded256 MiB. Tree wait4 .627859 CPU, outer self .101444 CPU, wall .666316 seconds.

A planned MemoryError injection killed/reaped a known sleeping child using its fixed PID and wait4, without fresh /proc enumeration. The fault child's .000216 CPU is included in the three-second observer bundle (two own plus one fault reservation). This demonstrates the narrow fallback, not a complete repaired production supervisor.

Proposed next gate only: repeat the four-singleton/two-session integration under supervisor64/controller64/native128 MiB, with fixed-known-PID/group cleanup fallback. Keep an outer observer in the256 MiB resident total; its extra virtual space means virtual-cap sums and resident aggregate must be distinguished during integration. No retry or production authority is implied. Prior failed30-second integration remains fully charged.
