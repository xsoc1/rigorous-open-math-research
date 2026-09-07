# L1 three-arm regression status

Updated: 2026-09-07. State: T1_C_A_AUDITED_B_RUNNING.

User requested continuation. Preparation and one infrastructure-invalid attempt
are recorded. Completed solver runs: 2 (T1 C and A). Scored/audited runs: 2.
T1 C and A blind audits both PASS, 100/100, no load-bearing gap or repair.
A solver used 1277.998200 active seconds; its external audit used 432.192049.
T1 B launched at 2026-09-07T01:48:49Z. Inspect t1/b/run/state.json before dispatch.
Its first segment exited after 12.037755 seconds because the isolated refresh
token was already used. Only private same-account authentication was refreshed.
Session 01a0798d-cd6d-7b22-bbd2-bb4b4a1fdb43 resumed at 01:51:36Z with that time
still charged. No new attempt or config change was introduced.
The intended experiment remains old plugin A / new plugin B / blank Codex C,
with T1 order C,A,B and T2 order B,A,C. T2 is prepared but not sealed.

## Current verified execution path

- Real checkout: /mnt/f/LaTeX/BVE research/_xsoc1_work. Ignore malformed desktop cwd.
- Current campaign: /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC-r1.
- Isolated CLI: /home/huangzy/codex-benchmark-runtime/0.153.4/codex, plus its
  matching code-mode host. Both binaries and the bundled catalog are hash-bound.
  The PATH CLI 0.149.1 is not part of this experiment.
- A commit: 516037f14f340107da8448b6e42df17317d9fc63.
  B commit: 6d6d739645981a5a2970b5faa26adda49a724113.
  All arms use gpt-6-astra / max and the same basic tools and child limit.
- Existing WSL loopback proxy now works. No previously rejected bridge was run.
- All T1 arms passed filesystem and network isolation, expected skill metadata,
  actual functions.exec sandbox execution and synthetic same-session resume.
  These stub tests used no external model calls and no real auth credentials.
- control/SEALED.json binds the manifest, harness code and six successful gates.
  At sealing, replacement homes had zero solver sessions. T1 C has since finished.
- Four deterministic runner checks and all 81 repository checks passed.
- B launch quota snapshot: 2026-09-07T01:48:49Z, five-hour remaining 50%, weekly
  remaining 76%. Historical snapshot only. The user has removed both reserve thresholds.
  Read live quota before dispatch; no reset redemption was authorized.

## A quota interruption and continuation

- Original session: 01a076cc-139f-76f1-aede-3af2443f3a4a.
- Segment 01 exited with code 1 after 451.422577 active seconds. CLI events
  explicitly report usage-limit exhaustion. The runner recorded INFRA_EXIT
  because the CLI exited before the next account snapshot reached zero.
- Segment 02 started at 2026-09-06T13:11:55Z with the same session ID and
  1348.577423 seconds remaining from the original 1800-second allowance.
  The research ledger, contract and candidate proof survived the interruption.
- This is an observed infrastructure recovery in old arm A, not a controlled
  test proving an advantage of the new plugin. No mathematical score is assigned
  before the returned candidate is frozen and independently audited.
- External A audit also hit actual quota after saving its PASS report, at
  391.086886 active seconds. On the user's 2026-09-07 continuation it resumed
  session 01a076e8-54ca-7531-b267-9c8372da88ed, returned normally after another
  41.105164 seconds, and was frozen. Scores, input/output hashes and actual
  model/effort were checked. All 15 claims pass; no repair was supplied.

## Exact next action

1. Read this file, git status and r1 control/SEALED.json. Do not prepare another
   campaign or reinstall the plugin. Inspect any run/state.json before dispatch.
2. Obtain a fresh account snapshot. Update r1 control/quota.json with captured_at
   (UTC ISO timestamp), five_hour_remaining and weekly_remaining. These are
   account-level data, not treatment costs. The user explicitly removed quota reserves. Launch with positive available
   quota; stop on actual exhaustion, stale snapshots or the fixed wall cap.
3. T1 C and A, including both external audits, are complete. Do not repeat them.
   Inspect t1/b/run/state.json. If B paused or exited due to quota, continue the
   existing session with its unspent 1800-second allowance:

   python3 -X utf8 scripts/benchmark_runner.py --root /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC-r1 --task t1 --arm B --resume
4. Refresh the quota file during execution. It expires after five minutes;
   actual exhaustion or creating run/STOP causes cancellation and checkpoint.
   The runner retains segment logs, root ID, observed child sessions and elapsed
   budget. An ordinary PAUSED state can use --resume with the same task/arm;
   --reconcile handles uncertain exits without creating another attempt.
5. After B returns, freeze and measure it, then prepare its independent external
   audit with benchmark_audit.py --task t1 --arm B. Apply the recorded leading
   status-line blinding rule if needed. Complete usage deduplication
   before aggregate cost comparisons. Missing returns or usage stay UNKNOWN.
6. T2, feature literature-to-tool reuse, controlled research interruption, L2
   and model/effort ablations remain later work. Do not dispatch them implicitly.

## Preserved invalid attempt and earlier evidence

Initial Linux campaign: /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC.
Its C root was 01a07589-bd4d-7291-bb67-129338dbe34b, stopped after 62.290282 s.
Two calls failed because code_mode_host was disabled while the schema still
exposed functions.exec. A child dispatch was observed. This is INFRA_INVALID,
not a mathematical failure. Its invalid-attempt.json prevents continuation.
Known root cumulative usage is 33755 input (21888 cached) and 469 output.
A second file reuses the root header ID and has no returned usage; total child
cost is unknown. Do not sum inherited/fork records as separate fresh usage.

Windows preparation and failed probes remain under
F:/benchmark/L1-20260906-ASTRA-ABC. Restricted and explicit-deny probes could read
forbidden files, so no Windows solver was launched. A network timeout alone did
not certify isolation. Automatic approval rejected a bridge start with only
blocked by policy; no bridge receipt or process was created by that command.
The existing proxy later became reachable after the user changed environments.

Git contains only manifest/probe summaries and invalid-attempt observations.
Auth files, raw sessions and private runtime data remain outside the repository.
Current BVE mathematics, accepted graph and Q9 were not changed. This benchmark
branch does not change released plugins or require a DSH/runtime installation.
