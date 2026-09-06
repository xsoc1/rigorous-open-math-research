"""Deterministic runner interruption checks; these never invoke a model."""

from datetime import datetime, timedelta, timezone
import fcntl
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

import benchmark_runner as R


class RunnerTests(unittest.TestCase):
	def test_quota_reserve_and_staleness(self):
		with tempfile.TemporaryDirectory() as Directory:
			Path = R.Path(Directory) / "quota.json"
			Data = dict(captured_at=R.utc_now(), five_hour_remaining=34, weekly_remaining=30)
			R.persist(Path, Data)
			self.assertEqual(R.quota_reason(Path, launching=True), "QUOTA_RESERVE")
			self.assertIsNone(R.quota_reason(Path))
			Data["captured_at"] = (datetime.now(timezone.utc) - timedelta(seconds=301)).isoformat()
			R.persist(Path, Data)
			self.assertEqual(R.quota_reason(Path), "QUOTA_SNAPSHOT_STALE")

	def test_stop_retains_work_and_remaining_budget(self):
		with tempfile.TemporaryDirectory() as Directory:
			Root = Path(Directory)
			Quota = Root / "quota.json"
			R.persist(Quota, dict(captured_at=R.utc_now(), five_hour_remaining=90, weekly_remaining=90))
			Script = Root / "fake.py"
			Script.write_text("import json,pathlib,time\nprint(json.dumps({'type':'thread.started','thread_id':'synthetic-test'}),flush=True)\npathlib.Path('retained.txt').write_text('partial')\npathlib.Path('STOP').touch()\ntime.sleep(30)\n")
			State = R.supervise([sys.executable, str(Script)], Root, {}, Root, {}, Quota, 5)
			self.assertEqual(State["stop_reason"], "COORDINATOR_STOP")
			self.assertEqual(State["root_thread_id"], "synthetic-test")
			self.assertEqual((Root / "retained.txt").read_text(), "partial")
			First = State["active_seconds"]
			(Root / "STOP").unlink()
			State = R.supervise([sys.executable, "-c", "print('continued')"], Root, {}, Root, State, Quota, 5)
			self.assertGreater(State["active_seconds"], First)
			self.assertEqual(len(State["segments"]), 2)
			self.assertEqual((Root / "retained.txt").read_text(), "partial")
			self.assertTrue((Root / "segment-01/events.jsonl").exists())
			with self.assertRaises(RuntimeError):
				R.supervise([sys.executable, "-c", "pass"], Root, {}, Root, State, Quota, First)

	def test_lock_excludes_duplicate_dispatch(self):
		with tempfile.TemporaryDirectory() as Directory:
			with (Path(Directory) / "lock").open("a") as First, (Path(Directory) / "lock").open("a") as Second:
				fcntl.flock(First, fcntl.LOCK_EX | fcntl.LOCK_NB)
				with self.assertRaises(BlockingIOError):
					fcntl.flock(Second, fcntl.LOCK_EX | fcntl.LOCK_NB)

	def test_missing_usage_is_unknown(self):
		with tempfile.TemporaryDirectory() as Directory:
			Root = Path(Directory)
			(Root / "sessions").mkdir()
			Rows = [dict(type="session_meta", payload=dict(id="synthetic-test", source="cli")),
				dict(type="turn_context", payload=dict(model="gpt-6-astra", effort="max")),
				dict(type="response_item", payload=dict(type="function_call", call_id="call-1"))]
			Rows.append(Rows[-1])
			(Root / "sessions/test.jsonl").write_text("\n".join(json.dumps(Row) for Row in Rows))
			Data = R.session_inventory(Root)[0]
			self.assertIsNone(Data["token_usage"])
			self.assertEqual(Data["outer_tool_calls"], 1)
			self.assertIsNone(Data["response_count"])


if(__name__ == "__main__"):
	unittest.main()
