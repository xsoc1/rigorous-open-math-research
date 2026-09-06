# Research ledger

- 2026-09-06T12:58:15Z: Started blind run. Read requested workflow and research dependencies. No AGENTS.md found in workspace. No external or prior-result retrieval performed.
- Direct closure attempt, owner /root: compute det(C)=1 and tr(C)=2z with z=(a cos^2(y)-s-s^{-1})/2. Direct multiplication gives (EC)12=sin(y)(a cos^2(y)-s). The recurrence therefore yields H_n(z)=U_n(z)+s^{-1}U_{n-1}(z).
- Cheapest exact falsification probes: n=1 gives Q_1=a x^2-s and roots +/-s/(s+1); at y=pi/2 direct diagonal multiplication gives G=(-s)^n. Both agree with the recurrence. No numerical scan used.
- Root-location closure: H_n at z_j=cos(j*pi/n), j=0,...,n, has alternating nonzero signs. Continuity gives n distinct roots and exact degree n proves exhaustiveness and simplicity. Since z(0)=-(s+s^{-1})/2<-1 and z(1)=1, each H-root produces two distinct interior x-roots.
- Candidate consolidated on disk before independent audit. No route expansion is needed. One fresh independent audit will decide closure versus a precisely localized repair.

- 2026-09-06T13:18:30.412310+00:00: Reconciled continuation: only /root existed before dispatch, and all saved candidate records remained available. Frozen candidate and completion manifest written. Pre-dispatch artifact validation initially identified incompatible pending-audit gate labels; corrected to ESCALATE / CONTINUE_REQUIRED, after which validation passed (one advisory: Lean manifest then absent). No mathematical proof edits arose from these metadata checks.
- 2026-09-06T13:18:30.412310+00:00: Fresh independent completion audit claimed by /root/completion_auditor, covering O1--O5; candidate author remains /root. Review deadline 13:22:00Z. No other worker or route was dispatched.
- 2026-09-06T13:18:30.412310+00:00: Formalization decision registered as an uncompiled scaffold. Static scan found 5 intentional sorry placeholders; Lean/Lake unavailable. No formal verification is claimed.

- 2026-09-06T13:23:34.143473+00:00: Independent reviewer returned PASS for O1--O5, with no load-bearing gaps or critical errors. Verified the returned audit and report hashes and their binding to the unchanged candidate. Certified STOP; no further research initiated.
- Auditor also reports non-load-bearing exact Laurent-polynomial and rational consistency probes; their scope is recorded in audit_report.md. The final proof uses no finite-computation premise.
- answer.md is the frozen candidate body with only its first status line upgraded after audit. All formal-track limitations remain explicitly recorded.

- Final integrity check passed. The workflow gate then exposed a relative-path convention difference for the source dependency. Added a run-local symlink to the identical canonical source bytes, preserving all frozen proof/manifest/audit hashes. No mathematical or bound-artifact content changed.
