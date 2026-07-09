"""Verify repaired outage compiler behavior and outputs."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

OUTPUT_DIR = Path("/app/output")
SUMMARY_PATH = OUTPUT_DIR / "downtime_summary.json"
WINDOWS_PATH = OUTPUT_DIR / "service_windows.json"
QUEUE_PATH = OUTPUT_DIR / "incident_queue.jsonl"
PIPELINE = Path("/app/workflow/compile_outages.py")
ORIGINAL_PIPELINE = Path("/app/workflow/.compile_outages.original")
INPUT_PATH = Path("/app/data/outages.json")
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


def _load_input(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def _canonicalize(rows: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for row in rows:
        incident_id = str(row["incident_id"])
        normalized = dict(row)
        normalized["service"] = str(normalized.get("service", "")).strip().lower()
        normalized["severity"] = str(normalized.get("severity", "")).strip().lower()
        normalized["planned"] = bool(normalized.get("planned", False))
        current = deduped.get(incident_id)
        if current is None or normalized["end_ms"] > current["end_ms"]:
            deduped[incident_id] = normalized
    return sorted(deduped.values(), key=lambda row: (row["service"], row["start_ms"], row["incident_id"]))


def _merge_unplanned(canonical_rows: list[dict]) -> tuple[dict[str, list[dict]], int]:
    by_service: dict[str, list[dict]] = {}
    planned_excluded_count = 0
    for row in canonical_rows:
        if row["planned"]:
            planned_excluded_count += 1
            continue
        by_service.setdefault(row["service"], []).append(row)

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
                        "max_severity": row["severity"],
                    }
                )
                continue
            prev = merged[-1]
            if row["start_ms"] <= prev["end_ms"]:
                prev["end_ms"] = max(prev["end_ms"], row["end_ms"])
                prev["incident_count"] += 1
                if SEVERITY_RANK[row["severity"]] > SEVERITY_RANK[prev["max_severity"]]:
                    prev["max_severity"] = row["severity"]
            else:
                merged.append(
                    {
                        "start_ms": row["start_ms"],
                        "end_ms": row["end_ms"],
                        "incident_count": 1,
                        "max_severity": row["severity"],
                    }
                )

        for block in merged:
            block["duration_ms"] = block["end_ms"] - block["start_ms"]
        windows[service] = merged

    return windows, planned_excluded_count


def _queue_from_windows(windows: dict[str, list[dict]]) -> list[dict]:
    rows: list[dict] = []
    for service, blocks in windows.items():
        for block in blocks:
            if block["duration_ms"] < 250:
                continue
            if block["max_severity"] == "critical" or block["duration_ms"] >= 700:
                priority = "critical"
            elif block["duration_ms"] >= 400:
                priority = "high"
            else:
                priority = "medium"
            rows.append(
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

    priority_rank = {name: idx for idx, name in enumerate(PRIORITY_ORDER)}
    rows.sort(
        key=lambda row: (
            priority_rank[row["priority"]],
            -row["duration_ms"],
            row["service"],
            row["start_ms"],
        )
    )
    return rows


def _build_summary(raw_rows: list[dict], canonical_rows: list[dict], windows: dict[str, list[dict]], queue: list[dict], planned_excluded_count: int) -> dict:
    severity_counts = {"critical": 0, "major": 0, "minor": 0}
    for row in canonical_rows:
        if row["severity"] in severity_counts:
            severity_counts[row["severity"]] += 1

    total_unplanned = sum(block["duration_ms"] for blocks in windows.values() for block in blocks)
    return {
        "schema_version": "outage-windows-v1",
        "raw_incident_count": len(raw_rows),
        "unique_incident_ids": len({str(row["incident_id"]) for row in raw_rows}),
        "canonical_incident_count": len(canonical_rows),
        "service_count": len(windows),
        "severity_counts": severity_counts,
        "total_unplanned_downtime_ms": total_unplanned,
        "queued_window_count": len(queue),
        "planned_excluded_count": planned_excluded_count,
    }


def _expected_from_input(path: Path) -> tuple[dict, dict[str, list[dict]], list[dict]]:
    raw_rows = _load_input(path)
    canonical_rows = _canonicalize(raw_rows)
    windows, planned_count = _merge_unplanned(canonical_rows)
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
    return json.loads(SUMMARY_PATH.read_text())


@pytest.fixture(scope="session")
def windows() -> dict[str, list[dict]]:
    return json.loads(WINDOWS_PATH.read_text())


@pytest.fixture(scope="session")
def queue_rows() -> list[dict]:
    return _queue_rows()


def test_cli_exists():
    assert PIPELINE.exists(), f"pipeline not found at {PIPELINE}"


def test_outputs_exist():
    for path in (SUMMARY_PATH, WINDOWS_PATH, QUEUE_PATH):
        assert path.exists(), f"missing required output: {path}"


def test_summary_schema(summary: dict):
    for key in (
        "schema_version",
        "raw_incident_count",
        "unique_incident_ids",
        "canonical_incident_count",
        "service_count",
        "severity_counts",
        "total_unplanned_downtime_ms",
        "queued_window_count",
        "planned_excluded_count",
    ):
        assert key in summary
    assert summary["schema_version"] == "outage-windows-v1"
    assert list(summary["severity_counts"].keys()) == ["critical", "major", "minor"]


def test_summary_matches_fixture(summary: dict):
    for key in (
        "schema_version",
        "raw_incident_count",
        "unique_incident_ids",
        "canonical_incident_count",
        "service_count",
        "severity_counts",
        "total_unplanned_downtime_ms",
        "queued_window_count",
        "planned_excluded_count",
    ):
        assert summary[key] == FIXTURE[key]


def test_summary_computed_from_input(summary: dict):
    expected_summary, _, _ = _expected_from_input(INPUT_PATH)
    assert summary == expected_summary


def test_service_windows_match_fixture(windows: dict[str, list[dict]]):
    assert windows == FIXTURE["expected_service_windows"]


def test_service_windows_computed_from_input(windows: dict[str, list[dict]]):
    _, expected_windows, _ = _expected_from_input(INPUT_PATH)
    assert windows == expected_windows


def test_queue_window_ids_match_fixture(queue_rows: list[dict]):
    assert [row["window_id"] for row in queue_rows] == FIXTURE["expected_queue_window_ids"]


def test_queue_computed_from_input(queue_rows: list[dict]):
    _, _, expected_queue = _expected_from_input(INPUT_PATH)
    assert queue_rows == expected_queue


def test_queue_required_fields(queue_rows: list[dict]):
    for row in queue_rows:
        assert set(row.keys()) == {
            "window_id",
            "service",
            "start_ms",
            "end_ms",
            "duration_ms",
            "incident_count",
            "max_severity",
            "priority",
        }


def test_queue_priorities(queue_rows: list[dict]):
    for row in queue_rows:
        if row["max_severity"] == "critical" or row["duration_ms"] >= 700:
            assert row["priority"] == "critical"
        elif row["duration_ms"] >= 400:
            assert row["priority"] == "high"
        else:
            assert row["priority"] == "medium"


def test_queue_sorted(queue_rows: list[dict]):
    rank = {name: idx for idx, name in enumerate(PRIORITY_ORDER)}
    actual = [
        (rank[row["priority"]], -row["duration_ms"], row["service"], row["start_ms"])
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


def test_windows_are_sorted(windows: dict[str, list[dict]]):
    assert list(windows.keys()) == sorted(windows.keys())
    for blocks in windows.values():
        starts = [block["start_ms"] for block in blocks]
        assert starts == sorted(starts)


def test_original_snapshot_preserved():
    assert ORIGINAL_PIPELINE.exists()
    digest = hashlib.sha256(ORIGINAL_PIPELINE.read_bytes()).hexdigest()
    assert digest == FIXTURE["broken_pipeline_sha256"]


def test_broken_snapshot_is_wrong():
    with tempfile.TemporaryDirectory() as tmp:
        broken = Path(tmp) / "compile_outages.py"
        out = Path(tmp) / "out"
        shutil.copy(ORIGINAL_PIPELINE, broken)
        result = _run_pipeline(pipeline=broken, output_dir=out)
        assert result.returncode == 0, result.stderr
        queue = _queue_rows(out / "incident_queue.jsonl")
        assert len(queue) == FIXTURE["broken_queue_count"]
        assert len(queue) != FIXTURE["queued_window_count"]


def test_pipeline_rerun_idempotent(summary: dict, queue_rows: list[dict]):
    with tempfile.TemporaryDirectory() as tmp:
        rerun_dir = Path(tmp) / "rerun"
        rerun_dir.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(output_dir=rerun_dir)
        assert result.returncode == 0, result.stderr
        rerun_summary = json.loads((rerun_dir / "downtime_summary.json").read_text())
        rerun_queue = _queue_rows(rerun_dir / "incident_queue.jsonl")
        assert rerun_summary == summary
        assert rerun_queue == queue_rows


def test_pipeline_supports_alternate_input():
    alt_path = Path(FIXTURE["alternate_input"])
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "alt"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(input_path=alt_path, output_dir=out)
        assert result.returncode == 0, result.stderr
        summary = json.loads((out / "downtime_summary.json").read_text())
        queue_rows = _queue_rows(out / "incident_queue.jsonl")
        expected_summary, _, expected_queue = _expected_from_input(alt_path)
        assert summary == expected_summary
        assert queue_rows == expected_queue


def test_alternate_fixture_values():
    alt = FIXTURE["alternate_expected"]
    alt_path = Path(FIXTURE["alternate_input"])
    expected_summary, _, expected_queue = _expected_from_input(alt_path)
    for key in (
        "raw_incident_count",
        "unique_incident_ids",
        "canonical_incident_count",
        "service_count",
        "severity_counts",
        "total_unplanned_downtime_ms",
        "queued_window_count",
        "planned_excluded_count",
    ):
        assert expected_summary[key] == alt[key]
    assert [row["window_id"] for row in expected_queue] == alt["queue_window_ids"]


def test_pipeline_supports_custom_output_dir():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "custom-output"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(output_dir=out)
        assert result.returncode == 0, result.stderr
        assert (out / "downtime_summary.json").exists()
        assert (out / "service_windows.json").exists()
        assert (out / "incident_queue.jsonl").exists()
