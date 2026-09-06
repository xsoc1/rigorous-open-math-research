# L1 old/new/blank regression protocol

Date: 2026-09-06. Status: DRAFT_INFRASTRUCTURE_PREFLIGHT_FAILED.
Task bytes and treatment commits are selected; launch configuration and runner
must be sealed only after successful isolation checks. No solver has started.

## Objective and treatments

Test the incremental effect of the optimization and its total cost relative to
blank Codex. A uses parent commit `516037f14f340107da8448b6e42df17317d9fc63`.
B uses `6d6d739645981a5a2970b5faa26adda49a724113`. Both install the four actual
marketplace plugins and invoke math-research-workflow. C installs no research
plugin and receives only the common task and output contract. All arms retain
the same basic tool permissions and access to at most three concurrent children.

Requested common model/effort: gpt-6-astra / max. CLI 0.153.4 is available as
both Windows and Linux binaries. Select one platform for every scored arm after
preflight; do not compare different platform binaries as a plugin-only effect.
Confirm actual model/effort and tool exposure from run records. Missing actual
identity is UNKNOWN, never inferred from the requested config.

## Tasks and ordering

These are known development problems, labeled REGRESSION. The coordinator has
seen historical answers. Every solver receives a fresh session/home/workspace
and no historical answers. This is not a novelty or hidden-holdout experiment.

| Task | Frozen source in BVE | SHA256 | Order |
| --- | --- | --- | --- |
| T1 B3 O3 root count | runs/plugin-benchmark-20260824-calibration/frozen_task.md | 1fa717b9a5f195c42ecca97d51e20327cb4eb2c316c936c054f55f7dd7416f16 | C, A, B |
| T2 U2 lamplighter TV | runs/three-arm-pilot-v2/pilot-v5-codex-u2/frozen_task.md | 6859e0af922ba8454758e2195fcefcfe8fa164a40e2c23022ec7ebb2da228943 | B, A, C |

One scored attempt per arm per task. Finish and inspect T1 before scheduling
T2. Score infrastructure-invalid attempts separately and retain their full
cost; replacements require a documented cause and a fresh work directory.
Do not replace a mathematically weak result or retroactively change thresholds.

## Budget and persistence

Each root and its internal children share a 30 minute active-wall cap. External
blind audit has a separate 15 minute cap per frozen arm. These are upper bounds,
not predicted use. Additional repairs or adjudications are separately logged
and cannot improve the original frozen score.

Launch only with a fresh account snapshot and enough reserve: at least 35%
five-hour remaining and 25% weekly remaining. At 25% five-hour remaining, stop
new research and preserve/reconcile current work. Account percentages are shared
and are not converted into per-task tokens. Never redeem reset credit without
explicit authorization. Check at stage boundaries and during long runs.

Record root/child IDs before dispatch, incrementally retain output, and persist
runner PID, active elapsed time and exact next action. A quota continuation
reuses the original session and remaining budget after artifact reconciliation;
it does not gain a fresh attempt. Unknown in-flight status remains UNKNOWN or
NO_RETURN, not a mathematical failure or success. The durable runner is still
to be implemented and tested before scoring.

## Isolation gate

Use separate homes, workspaces and immutable plugin snapshots. Disable project
AGENTS injection, memories, apps, web/browser/computer tools and host skill
discovery. C must have zero research skill metadata. A/B must show their exact
installed skills. Verify tool schemas, not just feature flags. Keep task,
internal audit, external audit and prior-arm output separated.

Before inference, test workspace writes, plugin reads, denied access to the
main project, sibling arms, historical benchmark outputs and authentication
files. Test network denial against a reachable baseline endpoint; a timeout
to a generally unreachable endpoint does not certify network isolation.
No scored launch is allowed on a failed or incomplete gate.

## Evaluation and decision

Freeze each answer and relevant proof dependencies before the label-blind
external audit. Auditor receives the common statement and frozen mathematics,
without treatment labels, usage, author exploration, or previous verdicts.
Use the same six axes: correctness 40, fidelity 20, strict progress 15,
calibration 10, evidence 10, reproducibility 5. Scores do not erase verdicts.
Require at least 70 overall and 32 correctness for the historical acceptance
threshold; any load-bearing gap prevents proof-level PASS.

Compare required-root closure and audited partial progress before cost. Report
uncached/cached input, output, responses, actual tool calls, child sessions,
root and aggregate active time, first proof, audit and total delivery cost.
Unknown fields remain null. Internal audit and protocol work are charged to
their treatment; report external audit separately and in full-delivery totals.

For B vs A, provisional go/no-go targets remain: no quality regression hiding
a load-bearing gap; median paired uncached-input ratio <= 0.75; root active-wall
ratio <= 0.80; total internal delivery time regression <= 10%. Also compare B
and A against C without assuming the plugin should win. Require zero duplicate
dispatch, lost returned artifact, unauthorized replay or research after STOP.
With two development tasks these are diagnostic decisions, not general claims.

Live literature-to-tool reuse and controlled in-flight interruption are separate
unscored feature acceptances. They do not introduce network into offline arms.
L2 and model/effort ablations remain later stages, not automatically dispatched.

## Sources and infrastructure record

Configuration and isolation procedures consult the official
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
and [non-interactive guide](https://learn.chatgpt.com/docs/non-interactive-mode),
alongside the installed binary's help and generated schemas. Local behavior
must pass the gate even when configuration text appears correct.
Current observed failures and recovery steps are in [STATUS.md](STATUS.md).
