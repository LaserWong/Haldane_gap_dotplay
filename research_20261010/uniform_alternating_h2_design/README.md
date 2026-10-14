# Proposed H² refinement of the thermal weights

The accepted Stage21 inputs remain kappa32≤.136 and kappa64≤.157, with the four accepted intervals unchanged. This design performs no physical H² calculation at lengths 32 or 64 and establishes no wider interval.

Existing exact inputs improve the Rayleigh/trace lower bounds on the ground-state Gibbs weights to .9387875477507066 and .9176574240821238. Directed design arithmetic suggests simple bounds kappa32≤.131 and kappa64≤.151 after refining the finite-energy and gap estimates. Those bounds require a separate certificate and review.

A complete H² contraction could further improve fidelity. Even perfect fidelity would leave this method at approximately kappa32=.0753620 and kappa64=.0892450, because the excited-state B² contribution is controlled only by its norm. At the current radii, the idealized reduction in seed loss corresponds to a radius improvement of approximately 1.323–1.325 times. This is not a certified wider interval.

The proposal is a separately authorized physical-64 H² test with 40 CPU seconds and 256 MiB, followed conditionally by physical 32 with 20 CPU seconds and 256 MiB. Existing positive-convolution fixtures and local blocks suffice. A structured-wrapper compilation would have a separate limit of 30 CPU seconds and 512 MiB. This document does not authorize or launch those calculations.
