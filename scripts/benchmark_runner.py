#!/usr/bin/env python3
"""Linux-only bounded, resumable runner for the preregistered Codex benchmark."""

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time

import benchmark_codex as B


def read_json(path):
	return json.loads(Path(path).read_text(encoding="utf-8"))


def persist(path, value):
	Path = path.with_suffix(".tmp")
	with Path.open("w", encoding="utf-8", newline="\n") as Stream:
		json.dump(value, Stream, ensure_ascii=False, indent="\t")
		Stream.write("\n")
		Stream.flush()
		os.fsync(Stream.fileno())
	os.replace(Path, path)


def utc_now():
	return datetime.now(timezone.utc).isoformat()


def file_hash(path):
	with Path(path).open("rb") as Stream:
		Digest = hashlib.sha256()
		for Chunk in iter(lambda: Stream.read(1048576), b""):
			Digest.update(Chunk)
	return Digest.hexdigest()


def quota_reason(path, launching=False):
	try:
		Quota = read_json(path)
		Age = (datetime.now(timezone.utc) - datetime.fromisoformat(Quota["captured_at"])).total_seconds()
		if(Age < 0 or Age > (120 if launching else 300)):
			return "QUOTA_SNAPSHOT_STALE"
		if(Quota["five_hour_remaining"] < (35 if launching else 25) or Quota["weekly_remaining"] < 25):
			return "QUOTA_RESERVE"
	except (OSError, ValueError, KeyError, TypeError):
		return "QUOTA_UNKNOWN"
	return None


def session_inventory(home):
	Sessions = []
	for Path in sorted((home / "sessions").glob("**/*.jsonl")):
		Meta, Usage, Models, Efforts, Calls = {}, None, set(), set(), set()
		with Path.open(encoding="utf-8") as Stream:
			for Line in Stream:
				try:
					Row = json.loads(Line)
					Payload = Row.get("payload", {})
					if(Row.get("type") == "session_meta"):
						Meta = Payload
					elif(Row.get("type") == "turn_context"):
						if(Payload.get("model")):
							Models.add(Payload["model"])
						if(Payload.get("effort", Payload.get("reasoning_effort"))):
							Efforts.add(Payload.get("effort", Payload.get("reasoning_effort")))
					elif(Row.get("type") == "event_msg" and Payload.get("type") == "token_count"):
						Info = Payload.get("info") or {}
						if(Info.get("total_token_usage") is not None):
							Usage = Info["total_token_usage"]
					elif(Row.get("type") == "response_item" and Payload.get("type") in ["function_call", "custom_tool_call"]):
						Calls.add(Payload.get("call_id") or Payload.get("id") or Line)
				except (json.JSONDecodeError, TypeError):
					continue
		Sessions.append(dict(id=Meta.get("id"), source=Meta.get("source"), path=str(Path),
			models=sorted(Models), efforts=sorted(Efforts), token_usage=Usage,
			token_usage_scope="FILE_CUMULATIVE_UNDEDUPLICATED",
			outer_tool_calls=len(Calls), response_count=None, aggregate_active_seconds=None))
	return Sessions


def assert_sealed(root, task, arm):
	ManifestPath = root / "control/manifest.json"
	Manifest = read_json(ManifestPath)
	Seal = read_json(root / "control/SEALED.json")
	if(file_hash(__file__) != Seal["runner_sha256"] or file_hash(B.__file__) != Seal["preparation_sha256"]):
		raise RuntimeError("runner changed after seal")
	if(Seal["manifest_sha256"] != file_hash(ManifestPath) or task not in Seal["tasks"]):
		raise RuntimeError("unsealed task or changed manifest")
	if(Manifest["platform"] != "linux" or file_hash(Manifest["binary"]) != Manifest["binary_sha256"]):
		raise RuntimeError("wrong platform or changed CLI")
	if(file_hash(root / "control/model-catalog.json") != Manifest["model_catalog_sha256"] or file_hash(Manifest["python"]) != Manifest["python_sha256"]):
		raise RuntimeError("changed catalog or Python")
	if(file_hash(Path(Manifest["binary"]).parent / "codex-code-mode-host") != Manifest["code_mode_host_sha256"]):
		raise RuntimeError("changed code-mode host")
	Base, Home, Work = B.arm_paths(root, task, arm)
	Binding = next(Item for Item in Manifest["arms"] if Item["task"] == task and Item["arm"] == arm)
	for File, Key in [(Home / "config.toml", "config_sha256"), (Work / "PROMPT.md", "prompt_sha256")]:
		if(file_hash(File) != Binding[Key]):
			raise RuntimeError("changed arm config or prompt")
	Gates = Seal["tasks"][task][arm]
	if(len(Gates) != 2 or {Gate["kind"] for Gate in Gates} != {"filesystem", "tools"}):
		raise RuntimeError("incomplete gate set")
	for Gate in Gates:
		File = Path(Gate["path"])
		Data = read_json(File)
		if(file_hash(File) != Gate["sha256"] or Data["verdict"] != "PASS" or Data["config_sha256"] != Binding["config_sha256"]):
			raise RuntimeError("failed or stale preflight")
		if(Gate["kind"] == "tools" and (not Data.get("operational_checks") or not all(Data["operational_checks"].values()) or not Data.get("resume_same_session"))):
			raise RuntimeError("tool execution and resume must pass, not just schemas")
	return Manifest, Base, Home, Work


