# Scope of the original transfer theorem

Recorded October 10, 2026, at 18:39 EDT / 22:39 UTC.
The source-level review passed.

The original final theorem covers even periodic lengths, but its transfer proposition explicitly covers every integer n>=4 and the ordinary untwisted H_n when g=I.
It uses no staggered transformation.
The reviewed odd-length interpolation therefore applies, and the new all-integer ranges starting at 52 remain valid.
This supplement uses only n>=4.

`SOURCE_SCOPE.md` gives the proof and comparison with the original theorem.
The official transfer, model, and introduction sources are pinned by Git blob hashes and preserved verbatim.
No earlier sealed review was edited.

Run `python verify.py > verify.log` in a disposable copy.
The exact comparison is 0.0102 against (4/105)log(80/79) for even L>=60, and against log20/784 for even L>=2304.
The later archived bound 0.005908566393 is distinct from the original theorem.
