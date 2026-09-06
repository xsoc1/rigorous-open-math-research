# L1 measured results

Development-task REGRESSION only. Updated 2026-09-06. T1 C has completed;
A and B have not produced scored results. No plugin benefit can yet be inferred.

| T1 stage | Verdict | Score | Active seconds | Uncached input | Cached input | Output | Responses with usage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C blank solver | Frozen, independently accepted | - | 443.189 | 41354 | 86272 | 13231 | 7 |
| C independent blind audit | PASS, no load-bearing gap or repair | 100/100 | 393.085 | 32648 | 113408 | 12024 | 7 |
| C solver + external audit | Accepted | 100/100 | 836.274 | 74002 | 199680 | 25255 | 14 |

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
