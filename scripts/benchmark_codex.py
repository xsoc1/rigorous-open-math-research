#!/usr/bin/env python3
"""Prepare and inspect isolated Codex regression arms without running a solver."""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

REPO = Path(__file__).resolve().parents[1]
BASELINE = "516037f14f340107da8448b6e42df17317d9fc63"
CANDIDATE = "6d6d739645981a5a2970b5faa26adda49a724113"
COMMON = """Solve the task below using only its statement, this workspace, and your available tools.
Do not inspect other projects, prior solutions, sessions, memory or internet sources.
Available subagents may be used within the configured limit; their work shares your wall budget.
Retain substantive completed work on disk as you proceed. Deliver a self-contained proof or
the strongest exact partial result with its precise remaining gap in answer.md and your final reply.
Distinguish proof, conjecture and numerical evidence. State external theorems and check hypotheses.
Your entire run, including internal audits and child agents, has a 30 minute wall limit.
Begin final consolidation by minute 25. Do not initiate further research after completing the task.
"""
FEATURES_OFF = ["apps", "browser_use", "browser_use_external", "browser_use_full_cdp_access",
	"computer_use", "image_generation", "in_app_browser", "recommended_plugins", "remote_plugin",
	"hooks", "goals", "workspace_dependencies", "skill_search", "memories", "code_mode_host",
	"local_thread_store_compression", "local_thread_store_shared_compression"]


def sha256(data):
	return hashlib.sha256(data).hexdigest()


def write_text(path, text):
	Path(path).parent.mkdir(parents=True, exist_ok=True)
	Path(path).write_text(text, encoding="utf-8", newline="\n")


def write_json(path, data):
	write_text(path, json.dumps(data, ensure_ascii=False, indent="\t") + "\n")


def arm_paths(root, task, arm):
	Base = root / task / arm.lower()
	return Base, Base / "home", Base / "work"


