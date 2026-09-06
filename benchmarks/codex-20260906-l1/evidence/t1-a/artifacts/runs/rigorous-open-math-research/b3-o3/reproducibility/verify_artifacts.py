#!/usr/bin/env python3
"""Verify the saved proof/audit bindings, not the mathematics itself."""
from pathlib import Path
import datetime
import hashlib
import json

RUN = Path(__file__).resolve().parent.parent
ROOT = RUN.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(reference):
    for base in (RUN, ROOT):
        candidate = (base / reference).resolve()
        if candidate.is_relative_to(ROOT) and candidate.is_file():
            return candidate
    raise AssertionError(f"Missing or unconfined artifact: {reference}")


manifest_path = RUN / "completion_manifest.json"
manifest = json.loads(manifest_path.read_text())
for key in ("contract", "obligation_graph", "candidate_proof"):
    binding = manifest[key]
    assert sha(resolve(binding["path"])) == binding["sha256"], key
for binding in manifest["dependencies"]:
    assert sha(resolve(binding["path"])) == binding["sha256"]

graph = json.loads(resolve(manifest["obligation_graph"]["path"]).read_text())
assert graph["root_obligations"] == manifest["root_obligations"]
assert all(item["status"] == "CLOSED" for item in graph["root_obligations"])

audit = json.loads((RUN / "completion_audit.json").read_text())
assert audit["audited_manifest_sha256"] == sha(manifest_path)
assert audit["candidate_author_id"] == manifest["candidate_author_id"]
assert audit["reviewer_id"] != manifest["candidate_author_id"]
assert audit["verdict"] == "PASS"
assert audit["load_bearing_gaps"] == []
assert audit.get("critical_errors", []) == []
assert datetime.datetime.fromisoformat(audit["reviewed_at"].replace("Z", "+00:00")) >= datetime.datetime.fromisoformat(manifest["frozen_at"].replace("Z", "+00:00"))

candidate = resolve(manifest["candidate_proof"]["path"]).read_text()
answer = (ROOT / "answer.md").read_text()
assert answer.split("\n", 1)[1] == candidate.split("\n", 1)[1]
assert answer.startswith("INDEPENDENTLY_AUDITED_PROOF")
print("PASS: frozen proof/source/contract/obligation hashes, independent audit, and final proof body match.")
print("This is an artifact-integrity check, not Lean or automated mathematical verification.")