def process_identity(pid):
	try:
		Fields = Path(f"/proc/{pid}/stat").read_text().rsplit(") ", 1)[1].split()
		return int(Fields[1]), Fields[19]
	except (OSError, ValueError, IndexError):
		return None


def descendants(pid):
	Processes = {int(Item.name): process_identity(int(Item.name)) for Item in Path("/proc").iterdir() if Item.name.isdigit()}
	Owned = {pid}
	while(True):
		Expanded = Owned | {Pid for Pid, Identity in Processes.items() if Identity and Identity[0] in Owned}
		if(Expanded == Owned):
			break
		Owned = Expanded
	return {Pid: Processes[Pid][1] for Pid in Owned - {pid} if Processes.get(Pid)}


def retain_thread_id(events, state):
	for Line in events.read_text(encoding="utf-8", errors="replace").splitlines():
		try:
			Event = json.loads(Line)
			if(Event.get("type") == "thread.started"):
				state["root_thread_id"] = Event["thread_id"]
		except (json.JSONDecodeError, KeyError):
			continue


def supervise(command, cwd, env, output, state, quota, budget):
	Previous = state.get("active_seconds", 0)
	if(Previous >= budget):
		raise RuntimeError("active wall budget exhausted")
	Segment = output / f"segment-{len(state.get('segments', [])) + 1:02d}"
	Segment.mkdir(exist_ok=False)
	StatePath = output / "state.json"
	state.update(status="DISPATCH_INTENT", updated_at=utc_now())
	persist(StatePath, state)
	Started = time.monotonic()
	LastInventory = Started
	Reason = None
	with (Segment / "events.jsonl").open("wb") as Events, (Segment / "stderr.txt").open("wb") as Errors:
		Process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
			stdout=Events, stderr=Errors, start_new_session=True)
		state.update(status="RUNNING", runner_pid=os.getpid(), process_pid=Process.pid,
			process_start_ticks=process_identity(Process.pid)[1],
			boot_id=Path("/proc/sys/kernel/random/boot_id").read_text().strip(), current_segment=str(Segment))
		try:
			while(Process.poll() is None):
				state.update(active_seconds=Previous + time.monotonic() - Started, updated_at=utc_now())
				retain_thread_id(Segment / "events.jsonl", state)
				persist(StatePath, state)
				Reason = "WALL_BUDGET" if state["active_seconds"] >= budget else quota_reason(quota)
				if(env.get("CODEX_HOME") and time.monotonic() - LastInventory >= 10):
					Inventory = session_inventory(Path(env["CODEX_HOME"]))
					persist(output / "sessions-live.json", Inventory)
					if(any(set(Item["models"]) - {"gpt-6-astra"} or set(Item["efforts"]) - {"max"} for Item in Inventory)):
						Reason = "MODEL_OR_EFFORT_MISMATCH"
					LastInventory = time.monotonic()
				if((output / "STOP").exists()):
					Reason = "COORDINATOR_STOP"
				if("code-mode host is disabled" in (Segment / "stderr.txt").read_text(encoding="utf-8", errors="replace")):
					Reason = "INFRA_TOOL_RUNTIME"
				if(Reason):
					break
				time.sleep(1)
		finally:
			if(Process.poll() is None):
				Owned = descendants(Process.pid)
				os.killpg(Process.pid, signal.SIGINT)
				try:
					Process.wait(timeout=5)
				except subprocess.TimeoutExpired:
					os.killpg(Process.pid, signal.SIGKILL)
					Process.wait()
				for Pid, Ticks in Owned.items():
					Identity = process_identity(Pid)
					if(Identity and Identity[1] == Ticks):
						try:
							os.kill(Pid, signal.SIGKILL)
						except ProcessLookupError:
							pass
			retain_thread_id(Segment / "events.jsonl", state)
			state.update(active_seconds=Previous + time.monotonic() - Started, updated_at=utc_now(),
				exit_code=Process.returncode, stop_reason=Reason)
			state.setdefault("segments", []).append(dict(path=str(Segment),
				active_seconds=state["active_seconds"] - Previous, exit_code=Process.returncode, stop_reason=Reason))
			state["status"] = "STOPPED" if Reason else "PROCESS_EXITED"
			persist(StatePath, state)
	return state


