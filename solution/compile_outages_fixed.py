#!/usr/bin/env python3
"""Repaired outage window compiler."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SEVERITY_RANK = {"minor": 1, "major": 2, "critical": 3}
PRIORITY_ORDER = ("critical", "high", "medium")
MAINTENANCE_PATH = Path("/app/data/maintenance_windows.json")


def load_outages(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def load_maintenance(path: Path = MAINTENANCE_PATH) -> list[dict]:
    return json.loads(path.read_text())


def normalize_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def canonicalize(rows: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for row in rows:
        normalized = dict(row)
        normalized["service"] = str(normalized.get("service", "")).strip().lower()
        normalized["severity"] = str(normalized.get("severity", "")).strip().lower()
        normalized["planned"] = normalize_bool(normalized.get("planned", False))
        incident_id = str(normalized["incident_id"])
        current = deduped.get(incident_id)
        if current is None or normalized["end_ms"] > current["end_ms"]:
            deduped[incident_id] = normalized
    return sorted(
        deduped.values(),
        key=lambda row: (row["service"], row["start_ms"], str(row["incident_id"])),
    )


def overlap_ms(start_a: int, end_a: int, start_b: int, end_b: int) -> int:
    return max(0, min(end_a, end_b) - max(start_a, start_b))


def maintenance_by_service(maintenance_rows: list[dict]) -> dict[str, list[tuple[int, int]]]:
    by_service: dict[str, list[tuple[int, int]]] = {}
    for row in maintenance_rows:
        service = str(row.get("service", "")).strip().lower()
        by_service.setdefault(service, []).append((int(row["start_ms"]), int(row["end_ms"])))
    return by_service


def merge_windows(
    canonical_rows: list[dict], maintenance_rows: list[dict]
) -> tuple[dict[str, list[dict]], int]:
    by_service: dict[str, list[dict]] = {}
    planned_excluded_count = 0
    for row in canonical_rows:
        if row["planned"]:
            planned_excluded_count += 1
            continue
        by_service.setdefault(row["service"], []).append(row)

    maintenance = maintenance_by_service(maintenance_rows)
    windows: dict[str, list[dict]] = {}
    for service in sorted(by_service):
        rows = sorted(by_service[service], key=lambda row: row["start_ms"])
        merged: list[dict] = []
        for row in rows:
            if not merged:
                merged.append(
                    {
                        "start_ms": row["start_ms"],
                        "end_ms": row["end_ms"],
                        "incident_count": 1,
                        "source_incident_ids": [str(row["incident_id"])],
                        "max_severity": row["severity"],
                    }
                )
                continue

            prev = merged[-1]
            if row["start_ms"] <= prev["end_ms"]:
                prev["end_ms"] = max(prev["end_ms"], row["end_ms"])
                prev["incident_count"] += 1
                incident_id = str(row["incident_id"])
                if incident_id not in prev["source_incident_ids"]:
                    prev["source_incident_ids"].append(incident_id)
                if SEVERITY_RANK[row["severity"]] > SEVERITY_RANK[prev["max_severity"]]:
                    prev["max_severity"] = row["severity"]
            else:
                merged.append(
                    {
                        "start_ms": row["start_ms"],
                        "end_ms": row["end_ms"],
                        "incident_count": 1,
                        "source_incident_ids": [str(row["incident_id"])],
                        "max_severity": row["severity"],
                    }
                )

        for block in merged:
            block["duration_ms"] = block["end_ms"] - block["start_ms"]
            block["source_incident_ids"] = sorted(block["source_incident_ids"])
            overlap_total = 0
            for start, end in maintenance.get(service, []):
                overlap_total += overlap_ms(block["start_ms"], block["end_ms"], start, end)
            block["maintenance_overlap_ms"] = overlap_total
            block["billable_duration_ms"] = max(block["duration_ms"] - overlap_total, 0)

        windows[service] = merged

    return windows, planned_excluded_count


def build_queue(windows: dict[str, list[dict]]) -> list[dict]:
    rows: list[dict] = []
    for service, blocks in windows.items():
        for block in blocks:
            if block["billable_duration_ms"] < 250:
                continue
            if (
                block["max_severity"] == "critical" and block["billable_duration_ms"] >= 300
            ) or block["billable_duration_ms"] >= 700:
                priority = "critical"
            elif block["billable_duration_ms"] >= 350 or (
                block["incident_count"] >= 3 and block["max_severity"] in {"major", "critical"}
            ):
                priority = "high"
            else:
                priority = "medium"
            incident_ids_csv = ",".join(block["source_incident_ids"])
            signature = hashlib.sha1(
                f"{service}|{block['start_ms']}|{block['end_ms']}|{incident_ids_csv}".encode(
                    "utf-8"
                )
            ).hexdigest()[:12]
            rows.append(
                {
                    "window_id": f"{service}:{block['start_ms']}-{block['end_ms']}",
                    "service": service,
                    "start_ms": block["start_ms"],
                    "end_ms": block["end_ms"],
                    "duration_ms": block["duration_ms"],
                    "maintenance_overlap_ms": block["maintenance_overlap_ms"],
                    "billable_duration_ms": block["billable_duration_ms"],
                    "incident_count": block["incident_count"],
                    "source_incident_ids": block["source_incident_ids"],
                    "max_severity": block["max_severity"],
                    "priority": priority,
                    "outage_signature": signature,
                }
            )

    rank = {name: idx for idx, name in enumerate(PRIORITY_ORDER)}
    rows.sort(
        key=lambda row: (
            rank[row["priority"]],
            -row["billable_duration_ms"],
            -row["incident_count"],
            row["service"],
            row["start_ms"],
        )
    )
    return rows


def build_summary(
    raw_rows: list[dict],
    canonical_rows: list[dict],
    windows: dict[str, list[dict]],
    queue: list[dict],
    planned_excluded_count: int,
) -> dict:
    severity_counts = {"critical": 0, "major": 0, "minor": 0}
    for row in canonical_rows:
        severity = row["severity"]
        if severity in severity_counts:
            severity_counts[severity] += 1

    total_unplanned_downtime_ms = sum(
        block["duration_ms"] for blocks in windows.values() for block in blocks
    )
    total_maintenance_overlap_ms = sum(
        block["maintenance_overlap_ms"] for blocks in windows.values() for block in blocks
    )
    total_billable_downtime_ms = sum(
        block["billable_duration_ms"] for blocks in windows.values() for block in blocks
    )
    longest_window_ms = max(
        (block["duration_ms"] for blocks in windows.values() for block in blocks),
        default=0,
    )
    queue_signature_checksum = hashlib.sha256(
        "|".join(row["outage_signature"] for row in queue).encode("utf-8")
    ).hexdigest()

    return {
        "schema_version": "outage-windows-v1",
        "raw_incident_count": len(raw_rows),
        "unique_incident_ids": len({str(row["incident_id"]) for row in raw_rows}),
        "canonical_incident_count": len(canonical_rows),
        "service_count": len(windows),
        "severity_counts": severity_counts,
        "total_unplanned_downtime_ms": total_unplanned_downtime_ms,
        "total_maintenance_overlap_ms": total_maintenance_overlap_ms,
        "total_billable_downtime_ms": total_billable_downtime_ms,
        "longest_window_ms": longest_window_ms,
        "queued_window_count": len(queue),
        "planned_excluded_count": planned_excluded_count,
        "queue_signature_checksum": queue_signature_checksum,
    }


def write_outputs(
    output_dir: Path,
    summary: dict,
    windows: dict[str, list[dict]],
    queue: list[dict],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "downtime_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output_dir / "service_windows.json").write_text(json.dumps(windows, indent=2) + "\n")
    with (output_dir / "incident_queue.jsonl").open("w", encoding="utf-8") as handle:
        for row in queue:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")


def compile_outages(input_path: Path, output_dir: Path) -> None:
    raw_rows = load_outages(input_path)
    maintenance_rows = load_maintenance()
    canonical_rows = canonicalize(raw_rows)
    windows, planned_excluded_count = merge_windows(canonical_rows, maintenance_rows)
    queue = build_queue(windows)
    summary = build_summary(
        raw_rows=raw_rows,
        canonical_rows=canonical_rows,
        windows=windows,
        queue=queue,
        planned_excluded_count=planned_excluded_count,
    )
    write_outputs(output_dir=output_dir, summary=summary, windows=windows, queue=queue)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/app/data/outages.json")
    parser.add_argument("--output-dir", default="/app/output")
    args = parser.parse_args()

    compile_outages(input_path=Path(args.input), output_dir=Path(args.output_dir))
    print(f"Wrote report to {args.output_dir}")


if __name__ == "__main__":
    main()
