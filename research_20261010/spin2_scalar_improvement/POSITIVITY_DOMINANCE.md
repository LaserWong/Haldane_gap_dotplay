# Global twist positivity locates a positive trivial-sector leading atom

Updated: 2026-10-10 14:30 EDT / 18:30 UTC.

This is an analytic improvement to the atom-location step. It is separate from
the frozen counterexample. It does not supply thermal purity or a uniform gap.

## Hypotheses that must be retained

For one fixed beta and energy shift, suppose the archived self-adjoint spatial
transfer representation gives real, unit-multiplicity spectral lists J,N and,
when C is used, I,O, with finite fourth moments. At all sufficiently large
integer lengths, assume the exact identities

Z_identity(k)=J_k+3N_k=I_k+2O_k+3N_k,
Z_P(k)=J_k-N_k=I_k+2O_k-N_k,
Z_C(k)=I_k-O_k.

The physical twisted Hamiltonians are finite-dimensional and self-adjoint,
so each of these physical partition functions is strictly positive for every
integer length for which that representation applies. This uses all-length
analytic positivity, not additional computed heat traces. One must check that
the same transfer representation and sector identities hold for odd lengths;
odd positivity is essential for concluding that the leading atom is positive.
Finite fourth moment suffices for all limiting arguments below; an infinite
spectral list is allowed. This is not an inference from a finite sample of
positive trace values.

## 1. Sign of the extremal trivial-sector atom

J_k=(Z_identity(k)+3Z_P(k))/4>0 for all relevant odd k.
Let p_J be the supremum of the positive J atoms. If a negative atom -x had
x>p_J, then for large odd k>=5 its negative contribution would dominate:

J_k <= J_4 p_J^(k-4) - x^k < 0.

(The case p_J=0 is immediate.) This is a contradiction. Hence
sup|J|=p_J. The nonzero supremum is attained, because fourth-moment summability
allows only finitely many atoms above any fixed positive modulus.

Likewise I_k=(Z_identity(k)+3Z_P(k)+8Z_C(k))/12>0 on odd k, and
sup|I|=p_I. No positivity of the odd O moments is asserted or needed.

## 2. Dominance over nontrivial sectors

Z_P(2k)=J_(2k)-N_(2k)>0 implies sup|N|<=sup|J|. Otherwise choose an N atom
whose modulus x exceeds sup|J| and compare x^(2k) with
J_4 sup|J|^(2k-4) as k tends to infinity.

With C available, Z_C(2k)=I_(2k)-O_(2k)>0 similarly implies
sup|O|<=sup|I|. Then Z_P(2k)=I_(2k)+2O_(2k)-N_(2k)>0 yields
sup|N|<=sup|I| by the same fourth-moment comparison.

Thus the largest modulus of the complete spatial spectrum is realized by a
positive J atom, and by a positive I atom when the finer decomposition exists.
In particular an assumption that there is no positive J atom above ell also
bounds EVERY atom in all lists by ell. The analogous statement holds for I.

## 3. A cheap exact atom-location certificate

For even L>q>=4, if every atom has modulus <=ell, then

Z_identity(L) <= ell^(L-q) Z_identity(q).

Hence any certified Z_identity(L)>B>0 and Z_identity(q)<=U exclude this
hypothesis whenever U ell^(L-q)<B. This locates a positive J (or I) atom above
ell without independently requiring an N-sector mass majorant below one.
It resolves the logical conditional-exclusion loophole in the old coarse test.

At beta8 use the already archived L8 untwisted upper interval at a0=4.7608.
At a1=4.76121 this remains an upper bound because increasing the shift reduces
Z8. The existing D124 MPS gives Z_L(beta8;a1)>1 at L=128,256,512,1024.
`verify_atom_location.py` chooses rational ell and checks U8*ell^(L-8)<1 using
only exact Fractions. No new finite trace or MPS contraction is needed.

These are conditional certificates under the stated transfer hypotheses and
inherited finite-input verification assumptions. The saved exact MPS tensor
has a distinct physical bond dimension 124; the atom-location argument does
not enlarge it or diagonalize a many-body Hamiltonian.

## 4. What this does not settle

A leading trivial-sector atom does not imply a separated second atom, spatial
purity near one, or physical thermal purity near one. The frozen I/P witness
already has a positive leading J atom and nonetheless defeats the current
numerator-one thermal recipe. A new ratio or multi-state numerator argument
would have to bring additional information. Do not launch higher-order traces
just because the atom-location step is now available.
