"""Verify repaired outage compiler behavior and outputs."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import pytest

OUTPUT_DIR = Path("/app/output")
SUMMARY_PATH = OUTPUT_DIR / "downtime_summary.json"
WINDOWS_PATH = OUTPUT_DIR / "service_windows.json"
QUEUE_PATH = OUTPUT_DIR / "incident_queue.jsonl"
PIPELINE = Path("/app/workflow/compile_outages.py")
ORIGINAL_PIPELINE = Path("/app/workflow/.compile_outages.original")
INPUT_PATH = Path("/app/data/outages.json")
MAINTENANCE_PATH = Path("/app/data/maintenance_windows.json")
ALT_INPUT_PATH = Path("/tests/fixtures/alt_outages.json")
FIXTURE_PATH = Path("/tests/fixtures/expected_outputs.json")
FIXTURE = json.loads(FIXTURE_PATH.read_text())

PRIORITY_ORDER = ("critical", "high", "medium")
SEVERITY_RANK = {"minor": 1, "major": 2, "critical": 3}


def _run_pipeline(
    pipeline: Path = PIPELINE,
    input_path: Path = INPUT_PATH,
    output_dir: Path = OUTPUT_DIR,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "python3",
            str(pipeline),
            "--input",
            str(input_path),
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )


def _load_json(path: Path):
    return json.loads(path.read_text())


def _normalize_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def _executable_text(src: str) -> str:
    docstring_lines: set[int] = set()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
            if isinstance(first.value.value, str):
                end = getattr(first, "end_lineno", first.lineno)
                docstring_lines.update(range(first.lineno, end + 1))

    lines: list[str] = []
    for line_number, line in enumerate(src.splitlines(), start=1):
        if line_number in docstring_lines:
            continue
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if "#" in line:
            line = line.split("#", 1)[0]
        lines.append(line)
    return "\n".join(lines)


def _canonicalize(rows: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for row in rows:
        incident_id = str(row["incident_id"])
        normalized = dict(row)
        normalized["service"] = str(normalized.get("service", "")).strip().lower()
        normalized["severity"] = str(normalized.get("severity", "")).strip().lower()
        normalized["planned"] = _normalize_bool(normalized.get("planned", False))
        current = deduped.get(incident_id)
        if current is None or normalized["end_ms"] > current["end_ms"]:
            deduped[incident_id] = normalized
    return sorted(
        deduped.values(),
        key=lambda row: (row["service"], row["start_ms"], str(row["incident_id"])),
    )


def _maintenance_by_service(rows: list[dict]) -> dict[str, list[tuple[int, int]]]:
    out: dict[str, list[tuple[int, int]]] = {}
    for row in rows:
        service = str(row.get("service", "")).strip().lower()
        out.setdefault(service, []).append((int(row["start_ms"]), int(row["end_ms"])))
    return out


def _overlap_ms(start_a: int, end_a: int, start_b: int, end_b: int) -> int:
    return max(0, min(end_a, end_b) - max(start_a, start_b))


def _merge_unplanned(
    canonical_rows: list[dict], maintenance_rows: list[dict]
) -> tuple[dict[str, list[dict]], int]:
    by_service: dict[str, list[dict]] = {}
    planned_excluded_count = 0
    for row in canonical_rows:
        if row["planned"]:
            planned_excluded_count += 1
            continue
        by_service.setdefault(row["service"], []).append(row)

    maintenance = _maintenance_by_service(maintenance_rows)
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
                event_id = str(row["incident_id"])
                if event_id not in prev["source_incident_ids"]:
                    prev["source_incident_ids"].append(event_id)
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
            block["source_incident_ids"] = sorted(block["source_incident_ids"])
            block["duration_ms"] = block["end_ms"] - block["start_ms"]
            overlap = 0
            for start, end in maintenance.get(service, []):
                overlap += _overlap_ms(block["start_ms"], block["end_ms"], start, end)
            block["maintenance_overlap_ms"] = overlap
            block["billable_duration_ms"] = max(block["duration_ms"] - overlap, 0)
        windows[service] = merged

    return windows, planned_excluded_count


def _queue_from_windows(windows: dict[str, list[dict]]) -> list[dict]:
    rows: list[dict] = []
    for service, blocks in windows.items():
        for block in blocks:
            if block["billable_duration_ms"] < 250:
                continue

            if (
                block["max_severity"] == "critical"
                and block["billable_duration_ms"] >= 300
            ) or block["billable_duration_ms"] >= 700:
                priority = "critical"
            elif block["billable_duration_ms"] >= 350 or (
                block["incident_count"] >= 3
                and block["max_severity"] in {"major", "critical"}
            ):
                priority = "high"
            else:
                priority = "medium"

            ids_csv = ",".join(block["source_incident_ids"])
            signature = hashlib.sha1(
                f"{service}|{block['start_ms']}|{block['end_ms']}|{ids_csv}".encode("utf-8")
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


def _build_summary(
    raw_rows: list[dict],
    canonical_rows: list[dict],
    windows: dict[str, list[dict]],
    queue: list[dict],
    planned_excluded_count: int,
) -> dict:
    severity_counts = {"critical": 0, "major": 0, "minor": 0}
    for row in canonical_rows:
        if row["severity"] in severity_counts:
            severity_counts[row["severity"]] += 1

    total_unplanned = sum(block["duration_ms"] for blocks in windows.values() for block in blocks)
    total_maintenance = sum(
        block["maintenance_overlap_ms"] for blocks in windows.values() for block in blocks
    )
    total_billable = sum(
        block["billable_duration_ms"] for blocks in windows.values() for block in blocks
    )
    longest_window = max(
        (block["duration_ms"] for blocks in windows.values() for block in blocks), default=0
    )
    checksum = hashlib.sha256(
        "|".join(row["outage_signature"] for row in queue).encode("utf-8")
    ).hexdigest()

    return {
        "schema_version": "outage-windows-v1",
        "raw_incident_count": len(raw_rows),
        "unique_incident_ids": len({str(row["incident_id"]) for row in raw_rows}),
        "canonical_incident_count": len(canonical_rows),
        "service_count": len(windows),
        "severity_counts": severity_counts,
        "total_unplanned_downtime_ms": total_unplanned,
        "total_maintenance_overlap_ms": total_maintenance,
        "total_billable_downtime_ms": total_billable,
        "longest_window_ms": longest_window,
        "queued_window_count": len(queue),
        "planned_excluded_count": planned_excluded_count,
        "queue_signature_checksum": checksum,
    }


def _expected_from_input(path: Path) -> tuple[dict, dict[str, list[dict]], list[dict]]:
    raw_rows = _load_json(path)
    maintenance_rows = _load_json(MAINTENANCE_PATH)
    canonical_rows = _canonicalize(raw_rows)
    windows, planned_count = _merge_unplanned(canonical_rows, maintenance_rows)
    queue = _queue_from_windows(windows)
    summary = _build_summary(raw_rows, canonical_rows, windows, queue, planned_count)
    return summary, windows, queue


def _queue_rows(path: Path = QUEUE_PATH) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


@pytest.fixture(scope="session", autouse=True)
def _prepare_outputs():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result = _run_pipeline()
    assert result.returncode == 0, result.stderr


@pytest.fixture(scope="session")
def summary() -> dict:
    return _load_json(SUMMARY_PATH)


@pytest.fixture(scope="session")
def windows() -> dict[str, list[dict]]:
    return _load_json(WINDOWS_PATH)


@pytest.fixture(scope="session")
def queue_rows() -> list[dict]:
    return _queue_rows()


def test_cli_exists():
    assert PIPELINE.exists(), f"pipeline not found at {PIPELINE}"


def test_outputs_exist():
    for path in (SUMMARY_PATH, WINDOWS_PATH, QUEUE_PATH):
        assert path.exists(), f"missing required output: {path}"


def test_output_dir_contains_exactly_three_files():
    expected_files = {"downtime_summary.json", "service_windows.json", "incident_queue.jsonl"}
    actual_files = {path.name for path in OUTPUT_DIR.iterdir() if path.is_file()}
    assert actual_files == expected_files


def test_summary_schema(summary: dict):
    for key in (
        "schema_version",
        "raw_incident_count",
        "unique_incident_ids",
        "canonical_incident_count",
        "service_count",
        "severity_counts",
        "total_unplanned_downtime_ms",
        "total_maintenance_overlap_ms",
        "total_billable_downtime_ms",
        "longest_window_ms",
        "queued_window_count",
        "planned_excluded_count",
        "queue_signature_checksum",
    ):
        assert key in summary
    assert summary["schema_version"] == "outage-windows-v1"
    assert list(summary["severity_counts"].keys()) == ["critical", "major", "minor"]
    assert len(summary["queue_signature_checksum"]) == 64


def test_summary_matches_expected_computation(summary: dict):
    expected_summary, _, _ = _expected_from_input(INPUT_PATH)
    assert summary == expected_summary


def test_service_windows_match_expected_computation(windows: dict[str, list[dict]]):
    _, expected_windows, _ = _expected_from_input(INPUT_PATH)
    assert windows == expected_windows


def test_queue_window_ids_match_expected_computation(queue_rows: list[dict]):
    _, _, expected_queue = _expected_from_input(INPUT_PATH)
    assert [row["window_id"] for row in queue_rows] == [row["window_id"] for row in expected_queue]


def test_queue_computed_from_input(queue_rows: list[dict]):
    _, _, expected_queue = _expected_from_input(INPUT_PATH)
    assert queue_rows == expected_queue


def test_queue_required_fields(queue_rows: list[dict]):
    expected_keys = {
        "window_id",
        "service",
        "start_ms",
        "end_ms",
        "duration_ms",
        "maintenance_overlap_ms",
        "billable_duration_ms",
        "incident_count",
        "source_incident_ids",
        "max_severity",
        "priority",
        "outage_signature",
    }
    for row in queue_rows:
        assert set(row.keys()) == expected_keys
        assert isinstance(row["source_incident_ids"], list)
        assert row["source_incident_ids"] == sorted(row["source_incident_ids"])
        assert len(row["outage_signature"]) == 12


def test_priority_rules(queue_rows: list[dict]):
    for row in queue_rows:
        if (row["max_severity"] == "critical" and row["billable_duration_ms"] >= 300) or row[
            "billable_duration_ms"
        ] >= 700:
            assert row["priority"] == "critical"
        elif row["billable_duration_ms"] >= 350 or (
            row["incident_count"] >= 3 and row["max_severity"] in {"major", "critical"}
        ):
            assert row["priority"] == "high"
        else:
            assert row["priority"] == "medium"


def test_queue_sorted(queue_rows: list[dict]):
    rank = {name: idx for idx, name in enumerate(PRIORITY_ORDER)}
    actual = [
        (
            rank[row["priority"]],
            -row["billable_duration_ms"],
            -row["incident_count"],
            row["service"],
            row["start_ms"],
        )
        for row in queue_rows
    ]
    assert actual == sorted(actual)


def test_jsonl_compact_format():
    for line in QUEUE_PATH.read_text().splitlines():
        if not line.strip():
            continue
        parsed = json.loads(line)
        assert ": " not in line
        assert json.dumps(parsed, separators=(",", ":")) == line


def test_windows_are_sorted_and_have_extra_fields(windows: dict[str, list[dict]]):
    assert list(windows.keys()) == sorted(windows.keys())
    for blocks in windows.values():
        starts = [block["start_ms"] for block in blocks]
        assert starts == sorted(starts)
        for block in blocks:
            assert set(block.keys()) == {
                "start_ms",
                "end_ms",
                "duration_ms",
                "maintenance_overlap_ms",
                "billable_duration_ms",
                "incident_count",
                "source_incident_ids",
                "max_severity",
            }


def test_maintenance_math_consistency(summary: dict, windows: dict[str, list[dict]]):
    total_duration = sum(block["duration_ms"] for blocks in windows.values() for block in blocks)
    total_overlap = sum(
        block["maintenance_overlap_ms"] for blocks in windows.values() for block in blocks
    )
    total_billable = sum(
        block["billable_duration_ms"] for blocks in windows.values() for block in blocks
    )
    assert summary["total_unplanned_downtime_ms"] == total_duration
    assert summary["total_maintenance_overlap_ms"] == total_overlap
    assert summary["total_billable_downtime_ms"] == total_billable
    assert total_billable <= total_duration
    assert summary["longest_window_ms"] == max(
        (block["duration_ms"] for blocks in windows.values() for block in blocks), default=0
    )


def test_original_snapshot_preserved():
    assert ORIGINAL_PIPELINE.exists()
    digest = hashlib.sha256(ORIGINAL_PIPELINE.read_bytes()).hexdigest()
    assert digest == FIXTURE["broken_pipeline_sha256"]


def test_pipeline_does_not_reference_test_artifacts():
    code = _executable_text(PIPELINE.read_text())
    for token in ("/tests", "test_outputs.py", "expected_outputs.json", "fixtures/"):
        assert token not in code


def test_broken_snapshot_is_wrong():
    with tempfile.TemporaryDirectory() as tmp:
        broken = Path(tmp) / "compile_outages.py"
        out = Path(tmp) / "out"
        shutil.copy(ORIGINAL_PIPELINE, broken)
        result = _run_pipeline(pipeline=broken, output_dir=out)
        assert result.returncode == 0, result.stderr
        queue = _queue_rows(out / "incident_queue.jsonl")
        _, _, expected_queue = _expected_from_input(INPUT_PATH)
        assert len(queue) == FIXTURE["broken_queue_count"]
        assert len(queue) != len(expected_queue)


def test_pipeline_rerun_idempotent(summary: dict, queue_rows: list[dict]):
    with tempfile.TemporaryDirectory() as tmp:
        rerun_dir = Path(tmp) / "rerun"
        rerun_dir.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(output_dir=rerun_dir)
        assert result.returncode == 0, result.stderr
        rerun_summary = _load_json(rerun_dir / "downtime_summary.json")
        rerun_queue = _queue_rows(rerun_dir / "incident_queue.jsonl")
        assert rerun_summary == summary
        assert rerun_queue == queue_rows


def test_pipeline_supports_alternate_input():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "alt"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(input_path=ALT_INPUT_PATH, output_dir=out)
        assert result.returncode == 0, result.stderr
        summary = _load_json(out / "downtime_summary.json")
        queue_rows = _queue_rows(out / "incident_queue.jsonl")
        expected_summary, _, expected_queue = _expected_from_input(ALT_INPUT_PATH)
        assert summary == expected_summary
        assert queue_rows == expected_queue


def test_alternate_input_expected_values():
    expected_summary, _, expected_queue = _expected_from_input(ALT_INPUT_PATH)
    assert expected_summary["raw_incident_count"] == 7
    assert expected_summary["unique_incident_ids"] == 6
    assert expected_summary["canonical_incident_count"] == 6
    assert expected_summary["service_count"] == 3
    assert expected_summary["severity_counts"] == {"critical": 2, "major": 2, "minor": 2}
    assert expected_summary["total_unplanned_downtime_ms"] == 1590
    assert expected_summary["total_maintenance_overlap_ms"] == 240
    assert expected_summary["total_billable_downtime_ms"] == 1350
    assert expected_summary["queued_window_count"] == 3
    assert expected_summary["planned_excluded_count"] == 1
    assert [row["window_id"] for row in expected_queue] == [
        "search:400-920",
        "billing:120-700",
        "auth:10-500",
    ]


def test_pipeline_supports_custom_output_dir():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "custom-output"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(output_dir=out)
        assert result.returncode == 0, result.stderr
        assert (out / "downtime_summary.json").exists()
        assert (out / "service_windows.json").exists()
        assert (out / "incident_queue.jsonl").exists()
        actual_files = {path.name for path in out.iterdir() if path.is_file()}
        assert actual_files == {"downtime_summary.json", "service_windows.json", "incident_queue.jsonl"}
