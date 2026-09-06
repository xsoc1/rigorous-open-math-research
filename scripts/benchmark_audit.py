#!/usr/bin/env python3
"""Prepare and run a label-blind, separately budgeted mathematical audit."""

import argparse
import fcntl
import json
from pathlib import Path
import shutil
import uuid

import benchmark_codex as B
import benchmark_runner as R


PROMPT = """Independently audit TASK.md against the candidate mathematics in CANDIDATE.md.
Use only these files and local scratch tools. You receive no author identity,
treatment, exploration history, usage statistics or previous verdict.
Check every load-bearing implication, quantifier, parameter endpoint, claimed
multiplicity and exact requested special case. Numerical checks can falsify;
they cannot replace a uniform exact proof. Identify the earliest substantive gap.
Distinguish a missing proof from a false claim. Do not silently supply a missing
load-bearing argument and then classify the submitted proof as complete.
Return audit.json with verdict PASS, REPAIRABLE_GAP, FAIL or INCONCLUSIVE;
scores (correctness /40, fidelity /20, strict_progress /15, calibration /10,
evidence /10, reproducibility /5), total_score, load_bearing_gaps (array),
checked_claims (array), and rationale. Also write a short audit.md.
Correctness assesses proof validity; fidelity assesses the exact task; strict
progress assesses demonstrated closure; calibration assesses truthful claims;
evidence assesses verifiable support; reproducibility assesses independent checking.
A score >=70 with correctness >=32 meets the historical score threshold but
does not erase a load-bearing gap. PASS requires all requested claims proved.
Any repair you supply must be labeled separately and cannot improve the original
submitted proof's verdict or score. Your entire audit, including any children,
has a 15 minute wall limit. Consolidate by minute 12 and stop after the audit.
"""


def prepare(campaign, task, arm):
	Source = campaign / task / arm.lower()
	State = R.read_json(Source / "run/state.json")
	if(State["status"] not in ["RETURNED_UNAUDITED", "BUDGET_EXHAUSTED"]):
		raise RuntimeError("candidate is not frozen")
	Frozen = Source / "run/frozen-work"
	Hashes = R.read_json(Source / "run/frozen-hashes.json")
	for Name in ["TASK.md", "answer.md"]:
		if(R.file_hash(Frozen / Name) != Hashes[Name]):
			raise RuntimeError("candidate changed after freeze")
	Manifest = R.read_json(campaign / "control/manifest.json")
	Root = campaign.parent / "blind-audits" / str(uuid.uuid4())
	Base, Home, Work = B.arm_paths(Root, "candidate", "C")
	Home.mkdir(parents=True)
	(Work / "tmp").mkdir(parents=True)
	(Root / "control").mkdir()
	shutil.copyfile(campaign / "control/model-catalog.json", Root / "control/model-catalog.json")
	shutil.copyfile(Frozen / "TASK.md", Work / "TASK.md")
	shutil.copyfile(Frozen / "answer.md", Work / "CANDIDATE.md")
	B.write_text(Work / "PROMPT.md", PROMPT)
	B.write_text(Root / "candidate/a/work/TASK.md", "FOREIGN_AUDIT_CANARY\n")
	Auth = Source / "home/auth.json"
	B.configure(Home, Work, Path(Manifest["binary"]), False, Manifest["python"], Auth)
	shutil.copyfile(Auth, Home / "auth.json")
	(Home / "auth.json").chmod(0o600)
	AuditManifest = {Key: Manifest[Key] for Key in ["binary", "binary_sha256", "python", "python_sha256", "proxy", "model", "effort", "model_catalog_sha256", "code_mode_host_sha256"]}
	R.persist(Root / "control/manifest.json", AuditManifest)
	Mapping = dict(root=str(Root), task_sha256=R.file_hash(Work / "TASK.md"),
		candidate_sha256=R.file_hash(Work / "CANDIDATE.md"), prompt_sha256=R.file_hash(Work / "PROMPT.md"),
		config_sha256=R.file_hash(Home / "config.toml"), created_at=R.utc_now(), budget_seconds=900)
	R.persist(campaign / f"control/audit-{task}-{arm}.json", Mapping)
	return Mapping


