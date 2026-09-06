INDEPENDENTLY_AUDITED_PROOF

Verdict: **PASS**. All root obligations O1--O5 are closed. There are no load-bearing gaps or critical errors. This is an informal mathematical audit, not Lean verification.

Author: `/root`. Fresh independent reviewer: `/root/completion_auditor`.
Reviewed at: 2026-09-06T13:20:30.671702+00:00.
Frozen completion-manifest SHA-256: `ba4cc98072bebfe51db7c51b867fc4531248fd468416f7ad041bbc86828300f5`.
Candidate-proof SHA-256: `d0f59db7d9f968a1b15b85eb2d9142c3e82c3680c5ed2a0e013394841d972b22`.

## Package and definition audit

I read only the permitted source statement and the five named current-run package files, together with the installed skill and its phase-78 audit instructions. No prior solutions, projects, repositories, git data, memory, sessions, internet, or external mathematical sources were consulted. No other auditor was spawned. The source, contract, obligation graph, and candidate bytes match their manifest hashes; the manifest matches the hash supplied in the audit task. The review took place after the recorded freeze.

The statement is exactly the matrix-entry problem for every integer n >= 1 and every real R > 1, with s = sqrt(R) > 1. The candidate retains E, C_s, the multiplication order E C_s^n, and the (1,2) entry. It proves the polynomial identity using the question's arccos definition, counts zeros only in (0,pi), and interprets simplicity as nonvanishing first derivative. R=1 is explicitly treated as an additional boundary check. No PDE fact or correctness of the physical interpretation is needed as a premise for this matrix theorem.

## O1: polynomial identity and exact degree

Independent algebraic derivation: set r=1/s and

    E_s = [[c, r q], [-s q, c]].

Multiplying gives C_s=E_s E exactly, including both off-diagonal signs. Both factors have determinant c^2+q^2=1; expansion also gives det(C_s)=(c^2+q^2)^2. The trace is

    2c^2-(s+r)q^2 = (s+2+r)c^2-s-r = 2z(c).

Direct multiplication of E by C_s gives

    (E C_s)12 = c(1+r)cq + q(c^2-sq^2)
               = q((2+r)c^2-sq^2)
               = q((s+2+r)c^2-s).

Thus G_0=q and G_1=q(2z+r), with the required multiplication order. For a general matrix [[u,v],[w,t]], expansion of A^2-(u+t)A+(ut-vw)I cancels each entry. Applying that identity to C_s and multiplying on the left by E C_s^(k-1), for k>=1, proves G_(k+1)=2zG_k-G_(k-1). There is no commutation assumption involving E. The stated U recurrence yields precisely the same H recurrence and initial values. Induction proves G_n(y)=sin(y)H_n(z(cos(y))) for all real y, so it is valid at the endpoints too.

For x in (-1,1), sin(arccos x)=sqrt(1-x^2)>0, and division gives the exact Q definition. The degree of U_n is n with leading coefficient 2^n: the degree-n+1 term of 2zU_n cannot cancel against U_(n-1). Adding rU_(n-1) leaves that coefficient unchanged. Composing with z(x), of degree two and leading coefficient a/2 where a=s+2+r>0, gives degree exactly 2n and leading coefficient a^n. Uniqueness of the extension follows from the polynomial root bound. O1 passes.

## O2: all H roots, location and multiplicity

The sine addition identity verifies U_k(cos theta)=sin((k+1)theta)/sin theta for 0<theta<pi by the given recurrence and base case. Evaluating the recurrence at +/-1 gives the claimed endpoint values independently of this formula, whose denominator vanishes there.

At the internal grid points theta_j=j*pi/n, 1<=j<=n-1, one has sin(n theta_j)=0 and

    sin((n+1)theta_j)=sin(j*pi+theta_j)=(-1)^j sin(theta_j).

Hence H_n(cos theta_j)=(-1)^j. At the endpoints, H_n(1)=n+1+rn>0 and H_n(-1)=(-1)^n(n+1-rn), with n+1-rn>0 because 0<r<1. Consequently the signs alternate across every adjacent pair of the strictly ordered grid. This includes the first and last intervals, and for n=1 the single interval is bounded by the two endpoint values and requires no internal grid points.

The n open grid intervals are disjoint, and the intermediate value theorem gives a distinct real root in each. Factoring these n distinct roots out of a degree-n polynomial gives a nonzero constant times their product. This proves exactly n roots, all in (-1,1), each of multiplicity one; it proves both location and simplicity, beyond a degree bound. O2 passes.

## O3: transfer to Q and G

For any root t of H_n in (-1,1), solving z(x)=t gives x^2=(2t+s+r)/a. Since s+r-2=(s-1)^2/s>0,

    0 < 2t+s+r < a.

