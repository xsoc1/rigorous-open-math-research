import json
from pathlib import Path
import tempfile
import unittest

import benchmark_usage as U


class UsageTests(unittest.TestCase):
	def test_inherited_records_are_counted_once(self):
		with tempfile.TemporaryDirectory() as Directory:
			Root = Path(Directory)
			Parent = dict(type="token_usage_record", payload=dict(response_id="response-parent", thread_id="parent", usage=dict(input_tokens=100, cached_input_tokens=60, output_tokens=20, reasoning_output_tokens=10)))
			Child = dict(type="token_usage_record", payload=dict(response_id="response-child", thread_id="child", usage=dict(input_tokens=150, cached_input_tokens=80, output_tokens=30, reasoning_output_tokens=20)))
			(Root / "parent.jsonl").write_text(json.dumps(Parent) + "\n")
			(Root / "child.jsonl").write_text(json.dumps(Parent) + "\n" + json.dumps(Child) + "\n")
			Data = U.collect_records(Root.glob("*.jsonl"))
			self.assertEqual(Data["duplicate_records"], 1)
			Totals = U.totals(list(Data["records"].values()))
			self.assertEqual(Totals["uncached_input_tokens"], 110)
			self.assertEqual(Totals["output_tokens"], 50)
			self.assertEqual(Totals["responses_with_usage"], 2)

	def test_conflicting_duplicate_is_rejected(self):
		with tempfile.TemporaryDirectory() as Directory:
			Path = U.Path(Directory) / "records.jsonl"
			Rows = [dict(type="token_usage_record", payload=dict(response_id="same", thread_id="parent", usage=dict(input_tokens=Value))) for Value in [100, 101]]
			Path.write_text("\n".join(json.dumps(Row) for Row in Rows))
			with self.assertRaises(ValueError):
				U.collect_records([Path])
		self.assertIsNone(U.totals([])["input_tokens"])


if(__name__ == "__main__"):
	unittest.main()
