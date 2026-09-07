# L1 measured results

Development-task REGRESSION only. Updated 2026-09-07. T1 C and A have completed;
B is running. C and A both passed the independent external audit at 100/100.
No plugin benefit can yet be inferred.

| T1 stage | Verdict | Score | Active seconds | Uncached input | Cached input | Output | Responses with usage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C blank solver | Frozen, independently accepted | - | 443.189 | 41354 | 86272 | 13231 | 7 |
| C independent blind audit | PASS, no load-bearing gap or repair | 100/100 | 393.085 | 32648 | 113408 | 12024 | 7 |
| C solver + external audit | Accepted | 100/100 | 836.274 | 74002 | 199680 | 25255 | 14 |
| A old solver, including internal audit | Frozen, independently accepted | - | 1277.998 | 123374 | 1425408 | 35714 | 29 |
| A independent blind audit | PASS, no load-bearing gap or repair | 100/100 | 432.192 | 62734 | 101120 | 12304 | 7 |
| A solver + external audit | Accepted | 100/100 | 1710.190 | 186108 | 1526528 | 48018 | 36 |

C proved the exact uniform polynomial root count and simplicity, with all
requested n=1, endpoint, midpoint and R=1 checks. The independent auditor
checked 17 claims and retained an additional exact algebra checker. The
checker supplements the submitted proof and is not the basis of uniform closure.

[Candidate](evidence/t1-c/answer.md), [audit](evidence/t1-c/audit/audit.json),
[solver usage](evidence/t1-c/usage-summary.json), and
[audit usage](evidence/t1-c/audit/usage-summary.json) bind this result.

Usage sums unique token_usage_record.response_id values across session files.
Cached input is included in provider input totals and subtracted once to obtain
uncached input. Reasoning output is included in output and is not added again.
These are returned usage records, not a conversion from account percentages.
Outer model calls, CLI command executions and complete nested tool calls are
different scopes; unknown aggregate active time and nested counts remain null.

The sum of timed solver and audit stages excludes the coordinator's intervening
setup work. Actual elapsed time from solver dispatch to audit return was about
1142.683 seconds; this first audit also required common harness preparation.
Keep setup/infrastructure costs separate in treatment comparisons. Earlier
INFRA_INVALID C and all its observed cost remain in the evidence directory.

The user explicitly removed quota reserves during C. C finished without hitting
its earlier loaded thresholds, so no interruption or extra wall allowance was
introduced. Later stages use the recorded no-reserve policy. This resource
amendment and the harness hash change must remain visible in comparisons.

A used one internal audit child. Its 29 returned responses include that child;
the interrupted in-flight response has no additional returned usage counter.
A naturally exhausted quota after 451.423 seconds, then completed the same
session using another 826.576 seconds. This does not establish a new-plugin
recovery benefit. See [continuation](evidence/t1-a/quota-continuation.json).

The solver exited normally. A local-file symlink blocked automatic freezing;
the stopped workspace was copied with that link materialized inside the frozen
copy after verifying the target and all before/after hashes. No solver rerun or
mathematical edit occurred. See [receipt](evidence/t1-a/freeze-reconciliation.json).
For external blindness, only A's leading status line reporting an earlier audit
PASS was removed from the auditor copy; all mathematical bytes remain unchanged.
The [binding](evidence/t1-a/blind-audit-binding.json) records both candidate hashes.

A's external audit checked 15 claims and retained a 16-identity exact algebra
checker. It exhausted quota after writing its report, then resumed the same
session for 41.105 seconds and returned normally. Its full 432.192 seconds and
all seven returned response records are counted. See [audit](evidence/t1-a/audit/audit.json)
and [audit continuation](evidence/t1-a/audit/quota-continuation.json).

At equal T1 proof quality, observed A/C solver ratios are 2.98 for uncached input
and 2.88 for active wall time. Full solver-plus-external-audit ratios are 2.51
for uncached input and 2.05 for active wall time. A includes two natural quota
continuations, so these raw observations do not isolate plugin overhead from
recovery overhead. B is required to assess the optimization; one development
task cannot establish a general performance advantage.
