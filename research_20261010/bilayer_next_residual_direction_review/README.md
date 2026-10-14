# Symbolic residual directions and moment requirements

The review checks the symbolic residual-direction calculation and its moment requirements using pinned inputs in `snapshot`. It includes the producer's cost erratum. The result uses cached and symbolic calculations, with no new physical-support contraction or gap bound.

`PROOF.md` and `ACCEPTANCE.json` describe the scope. Run `sh REPRODUCE.sh` for a fresh exact replay. The observed cost was less than 1 CPU second and less than 20 MiB.
