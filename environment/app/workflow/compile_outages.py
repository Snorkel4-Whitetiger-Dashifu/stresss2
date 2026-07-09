#!/usr/bin/env python3
"""Broken outage window compiler used for debugging tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_outages(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def dedupe_incidents(rows: list[dict]) -> list[dict]:
    # BUG: keeps first-seen incident instead of record with highest end_ms.
    deduped: dict[str, dict] = {}
    for row in rows:
        incident_id = str(row["incident_id"])
        if incident_id not in deduped:
            deduped[incident_id] = dict(row)
    return list(deduped.values())


def merge_windows(rows: list[dict]) -> dict[str, list[dict]]:
    by_service: dict[str, list[dict]] = {}
    for row in rows:
        # BUG: service is not normalized.
        service = str(row.get("service", ""))
        by_service.setdefault(service, []).append(dict(row))

    windows: dict[str, list[dict]] = {}
    for service, items in by_service.items():
        # BUG: planned incidents should be excluded before merge.
        items.sort(key=lambda x: x["start_ms"])
        merged: list[dict] = []
        for item in items:
            if not merged:
                merged.append(
                    {
                        "start_ms": item["start_ms"],
                        "end_ms": item["end_ms"],
                        "incident_count": 1,
                        "max_severity": item["severity"],
                    }
                )
                continue
            prev = merged[-1]
            # BUG: touching intervals (==) must merge, this only merges overlap.
            if item["start_ms"] < prev["end_ms"]:
                prev["end_ms"] = max(prev["end_ms"], item["end_ms"])
                prev["incident_count"] += 1
                if item["severity"] == "critical":
                    prev["max_severity"] = "critical"
            else:
                merged.append(
                    {
                        "start_ms": item["start_ms"],
                        "end_ms": item["end_ms"],
                        "incident_count": 1,
                        "max_severity": item["severity"],
                    }
                )
        for block in merged:
            # BUG: duration should be end_ms - start_ms.
            block["duration_ms"] = block["end_ms"] - block["start_ms"] + 1
        windows[service] = merged
    return windows


def build_queue(windows: dict[str, list[dict]]) -> list[dict]:
    queue: list[dict] = []
    for service, blocks in windows.items():
        for block in blocks:
            # BUG: should include windows >= 250, this filters too aggressively.
            if block["duration_ms"] < 500:
                continue
            # BUG: priority rules are incorrect and too coarse.
            priority = "high" if block["max_severity"] == "critical" else "medium"
            queue.append(
                {
                    "window_id": f"{service}:{block['start_ms']}-{block['end_ms']}",
                    "service": service,
                    "start_ms": block["start_ms"],
                    "end_ms": block["end_ms"],
                    "duration_ms": block["duration_ms"],
                    "incident_count": block["incident_count"],
                    "max_severity": block["max_severity"],
                    "priority": priority,
                }
            )
    # BUG: sort order should be priority desc then duration desc.
    queue.sort(key=lambda row: (row["priority"], row["duration_ms"], row["service"]))
    return queue


def build_summary(raw_rows: list[dict], canonical_rows: list[dict], queue: list[dict], windows: dict[str, list[dict]]) -> dict:
    severity_counts = {"critical": 0, "major": 0, "minor": 0}
    for row in canonical_rows:
        sev = str(row.get("severity", ""))
        if sev in severity_counts:
            severity_counts[sev] += 1

    total_downtime = 0
    for blocks in windows.values():
        for block in blocks:
            total_downtime += block["duration_ms"]

    return {
        "schema_version": "outage-windows-v1",
        "raw_incident_count": len(raw_rows),
        "unique_incident_ids": len({str(row["incident_id"]) for row in raw_rows}),
        "canonical_incident_count": len(canonical_rows),
        "service_count": len(windows),
        "severity_counts": severity_counts,
        "total_unplanned_downtime_ms": total_downtime,
        "queued_window_count": len(queue),
        # BUG: planned_excluded_count should count canonical planned incidents.
        "planned_excluded_count": 0,
    }


def write_outputs(output_dir: Path, summary: dict, windows: dict[str, list[dict]], queue: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "downtime_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output_dir / "service_windows.json").write_text(json.dumps(windows, indent=2) + "\n")
    with (output_dir / "incident_queue.jsonl").open("w", encoding="utf-8") as handle:
        for row in queue:
            # BUG: output must be compact JSON lines.
            handle.write(json.dumps(row) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/app/data/outages.json")
    parser.add_argument("--output-dir", default="/app/output")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    raw_rows = load_outages(input_path)
    canonical_rows = dedupe_incidents(raw_rows)
    windows = merge_windows(canonical_rows)
    queue = build_queue(windows)
    summary = build_summary(raw_rows, canonical_rows, queue, windows)
    write_outputs(output_dir, summary, windows, queue)
    print(f"Wrote report to {output_dir}")


if __name__ == "__main__":
    main()