def run(args):
	Campaign = Path(args.campaign).resolve()
	MapPath = Campaign / f"control/audit-{args.task}-{args.arm}.json"
	Mapping = R.read_json(MapPath) if MapPath.exists() else prepare(Campaign, args.task, args.arm)
	Root = Path(Mapping["root"])
	Base, Home, Work = B.arm_paths(Root, "candidate", "C")
	Manifest = R.read_json(Root / "control/manifest.json")
	for Name, Key in [("TASK.md", "task_sha256"), ("CANDIDATE.md", "candidate_sha256"), ("PROMPT.md", "prompt_sha256")]:
		if(R.file_hash(Work / Name) != Mapping[Key]):
			raise RuntimeError("changed audit input")
	if(R.file_hash(Home / "config.toml") != Mapping["config_sha256"]):
		raise RuntimeError("changed audit config")
	GatePath = Root / "control/gates.json"
	if(not GatePath.exists()):
		ProbeArgs = argparse.Namespace(root=str(Root), project=args.project, task="candidate", arm="C")
		B.probe(ProbeArgs)
		B.probe_tools(ProbeArgs)
		Gates = []
		for Pattern in ["preflight-*/summary.json", "tools-*/summary.json"]:
			File = max(Base.glob(Pattern), key=lambda Path: Path.stat().st_mtime)
			if(R.read_json(File)["verdict"] != "PASS"):
				raise RuntimeError("audit preflight failed")
			Gates.append(dict(path=str(File), sha256=R.file_hash(File)))
		R.persist(GatePath, Gates)
	for Gate in R.read_json(GatePath):
		if(R.file_hash(Gate["path"]) != Gate["sha256"]):
			raise RuntimeError("changed audit gate")
	if(args.prepare_only):
		print(json.dumps(Mapping))
		return
	Output = Base / "run"
	Output.mkdir(exist_ok=True)
	with (Campaign / "control/runner.lock").open("a") as Lock:
		fcntl.flock(Lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
		StatePath = Output / "state.json"
		State = R.read_json(StatePath) if StatePath.exists() else dict(root_thread_id=None, active_seconds=0, segments=[], role="BLIND_AUDIT")
		if(StatePath.exists() and (not args.resume or State["status"] not in ["PAUSED", "INFRA_EXIT"])):
			raise RuntimeError("audit already dispatched; explicit reconciled continuation required")
		Reason = R.quota_reason(Campaign / "control/quota.json", launching=True)
		if(Reason):
			raise RuntimeError(Reason)
		Command = [Manifest["binary"], "exec", "--strict-config", "--json", "--skip-git-repo-check", "--ignore-rules", "-C", str(Work), "-o", str(Output / "last-message.txt")]
		if(args.resume):
			if(not State.get("root_thread_id")):
				raise RuntimeError("unknown audit session")
			Command.extend(["resume", State["root_thread_id"], f"Continue the same audit after reconciling saved work. Remaining shared wall budget: {max(0, 900-State['active_seconds']):.0f} seconds."])
		else:
			Command.append(PROMPT)
		State = R.supervise(Command, Work, B.environment(Home, Work, Manifest["python"], Manifest["proxy"]), Output, State, Campaign / "control/quota.json", 900)
		State["status"] = "PAUSED" if State.get("stop_reason") else ("RETURNED_UNREVIEWED" if State["exit_code"] == 0 else "INFRA_EXIT")
		R.persist(Output / "sessions.json", R.session_inventory(Home))
		if(State["status"] == "RETURNED_UNREVIEWED"):
			if(any(Path.is_symlink() for Path in Work.rglob("*"))):
				raise RuntimeError("audit freeze requires symlink reconciliation")
			shutil.copytree(Work, Output / "frozen-work")
			R.persist(Output / "frozen-hashes.json", {str(Path.relative_to(Work)): R.file_hash(Path) for Path in Work.rglob("*") if Path.is_file()})
		R.persist(StatePath, State)
		print(json.dumps(dict(mapping=str(MapPath), state=State)))


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("--campaign", required=True)
	Parser.add_argument("--task", required=True, choices=["t1", "t2"])
	Parser.add_argument("--arm", required=True, choices=["A", "B", "C"])
	Parser.add_argument("--project", default=str(B.REPO.parent))
	Parser.add_argument("--prepare-only", action="store_true")
	Parser.add_argument("--resume", action="store_true")
	run(Parser.parse_args())


if(__name__ == "__main__"):
	main()
