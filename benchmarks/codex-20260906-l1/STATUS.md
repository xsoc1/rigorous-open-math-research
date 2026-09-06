# L1 three-arm regression status

Updated: 2026-09-06. State: T1_REPLACEMENT_READY_WAITING_QUOTA.

User requested continuation. Preparation and one infrastructure-invalid attempt
are recorded. Valid completed/scored runs: 0. External mathematical audits: 0.
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
  Every replacement solver home has zero solver sessions at sealing.
- Four deterministic runner checks and all 81 repository checks passed.
- Last quota snapshot: 2026-09-06T07:13:41Z, five-hour remaining 22%, weekly
  remaining 24%. Below the 35% / 25% launch gate. No reset redemption authorized.

## Exact next action

1. Read this file, git status and r1 control/SEALED.json. Do not prepare another
   campaign or reinstall the plugin. Inspect any run/state.json before dispatch.
2. Obtain a fresh account snapshot. Update r1 control/quota.json with captured_at
   (UTC ISO timestamp), five_hour_remaining and weekly_remaining. These are
   account-level data, not treatment costs. Launch only at >=35% / >=25%.
3. Run from the checkout:
   python3 -X utf8 scripts/benchmark_runner.py --root /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC-r1 --task t1 --arm C
4. Refresh the quota file during execution. It expires after five minutes;
   reaching the reserve or creating run/STOP causes cancellation and checkpoint.
   The runner retains segment logs, root ID, observed child sessions and elapsed
   budget. An ordinary PAUSED state can use --resume with the same task/arm;
   --reconcile handles uncertain exits without creating another attempt.
5. Freeze and inspect the returned mathematics, perform the separately budgeted
   label-blind audit, and calibrate cost before A/B. Complete usage deduplication
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
