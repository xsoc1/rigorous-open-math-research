# L1 old/new/blank regression protocol

Date: 2026-09-06. Status: T1_REPLACEMENT_R1_SEALED_WAITING_QUOTA.
Task bytes and treatment commits are selected. T1 uses the Linux CLI 0.153.4
and a pinned bundled model catalog; its three arms passed filesystem and
loopback request-capture checks. Scoring starts only after control/SEALED.json
binds the final config, gates and manifest. The original seal preceded any solver call. One infrastructure-invalid C attempt
then led to the replacement amendment below; no replacement solver has started.

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

Record dispatch intent before process creation, then retain allocated root/child
IDs as soon as they are observable. Incrementally retain output and persist
runner PID, active elapsed time and exact next action. A quota continuation
reuses the original session and remaining budget after artifact reconciliation;
it does not gain a fresh attempt. Unknown in-flight status remains UNKNOWN or
NO_RETURN, not a mathematical failure or success. The durable Linux runner retains segment logs, enforces a single campaign
lock and active-wall remainder, and stops on stale quota snapshots after five
minutes. Graceful cancellation has a five-second cleanup allowance, recorded
in elapsed time. Unknown unobserved intervals require budget reconciliation.

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

## Linux preflight amendment before the first scored call

The existing WSL loopback proxy became reachable after the environment change.
No new proxy bridge was started. The isolated executable hash is
`56ef98ab4032d317ab26e9b5e5a175650717351edb16ed9cde0cb6d1734d62da`.
The PATH CLI 0.149.1 is not used. Model catalog bytes are pinned for all arms.

Filesystem probes now include sibling reads and out-of-workspace writes. A
reachable loopback proxy supplies the positive network control. The source
auth file is copied only to private fresh homes and remains unavailable to
solver shell tools. No real credential is used by the request-capture stub.

Tool schemas were captured from synthetic requests to a loopback HTTP stub
using the same catalog, model and effort, with an explicit custom provider.
This validates client-side tool construction; it is not a live service test.
The common tools are shell/patch, local image viewing, clock, input questions
and agent collaboration. Network, browser, app and cross-task tools are absent.
A synthetic interrupted session resumes with the same root UUID. Live model
identity, usage and any infrastructure failure must still be recorded.

Four deterministic runner checks cover reserve/staleness, retained artifacts
and shared continuation budget, exclusive locking, and unknown usage. Synthetic
requests and runner tests are unscored infrastructure work. T2 is not sealed.

## Replacement amendment after initial C infrastructure failure

Initial C ran for 62.290282 seconds and was stopped after two attempted code
execution calls reported code-mode host is disabled. A child dispatch was also
observed. No result was scored. Preserve the full attempt, partial usage and
unknown child accounting as infrastructure cost; do not reuse its session.
The earlier request-schema gate missed this runtime failure.

All replacement arms use new homes under
/home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC-r1. The common mechanical
change enables code_mode_host and copies/hashes the matching helper executable.
Task bytes, plugin commits, model, effort, ordering, time caps, scoring and quota
thresholds remain the preregistered values. The replacement does not depend on
mathematical quality: the original attempt is excluded for unusable tools.

The stronger loopback stub now returns a synthetic tool call, executes the
sandbox probe through functions.exec, checks positive and negative controls,
then completes and resumes the same UUID. A/B/C all passed with real sandbox
command execution and no external model calls. The copied probe home contains
only a fake auth placeholder; actual arm auth denial is checked separately.
The runner refuses schema-only gates and invalid-attempt continuations. Its
seal also binds the runtime helper and harness code hashes.

Usage summaries are file-level cumulative observations. A duplicate session
header appeared in a second file after child dispatch; deduplication and unknown
in-flight usage must be resolved before reporting aggregate treatment cost.
The benchmark has zero valid completed runs and zero external audits so far.

## Resource amendment before the first r1 solver call

The user requested continuation with the five-hour window restored and 21% of
the weekly window remaining. The prior 25% weekly reserve was a coordinator
policy rather than a user-specified hard budget. For this continuation, start
with T1 C and its blind audit. Set the weekly stop threshold to <=10%, retaining
the five-hour launch >=35% and stop <25% thresholds. The weekly launch gate is
now >10%. This amendment changes only account reserve policy, before any r1
solver call. Task, treatment, model, effort, wall limits and scores retain their
original definitions. Preserve the previous seal and bind the updated runner.

## User override: no quota reserve

During T1 C, the user explicitly said no quota reserve is needed. This overrides
all prior reserve thresholds. Future dispatch and continuation require positive
available quota only; exhaustion, stale snapshots and the fixed active-wall cap
still stop execution. No reset-credit redemption was requested. The already
running first segment retains its loaded runner code, archived by hash in
control/runner-first-segment.py. If its former reserve triggers, continue the
same session with the unspent wall budget under this override. Record any pause.
