# Problem contract

Authoritative input: the user's frozen B3 O3 root-count statement, received 2026-09-06. All definitions of E, C_s, M_{n,s}, G_{n,s}, and Q_{n,s} are exactly those in that statement.

## Objects and hypotheses
Integer n >= 1; real R > 1; s = sqrt(R) > 1. The function G is the (1,2) entry of E(y) C_s(y)^n. The interval is the open interval (0, pi).

## Target and acceptance criteria
Prove or disprove, uniformly in n and R, that G has exactly 2n distinct zeros in (0, pi) and that its derivative is nonzero at every such zero. Any polynomial reduction must prove equality on (-1,1), polynomial extension, exact degree, location of all roots, and simplicity. Audit n=1, y=0, y=pi, y=pi/2, and R=1 separately. Do not include endpoints in the count.

## Quantifiers and permitted outcomes
The assertion is for every integer n >= 1 and every real R > 1, without genericity or asymptotic qualifications. A proof, a counterexample, or a rigorous partial theorem with the first exact remaining gap is permitted.

## Non-completion conditions
Finite scans, numerical evidence, pairing alone, an upper bound alone, or an unproved polynomial equivalence do not complete the task.

## Tool and source constraints
Blind benchmark: use only the user statement, this workspace, and available tools. No other projects, repositories, git history, prior solutions, sessions, memory, internet, literature search, or later novelty audit. Installed skill instructions may be read as requested. Full wall budget 30 minutes, including agents; final consolidation by minute 25. Start 2026-09-06T12:58:15Z; consolidation deadline 13:23:15Z; final deadline 13:28:15Z. No formal verification was expressly requested. No Lean or Lake executable was found on PATH.

## Equivalent formulation
To be justified in the proof: Q(x) = H_n((a x^2 - s - s^{-1})/2), where a=s+2+s^{-1} and H_n(z)=U_n(z)+s^{-1}U_{n-1}(z).

## Contract audit
All original quantifiers and listed edge cases are retained. No ambiguity requires user input. Root simplicity means a nonzero first derivative, and endpoint roots are excluded.