def environment(home, work, python=None, proxy="http://127.0.0.1:7897"):
	Env = os.environ.copy()
	for Key in list(Env):
		if(Key.startswith("CODEX_") or Key in ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_ORG_ID"]):
			Env.pop(Key)
	Env.update(CODEX_HOME=str(home), CODEX_PERMISSION_PROFILE="benchmark", PYTHONUTF8="1",
		PYTHONDONTWRITEBYTECODE="1", TEMP=str(work / "tmp"), TMP=str(work / "tmp"),
		HTTP_PROXY=proxy, HTTPS_PROXY=proxy, ALL_PROXY=proxy,
		http_proxy=proxy, https_proxy=proxy, all_proxy=proxy,
		NO_PROXY="127.0.0.1,localhost")
	if(python):
		Env.update(PYTHON_EXECUTABLE=str(python), PATH=str(Path(python).parent) + os.pathsep + Env.get("PATH", ""))
	return Env


def command(args, cwd, env=None, timeout=90):
	Result = subprocess.run([str(Item) for Item in args], cwd=cwd, env=env,
		capture_output=True, timeout=timeout)
	if(Result.returncode):
		raise RuntimeError(f"command failed ({Result.returncode}): {Result.stderr.decode('utf-8', 'replace')[-2000:]}")
	return Result.stdout


def configure(home, work, binary, plugins, python, auth_source=None):
	SystemPaths = ["C:/Windows", "C:/Program Files"] if os.name == "nt" else ["/usr", "/bin", "/lib", "/lib64", "/etc", "/dev"]
	ReadPaths = [*SystemPaths, str(binary.parent).replace("\\", "/"),
		str(Path(python).parent).replace("\\", "/"), (home / "plugins").as_posix(),
		(home / "skills").as_posix()]
	Rows = [
		'model = "gpt-6-astra"', 'model_reasoning_effort = "max"', 'approval_policy = "never"',
		'default_permissions = "benchmark"', 'project_doc_max_bytes = 0', 'web_search = "disabled"',
		'allow_login_shell = false', 'cli_auth_credentials_store = "file"',
		'[windows]', 'sandbox = "elevated"',
		'[permissions.benchmark.filesystem]', '":minimal" = "read"', '":workspace_roots" = "write"',
	]
	Rows.extend(json.dumps(Path, ensure_ascii=False) + ' = "read"' for Path in ReadPaths)
	Campaign = work.parents[2]
	OriginalHome = Path(auth_source).parent if auth_source else Path.home() / ".codex"
	Denied = [REPO.parent, OriginalHome, Path.home() / ".codex", Campaign / "control",
		home / "auth.json", home / "sessions"]
	Denied.extend(Path for Path in Campaign.parent.iterdir() if Path.is_dir() and Path != Campaign)
	Denied.extend(Campaign / Task / Arm for Task in ["t1", "t2"] for Arm in ["a", "b", "c"]
		if Campaign / Task / Arm != work.parent)
	Rows.extend(json.dumps(Path.as_posix()) + ' = "deny"' for Path in dict.fromkeys(Denied))
	Rows.extend(['[permissions.benchmark.network]', 'enabled = false',
		'[agents]', 'enabled = true', 'default_subagent_model = "gpt-6-astra"',
		'default_subagent_reasoning_effort = "max"', 'max_concurrent_threads_per_session = 3',
		'[memories]', 'use_memories = false', 'generate_memories = false',
		'[features]', 'multi_agent = true', 'skip_host_skill_discovery = true',
		'plugins = ' + str(plugins).lower(), 'plugin_sharing = false'])
	Rows.extend(Key + " = false" for Key in FEATURES_OFF)
	Rows.extend(['[projects.' + json.dumps(work.as_posix()) + ']', 'trust_level = "trusted"'])
	write_text(home / "config.toml", "\n".join(Rows) + "\n")


def prepare(args):
	Root = Path(args.root).resolve()
	ManifestPath = Root / "control/manifest.json"
	if(ManifestPath.exists()):
		raise FileExistsError("prepared campaign already exists; inspect it instead of reinitializing")
	Binary = Path(args.binary or shutil.which("codex")).resolve()
	Source = Path(args.project).resolve()
	TaskPaths = dict(t1=Source / "runs/plugin-benchmark-20260824-calibration/frozen_task.md",
		t2=Source / "runs/three-arm-pilot-v2/pilot-v5-codex-u2/frozen_task.md")
	Snapshots = dict()
	for Arm, Commit in [("A", BASELINE), ("B", CANDIDATE)]:
		Archive = command(["git", "archive", "--format=zip", Commit, "plugins", ".agents/plugins/marketplace.json"], REPO)
		Snapshot = Root / "control" / ("snapshot-" + Arm.lower())
		Snapshot.mkdir(parents=True, exist_ok=False)
		with zipfile.ZipFile(io.BytesIO(Archive)) as Zip:
			Zip.extractall(Snapshot)
		Snapshots[Arm] = Snapshot
	Manifest = dict(schema_version=1, kind="REGRESSION_NOT_NOVELTY", root=str(Root),
		binary=str(Binary), binary_sha256=sha256(Binary.read_bytes()),
		python=str(Path(args.python).resolve()), python_sha256=sha256(Path(args.python).read_bytes()),
		proxy=args.proxy, platform=sys.platform,
		cli_version=command([Binary, "--version"], REPO).decode().strip(),
		model="gpt-6-astra", effort="max", arm_commits=dict(A=BASELINE, B=CANDIDATE, C=None),
		schedule=dict(t1=["C", "A", "B"], t2=["B", "A", "C"]), arms=[], tasks=dict())
	for Task, TaskPath in TaskPaths.items():
		TaskBytes = TaskPath.read_bytes()
		Manifest["tasks"][Task] = dict(source=str(TaskPath), sha256=sha256(TaskBytes))
		for Arm in ("A", "B", "C"):
			Base, Home, Work = arm_paths(Root, Task, Arm)
			Home.mkdir(parents=True, exist_ok=False)
			(Work / "tmp").mkdir(parents=True, exist_ok=False)
			(Work / "TASK.md").write_bytes(TaskBytes)
			Prefix = "Use the installed math-research-workflow skill and its research dependencies for this task.\n" if Arm != "C" else ""
			write_text(Work / "PROMPT.md", Prefix + COMMON + "\n" + TaskBytes.decode("utf-8-sig"))
			configure(Home, Work, Binary, Arm != "C", args.python, args.auth_source)
			shutil.copyfile(args.auth_source, Home / "auth.json")
			(Home / "auth.json").chmod(0o600)
			Env = environment(Home, Work, args.python, args.proxy)
			if(Arm != "C"):
				command([Binary, "plugin", "marketplace", "add", Snapshots[Arm]], Work, Env)
				for Plugin in ["math-research-workflow", "rigorous-open-math-research", "manage-math-research-program", "lean-verify"]:
					command([Binary, "plugin", "add", Plugin + "@math-research", "--json"], Work, Env)
			Manifest["arms"].append(dict(task=Task, arm=Arm, base=str(Base), home=str(Home), work=str(Work),
				prompt_sha256=sha256((Work / "PROMPT.md").read_bytes()), config_sha256=sha256((Home / "config.toml").read_bytes())))
	write_json(ManifestPath, Manifest)
	print(json.dumps(dict(verdict="PREPARED", manifest=str(ManifestPath), arms=len(Manifest["arms"]))))


def probe(args):
	Root = Path(args.root).resolve()
	Manifest = json.loads((Root / "control/manifest.json").read_text(encoding="utf-8"))
	Binary = Path(Manifest["binary"])
	Base, Home, Work = arm_paths(Root, args.task, args.arm)
	Env = environment(Home, Work, Manifest["python"], Manifest.get("proxy", "http://127.0.0.1:7897"))
	Number = 1
	Output = Base / f"preflight-{Number:02d}"
	while(Output.exists()):
		Number += 1
		Output = Base / f"preflight-{Number:02d}"
	Output.mkdir(exist_ok=False)
	Prompt = command([Binary, "-C", Work, "debug", "prompt-input", "PREFLIGHT_ONLY_NO_MATHEMATICS"], Work, Env)
	(Output / "prompt-input.json").write_bytes(Prompt)
	Decoded = Prompt.decode("utf-8")
	Input = json.loads(Decoded)
	Canary = Root / "control/foreign-canary.txt"
	write_text(Canary, "THIS_FILE_MUST_BE_UNREADABLE_TO_THE_SOLVER\n")
	Check = Work / "sandbox_probe.py"
	write_text(Check, """import json, pathlib, socket
result = {}
try:
 pathlib.Path('sandbox-write.txt').write_text('writable', encoding='utf-8')
 result['workspace_write'] = True
except OSError:
 result['workspace_write'] = False
for name, path in """ + repr(dict(foreign=str(Canary), project=str(Path(args.project) / "AGENTS.md"),
		auth=str(Home / "auth.json"))) + """.items():
 try:
  pathlib.Path(path).read_bytes()
  result[name + '_read_blocked'] = False
 except OSError:
  result[name + '_read_blocked'] = True
try:
 socket.create_connection(('1.1.1.1', 443), timeout=2).close()
 result['network_blocked'] = False
except OSError:
 result['network_blocked'] = True
print(json.dumps(result))
""".replace("\n ", "\n\t"))
	Raw = command([Binary, "sandbox", "-P", "benchmark", "-C", Work, Manifest["python"], Check], Work, Env)
	(Output / "sandbox.json").write_bytes(Raw)
	Checks = json.loads(Raw.decode("utf-8"))
	Checks.update(prompt_items=len(Input), prompt_bytes=len(Prompt),
		workflow_visible="math-research-workflow" in Decoded,
		legacy_project_visible="KP-DET" in Decoded or "Q_quad" in Decoded,
		foreign_session_visible="01a06f46-dd03-7c83-9267-32048412c359" in Decoded)
	Checks["verdict"] = "PASS" if all(Checks[Key] for Key in ["workspace_write", "foreign_read_blocked",
		"project_read_blocked", "auth_read_blocked", "network_blocked"]) and not Checks["legacy_project_visible"] and not Checks["foreign_session_visible"] and Checks["workflow_visible"] == (args.arm != "C") else "FAIL"
	write_json(Output / "summary.json", Checks)
	print(json.dumps(Checks))
	if(Checks["verdict"] != "PASS"):
		raise RuntimeError("preflight failed; no scored solver may start")


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("action", choices=["prepare", "probe"])
	Parser.add_argument("--root", required=True)
	Parser.add_argument("--project", required=True)
	Parser.add_argument("--task", choices=["t1", "t2"], default="t1")
	Parser.add_argument("--arm", choices=["A", "B", "C"], default="C")
	Parser.add_argument("--python", default=sys.executable)
	Parser.add_argument("--binary")
	Parser.add_argument("--auth-source", default=str(Path.home() / ".codex/auth.json"))
	Parser.add_argument("--proxy", default="http://127.0.0.1:7897")
	Args = Parser.parse_args()
	(prepare if Args.action == "prepare" else probe)(Args)


if(__name__ == "__main__"):
	main()