There are precisely two real preimages, both strictly inside (-1,1), and neither is zero. Distinct t give distinct squared values, so no pair overlaps another pair. These are all Q roots by the proved composition identity; no further real or complex roots are possible after the degree is exhausted. At a preimage x, z'(x)=ax is nonzero and H_n'(t) is nonzero, so Q'(x)=ax H_n'(t) is nonzero.

Cosine is a bijection from (0,pi) to (-1,1), and sin(y)>0 on this interval. Thus G has exactly the 2n corresponding roots. Differentiating the identity gives, at a root, G'(y)=-sin(y)^2 Q'(cos y), which is nonzero. No division by a vanishing factor occurs. Both the count and simplicity hold uniformly for every allowed s and n. O3 passes.

## O4: low order and exceptional points

The n=1 matrix calculation above independently yields Q_1(x)=a x^2-s, whose roots are +/-s/(s+1). They are nonzero, have absolute value less than one, and have nonzero derivatives 2ax. As a second check, H_1(z)=2z+r has root -r/2, and the quadratic substitution gives exactly the same squared value s/a.

At y=0 and y=pi, direct substitution yields C_s=I and E=I and -I respectively, hence G=0. The derivative from the polynomial identity equals +(n+1+n/s) at zero and its negative at pi. Independently, to first order near zero, C_s=I+yA+O(y^2), E=I+yJ+O(y^2), where A12=1+r and J12=1; the derivative of E C_s^n is J+nA. Near pi the same C expansion and E=-I-(y-pi)J+O((y-pi)^2) give the opposite derivative. These roots are simple and excluded from the requested count.

At y=pi/2, direct matrix multiplication with C_s=diag(-r,-s) gives G_n=(-s)^n. As an independent second derivation, z(0)=-(s+r)/2, H_0=1 and H_1=-s. The recurrence h_(k+1)=-(s+r)h_k-h_(k-1), with sr=1, gives h_k=(-s)^k by induction. Thus the midpoint formula agrees by two different calculations and is never zero.

At R=1, the entries give C_1=E(2y)=E(y)^2. The angle addition identity E(u)E(v)=E(u+v) yields G_n=sin((2n+1)y); its interior zeros are exactly k*pi/(2n+1), 1<=k<=2n, with derivatives (2n+1)(-1)^k. The endpoints and midpoint agree with the candidate. A separate check through the general argument uses r=1: n+1-rn=1, and t>-1 ensures 2t+2>0. It therefore retains the same interior count and simplicity. The trigonometric U formula gives Q_(n,1)=U_(2n) on (-1,1), with the degree and roots claimed. O4 passes.

## O5: dependencies and logical audit

The proof uses the intermediate value theorem for a continuous real function on a closed nondegenerate interval with opposite endpoint signs; here the function is a polynomial and the ordered grid ensures all hypotheses. The polynomial factor theorem is used over the real numbers with a nonzero polynomial of known exact finite degree; distinct factors exhaust the degree, establishing multiplicity as well as the root bound. Product and chain rules apply to differentiable real polynomials and trigonometric functions. The elementary angle addition identities, derivatives, and the monotone bijection of cosine on (0,pi) are used within their stated real domains. Matrix recurrence and the needed U facts are derived in the proof; no spectral or literature theorem is assumed.

There is no circularity, generic-parameter restriction, unstated limiting step, missing parity case, or compatibility problem. The dependency O1+O2 -> O3 is valid; the required boundary checks and theorem hypotheses are discharged. O5 passes.

## Exact probes and decision

A short in-memory exact Laurent-polynomial calculation independently checked C_s=E_s E, det(C_s)=(c^2+q^2)^2, and the direct n=1 formula. Exact rational matrix calculations also checked the recurrence and midpoint at s=1, 1001/1000, 2, and 10^6, n=1,...,12, and the exact circle points (+/-1,0), (0,1), and (+/-3/5,4/5). These are consistency probes only; the uniform theorem rests on the algebraic and root-count arguments audited above.

Covered scope: contract fidelity; O1--O5; every integer n>=1 and real R>1; exact polynomial extension, degree, root location, multiplicity and G derivatives; n=1, both endpoints, the midpoint, and R=1; all load-bearing dependency hypotheses.

Residual risk: informal mathematical audit only. Lean/kernel verification and an external literature or novelty audit were not performed. No mathematical obligation within the requested scope remains unchecked or unresolved.

Critical errors: none. Load-bearing gaps: none. Repair hints: none required.

Decision delta: candidate completion -> independently audited completion; the zero-gap PASS supports certified STOP. No additional research route is required.
