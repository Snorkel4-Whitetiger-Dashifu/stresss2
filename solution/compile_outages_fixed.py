#!/usr/bin/env python3
"""Repaired outage window compiler."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SEVERITY_RANK = {"minor": 1, "major": 2, "critical": 3}
SEVERITY_ORDER = ("critical", "major", "minor")
PRIORITY_ORDER = ("critical", "high", "medium")
MAINTENANCE_PATH = Path("/app/data/maintenance_windows.json")
POLICY_PATH = Path("/app/data/response_policies.json")
SERVICE_ALIASES = {
    "authentication": "auth",
    "payments": "billing",
    "search-api": "search",
}
DEFAULT_POLICY = {
    "queue_min_effective_ms": 220,
    "critical_p1_min_ms": 280,
    "critical_threshold_ms": 650,
    "high_threshold_ms": 320,
    "no_overlap_high_duration_ms": 450,
    "critical_count_for_critical": 2,
    "no_overlap_bonus": 4,
    "segment_bonus": 1,
    "severity_weight": {"critical": 5, "major": 3, "minor": 1},
    "score_threshold_critical": 34,
    "score_threshold_high": 18,
}


def load_outages(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def load_maintenance(path: Path = MAINTENANCE_PATH) -> list[dict]:
    return json.loads(path.read_text())


def load_policies(path: Path = POLICY_PATH) -> dict:
    return json.loads(path.read_text())


def normalize_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def normalize_service(value: object) -> str:
    normalized = str(value if value is not None else "").strip().lower()
    return SERVICE_ALIASES.get(normalized, normalized)


def normalize_severity(value: object) -> str:
    normalized = str(value if value is not None else "").strip().lower()
    return normalized if normalized in SEVERITY_RANK else "minor"


def normalize_ms(value: object) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def _normalize_policy(raw_policy: dict | None) -> dict:
    raw_policy = raw_policy or {}
    normalized = dict(DEFAULT_POLICY)
    for key in (
        "queue_min_effective_ms",
        "critical_p1_min_ms",
        "critical_threshold_ms",
        "high_threshold_ms",
        "no_overlap_high_duration_ms",
        "critical_count_for_critical",
        "no_overlap_bonus",
        "segment_bonus",
        "score_threshold_critical",
        "score_threshold_high",
    ):
        if key in raw_policy:
            normalized[key] = normalize_ms(raw_policy.get(key))
    raw_weights = raw_policy.get("severity_weight", {})
    if isinstance(raw_weights, dict):
        weights = dict(DEFAULT_POLICY["severity_weight"])
        for severity in ("critical", "major", "minor"):
            if severity in raw_weights:
                weights[severity] = normalize_ms(raw_weights.get(severity))
        normalized["severity_weight"] = weights
    return normalized


def _policy_for_service(service: str, policy_data: dict) -> tuple[str, dict]:
    default_policy = _normalize_policy(policy_data.get("default", {}))
    overrides = policy_data.get("service_overrides", {})
    if not isinstance(overrides, dict):
        return "default", default_policy
    raw_override = overrides.get(service)
    if not isinstance(raw_override, dict):
        return "default", default_policy
    merged = dict(default_policy)
    merged.update(_normalize_policy(raw_override))
    # keep default-provided severity weights when override has partial map
    if "severity_weight" in raw_override:
        merged_weights = dict(default_policy["severity_weight"])
        merged_weights.update(_normalize_policy(raw_override)["severity_weight"])
        merged["severity_weight"] = merged_weights
    return service, merged


def _policy_checksum(policy_data: dict) -> str:
    lines: list[str] = []
    default_policy = _normalize_policy(policy_data.get("default", {}))
    lines.append(
        "default|{queue_min_effective_ms}|{critical_p1_min_ms}|{critical_threshold_ms}|"
        "{high_threshold_ms}|{no_overlap_high_duration_ms}|{critical_count_for_critical}|"
        "{no_overlap_bonus}|{segment_bonus}|{score_threshold_critical}|"
        "{score_threshold_high}|{critical}|{major}|{minor}".format(
            **default_policy, **default_policy["severity_weight"]
        )
    )
    overrides = policy_data.get("service_overrides", {})
    if isinstance(overrides, dict):
        for service in sorted(overrides):
            profile, policy = _policy_for_service(service, policy_data)
            lines.append(
                "{profile}|{queue_min_effective_ms}|{critical_p1_min_ms}|{critical_threshold_ms}|"
                "{high_threshold_ms}|{no_overlap_high_duration_ms}|{critical_count_for_critical}|"
                "{no_overlap_bonus}|{segment_bonus}|{score_threshold_critical}|"
                "{score_threshold_high}|{critical}|{major}|{minor}".format(
                    profile=profile, **policy, **policy["severity_weight"]
                )
            )
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def canonicalize(rows: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for row in rows:
        normalized = dict(row)
        normalized["service"] = normalize_service(normalized.get("service", ""))
        normalized["severity"] = normalize_severity(normalized.get("severity", ""))
        normalized["planned"] = normalize_bool(normalized.get("planned", False))
        normalized["start_ms"] = normalize_ms(normalized.get("start_ms", 0))
        normalized["end_ms"] = normalize_ms(normalized.get("end_ms", 0))
        if normalized["end_ms"] < normalized["start_ms"]:
            normalized["end_ms"] = normalized["start_ms"]
        incident_id = str(normalized["incident_id"])
        current = deduped.get(incident_id)
        if current is None:
            deduped[incident_id] = normalized
            continue
        replace = False
        if normalized["end_ms"] > current["end_ms"]:
            replace = True
        elif normalized["end_ms"] == current["end_ms"]:
            next_rank = SEVERITY_RANK[normalized["severity"]]
            current_rank = SEVERITY_RANK[current["severity"]]
            if next_rank > current_rank:
                replace = True
            elif next_rank == current_rank:
                if current["planned"] and not normalized["planned"]:
                    replace = True
                elif current["planned"] == normalized["planned"]:
                    if normalized["start_ms"] > current["start_ms"]:
                        replace = True
                    elif normalized["start_ms"] == current["start_ms"]:
                        if normalized["service"] > current["service"]:
                            replace = True
        if replace:
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
        service = normalize_service(row.get("service", ""))
        start = normalize_ms(row.get("start_ms", 0))
        end = normalize_ms(row.get("end_ms", 0))
        if end <= start:
            continue
        by_service.setdefault(service, []).append((start, end))
    merged_by_service: dict[str, list[tuple[int, int]]] = {}
    for service in by_service:
        intervals = sorted(by_service[service])
        merged: list[list[int]] = []
        for start, end in intervals:
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
        merged_by_service[service] = [(start, end) for start, end in merged]
    return merged_by_service


def merge_windows(
    canonical_rows: list[dict], maintenance_rows: list[dict]
) -> tuple[dict[str, list[dict]], int, dict[str, list[tuple[int, int]]]]:
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
                        "critical_incident_count": 1 if row["severity"] == "critical" else 0,
                        "source_incident_ids": [str(row["incident_id"])],
                        "max_severity": row["severity"],
                    }
                )
                continue

            prev = merged[-1]
            if row["start_ms"] <= prev["end_ms"] + 30:
                prev["end_ms"] = max(prev["end_ms"], row["end_ms"])
                prev["incident_count"] += 1
                if row["severity"] == "critical":
                    prev["critical_incident_count"] += 1
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
                        "critical_incident_count": 1 if row["severity"] == "critical" else 0,
                        "source_incident_ids": [str(row["incident_id"])],
                        "max_severity": row["severity"],
                    }
                )

        for block in merged:
            block["duration_ms"] = block["end_ms"] - block["start_ms"]
            block["source_incident_ids"] = sorted(block["source_incident_ids"])
            overlap_spans: list[tuple[int, int]] = []
            for start, end in maintenance.get(service, []):
                span_start = max(block["start_ms"], start)
                span_end = min(block["end_ms"], end)
                if span_end > span_start:
                    overlap_spans.append((span_start, span_end))
            overlap_total = sum(span_end - span_start for span_start, span_end in overlap_spans)
            block["maintenance_overlap_ms"] = overlap_total
            block["maintenance_span_count"] = len(overlap_spans)
            block["billable_duration_ms"] = max(block["duration_ms"] - overlap_total, 0)
            block["window_signature"] = hashlib.sha1(
                (
                    f"{service}|{block['start_ms']}|{block['end_ms']}|"
                    f"{','.join(block['source_incident_ids'])}|{block['max_severity']}"
                ).encode("utf-8")
            ).hexdigest()[:10]

        windows[service] = merged

    return windows, planned_excluded_count, maintenance


def build_queue(windows: dict[str, list[dict]], policy_data: dict) -> list[dict]:
    rows: list[dict] = []
    for service, blocks in windows.items():
        policy_profile, policy = _policy_for_service(service, policy_data)
        for block in blocks:
            if block["billable_duration_ms"] < policy["queue_min_effective_ms"]:
                continue
            severity_weight = policy["severity_weight"].get(block["max_severity"], 0)
            escalation_score = (
                block["billable_duration_ms"] // 60
                + block["incident_count"] * 2
                + block["critical_incident_count"] * 3
                + (policy["no_overlap_bonus"] if block["maintenance_overlap_ms"] == 0 else 0)
                + block["maintenance_span_count"] * policy["segment_bonus"]
                + severity_weight
            )
            if (
                (block["max_severity"] == "critical" and block["billable_duration_ms"] >= policy["critical_p1_min_ms"])
                or block["billable_duration_ms"] >= policy["critical_threshold_ms"]
                or block["critical_incident_count"] >= policy["critical_count_for_critical"]
                or escalation_score >= policy["score_threshold_critical"]
            ):
                priority = "critical"
            elif (
                block["billable_duration_ms"] >= policy["high_threshold_ms"]
                or (block["incident_count"] >= 3 and block["max_severity"] in {"major", "critical"})
                or (
                    block["maintenance_overlap_ms"] == 0
                    and block["duration_ms"] >= policy["no_overlap_high_duration_ms"]
                )
                or escalation_score >= policy["score_threshold_high"]
            ):
                priority = "high"
            else:
                priority = "medium"
            incident_ids_csv = ",".join(block["source_incident_ids"])
            signature = hashlib.sha1(
                (
                    f"{service}|{block['start_ms']}|{block['end_ms']}|"
                    f"{incident_ids_csv}|{block['window_signature']}|{block['max_severity']}|"
                    f"{block['maintenance_span_count']}|{policy_profile}"
                ).encode("utf-8")
            ).hexdigest()[:12]
            rows.append(
                {
                    "window_id": f"{service}:{block['start_ms']}-{block['end_ms']}",
                    "service": service,
                    "start_ms": block["start_ms"],
                    "end_ms": block["end_ms"],
                    "duration_ms": block["duration_ms"],
                    "maintenance_overlap_ms": block["maintenance_overlap_ms"],
                    "maintenance_span_count": block["maintenance_span_count"],
                    "billable_duration_ms": block["billable_duration_ms"],
                    "incident_count": block["incident_count"],
                    "critical_incident_count": block["critical_incident_count"],
                    "source_incident_ids": block["source_incident_ids"],
                    "max_severity": block["max_severity"],
                    "window_signature": block["window_signature"],
                    "policy_profile": policy_profile,
                    "policy_queue_min_ms": policy["queue_min_effective_ms"],
                    "escalation_score": escalation_score,
                    "priority": priority,
                    "outage_signature": signature,
                }
            )

    rank = {name: idx for idx, name in enumerate(PRIORITY_ORDER)}
    rows.sort(
        key=lambda row: (
            rank[row["priority"]],
            -row["escalation_score"],
            -row["billable_duration_ms"],
            -row["critical_incident_count"],
            -row["maintenance_span_count"],
            -row["incident_count"],
            row["service"],
            row["start_ms"],
        )
    )
    return rows


def build_summary(
    raw_rows: list[dict],
    canonical_rows: list[dict],
    maintenance: dict[str, list[tuple[int, int]]],
    policy_data: dict,
    windows: dict[str, list[dict]],
    queue: list[dict],
    planned_excluded_count: int,
) -> dict:
    severity_counts = {name: 0 for name in SEVERITY_ORDER}
    for row in canonical_rows:
        severity_counts[row["severity"]] += 1

    total_unplanned = sum(block["duration_ms"] for blocks in windows.values() for block in blocks)
    total_maintenance = sum(
        block["maintenance_overlap_ms"] for blocks in windows.values() for block in blocks
    )
    total_maintenance_span_count = sum(
        block["maintenance_span_count"] for blocks in windows.values() for block in blocks
    )
    total_billable = sum(
        block["billable_duration_ms"] for blocks in windows.values() for block in blocks
    )
    longest_window = max(
        (block["duration_ms"] for blocks in windows.values() for block in blocks),
        default=0,
    )
    critical_window_count = sum(
        1 for blocks in windows.values() for block in blocks if block["max_severity"] == "critical"
    )
    priority_counts = {name: 0 for name in PRIORITY_ORDER}
    for row in queue:
        priority_counts[row["priority"]] += 1
    max_escalation_score = max((row["escalation_score"] for row in queue), default=0)
    canonical_input_checksum = hashlib.sha256(
        "\n".join(
            (
                f"{row['incident_id']}|{row['service']}|{row['start_ms']}|"
                f"{row['end_ms']}|{row['severity']}|{1 if row['planned'] else 0}"
            )
            for row in canonical_rows
        ).encode("utf-8")
    ).hexdigest()
    queue_signature_checksum = hashlib.sha256(
        "|".join(row["outage_signature"] for row in queue).encode("utf-8")
    ).hexdigest()
    maintenance_compaction_checksum = hashlib.sha256(
        "\n".join(
            f"{service}|{start}|{end}"
            for service in sorted(maintenance)
            for start, end in maintenance[service]
        ).encode("utf-8")
    ).hexdigest()
    policy_checksum = _policy_checksum(policy_data)

    return {
        "schema_version": "outage-windows-v1",
        "raw_incident_count": len(raw_rows),
        "unique_incident_ids": len({str(row["incident_id"]) for row in raw_rows}),
        "canonical_incident_count": len(canonical_rows),
        "service_count": len(windows),
        "severity_counts": severity_counts,
        "total_unplanned_downtime_ms": total_unplanned,
        "total_maintenance_overlap_ms": total_maintenance,
        "total_maintenance_span_count": total_maintenance_span_count,
        "total_billable_downtime_ms": total_billable,
        "longest_window_ms": longest_window,
        "queued_window_count": len(queue),
        "priority_counts": priority_counts,
        "max_escalation_score": max_escalation_score,
        "planned_excluded_count": planned_excluded_count,
        "critical_window_count": critical_window_count,
        "canonical_input_checksum": canonical_input_checksum,
        "queue_signature_checksum": queue_signature_checksum,
        "maintenance_compaction_checksum": maintenance_compaction_checksum,
        "policy_checksum": policy_checksum,
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
    policy_data = load_policies()
    canonical_rows = canonicalize(raw_rows)
    windows, planned_excluded_count, maintenance = merge_windows(canonical_rows, maintenance_rows)
    queue = build_queue(windows, policy_data)
    summary = build_summary(
        raw_rows=raw_rows,
        canonical_rows=canonical_rows,
        maintenance=maintenance,
        policy_data=policy_data,
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
