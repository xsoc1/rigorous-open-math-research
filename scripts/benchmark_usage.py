#!/usr/bin/env python3
"""Measure returned response usage once across inherited Codex session logs."""

import argparse
import json
from pathlib import Path

import benchmark_runner as R


def collect_records(paths):
	Records, Calls, Models, Efforts = {}, {}, set(), set()
	Duplicates = 0
	for File in paths:
		with Path(File).open(encoding="utf-8") as Stream:
			for Number, Line in enumerate(Stream, 1):
				if(not Line.strip()):
					continue
				Row = json.loads(Line)
				Payload = Row.get("payload", {})
				if(Row.get("type") == "turn_context"):
					if(Payload.get("model")):
						Models.add(Payload["model"])
					if(Payload.get("effort")):
						Efforts.add(Payload["effort"])
				if(Row.get("type") == "response_item" and Payload.get("type") in ["function_call", "custom_tool_call"] and Payload.get("call_id")):
					Calls[Payload["call_id"]] = dict(type=Payload["type"], name=Payload.get("name"), namespace=Payload.get("namespace"))
				if(Row.get("type") != "token_usage_record"):
					continue
				Id = Payload.get("response_id")
				if(not Id or not Payload.get("thread_id") or not isinstance(Payload.get("usage"), dict)):
					raise ValueError("usage record lacks a stable identity or usage")
				Value = dict(thread_id=Payload["thread_id"], usage=Payload["usage"])
				if(Id in Records):
					if(Records[Id]["value"] != Value):
						raise ValueError(f"conflicting usage for {Id}")
					Duplicates += 1
				else:
					Records[Id] = dict(value=Value, origins=[])
				Records[Id]["origins"].append(dict(path=str(File), line=Number))
	return dict(records=Records, duplicate_records=Duplicates, outer_calls=Calls,
		models=sorted(Models), efforts=sorted(Efforts))


def totals(records):
	Fields = ["input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens"]
	Result = {}
	for Field in Fields:
		Values = [Item["value"]["usage"].get(Field) for Item in records]
		if(any(Value is not None and (isinstance(Value, bool) or not isinstance(Value, int) or Value < 0) for Value in Values)):
			raise ValueError("invalid usage counter")
		Result[Field] = sum(Values) if Values and None not in Values else None
	Input, Cached = Result["input_tokens"], Result["cached_input_tokens"]
	if(Input is not None and Cached is not None and Cached > Input):
		raise ValueError("cached input exceeds total input")
	Result["uncached_input_tokens"] = Input - Cached if Input is not None and Cached is not None else None
	Result["responses_with_usage"] = len(records)
	return Result


def measure(base):
	Base = Path(base)
	State = R.read_json(Base / "run/state.json")
	Data = collect_records(sorted((Base / "home/sessions").glob("**/*.jsonl")))
	ByThread = {}
	for Item in Data["records"].values():
		ByThread.setdefault(Item["value"]["thread_id"], []).append(Item)
	Commands = 0
	for Segment in (Base / "run").glob("segment-*/events.jsonl"):
		Ids = set()
		for Line in Segment.read_text().splitlines():
			Event = json.loads(Line)
			Item = Event.get("item", {})
			if(Event.get("type") == "item.completed" and Item.get("type") == "command_execution"):
				Ids.add(Item["id"])
		Commands += len(Ids)
	Summary = dict(schema_version=1, status=State["status"],
		root_thread_id=State.get("root_thread_id"), models=Data["models"], efforts=Data["efforts"],
		root_active_wall_seconds=State["active_seconds"], aggregate_active_wall_seconds=None,
		returned_usage=totals(list(Data["records"].values())),
		per_thread={Id: totals(Items) for Id, Items in ByThread.items()},
		duplicate_usage_records_removed=Data["duplicate_records"],
		outer_model_tool_calls=len(Data["outer_calls"]), root_cli_command_executions=Commands,
		all_actual_tool_calls=None,
		coverage="Returned response usage only. Unknown in-flight usage is not zero. Outer calls and CLI commands are distinct scopes; aggregate active time and complete nested tool counts remain unknown.")
	R.persist(Base / "run/usage-records.json", Data)
	R.persist(Base / "run/usage-summary.json", Summary)
	return Summary


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("base")
	Args = Parser.parse_args()
	print(json.dumps(measure(Args.base)))


if(__name__ == "__main__"):
	main()