def run(args):
	Root = Path(args.root).resolve()
	Manifest, Base, Home, Work = assert_sealed(Root, args.task, args.arm)
	Output = Base / "run"
	Output.mkdir(exist_ok=True)
	if((Output / "invalid-attempt.json").exists()):
		raise RuntimeError("invalid attempt is immutable; use its documented replacement")
	with (Root / "control/runner.lock").open("a") as Lock:
		fcntl.flock(Lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
		StatePath = Output / "state.json"
		Existing = read_json(StatePath) if StatePath.exists() else None
		if(args.reconcile):
			if(not Existing):
				raise RuntimeError("no dispatch to reconcile")
			Identity = process_identity(Existing.get("process_pid", 0))
			SameBoot = Existing.get("boot_id") == Path("/proc/sys/kernel/random/boot_id").read_text().strip()
			if(SameBoot and Identity and Identity[1] == Existing.get("process_start_ticks")):
				raise RuntimeError("owned process is still alive")
			persist(Output / "sessions.json", session_inventory(Home))
			if(Existing["status"] in ["RUNNING", "DISPATCH_INTENT", "STOPPED", "PROCESS_EXITED"]):
				Existing.update(status="NO_RETURN", budget_uncertain=True, updated_at=utc_now())
				persist(StatePath, Existing)
			print(json.dumps(Existing))
			return
		if(Existing and not args.resume):
			raise RuntimeError("existing dispatch; reconcile before explicit continuation")
		if(args.resume and (not Existing or Existing["status"] not in ["PAUSED", "INFRA_EXIT", "NO_RETURN"])):
			raise RuntimeError("no reconciled resumable state")
		Reason = quota_reason(Root / "control/quota.json", launching=True)
		if(Reason):
			raise RuntimeError(Reason)
		State = Existing or dict(schema_version=1, dispatch_id=f"{args.task}-{args.arm}",
			created_at=utc_now(), root_thread_id=None, active_seconds=0, segments=[])
		if(args.resume and not State.get("root_thread_id")):
			raise RuntimeError("root session unknown; no automatic replacement")
		if(State.get("budget_uncertain")):
			raise RuntimeError("unobserved active interval requires explicit budget reconciliation")
		if((Output / "STOP").exists()):
			raise RuntimeError("STOP still present; reconcile the stop reason first")
		Command = [Manifest["binary"], "exec", "--strict-config", "--json", "--skip-git-repo-check", "--ignore-rules", "-C", str(Work), "-o", str(Output / "last-message.txt")]
		if(args.resume):
			Remaining = max(0, 1800 - State["active_seconds"])
			Command.extend(["resume", State["root_thread_id"],
				f"Continue the same attempt after interruption. Reconcile returned artifacts before dispatch. The remaining shared wall budget is {Remaining:.0f} seconds. Preserve the original theorem and output contract."])
		else:
			Command.append((Work / "PROMPT.md").read_text(encoding="utf-8"))
		Env = B.environment(Home, Work, Manifest["python"], Manifest["proxy"])
		Env["PATH"] = str(Path(Manifest["binary"]).parent) + os.pathsep + Env["PATH"]
		State = supervise(Command, Work, Env, Output, State, Root / "control/quota.json", 1800)
		Inventory = session_inventory(Home)
		persist(Output / "sessions.json", Inventory)
		Models = {Model for Item in Inventory for Model in Item["models"]}
		Efforts = {Effort for Item in Inventory for Effort in Item["efforts"]}
		State["identity_verdict"] = "PASS" if Models == {Manifest["model"]} and Efforts == {Manifest["effort"]} else "UNKNOWN_OR_MISMATCH"
		if(State["stop_reason"]):
			State["status"] = {"WALL_BUDGET": "BUDGET_EXHAUSTED", "INFRA_TOOL_RUNTIME": "INFRA_EXIT"}.get(State["stop_reason"], "PAUSED")
		elif(State["exit_code"] != 0):
			State["status"] = "INFRA_EXIT"
		else:
			State["status"] = "RETURNED_UNAUDITED"
		if(State["status"] in ["RETURNED_UNAUDITED", "BUDGET_EXHAUSTED"]):
			Frozen = Output / "frozen-work"
			for Item in Work.rglob("*"):
				if(Item.is_symlink()):
					raise RuntimeError("freeze requires explicit symlink reconciliation")
			shutil.copytree(Work, Frozen)
			Hashes = {str(Item.relative_to(Frozen)): file_hash(Item) for Item in Frozen.rglob("*") if Item.is_file()}
			if((Output / "last-message.txt").exists()):
				Hashes["../last-message.txt"] = file_hash(Output / "last-message.txt")
			persist(Output / "frozen-hashes.json", Hashes)
		persist(StatePath, State)
		print(json.dumps(State))


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("--root", required=True)
	Parser.add_argument("--task", choices=["t1", "t2"], required=True)
	Parser.add_argument("--arm", choices=["A", "B", "C"], required=True)
	Parser.add_argument("--resume", action="store_true")
	Parser.add_argument("--reconcile", action="store_true")
	run(Parser.parse_args())


if(__name__ == "__main__"):
	main()
