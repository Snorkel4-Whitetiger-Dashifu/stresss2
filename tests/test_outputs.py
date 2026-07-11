"""Verify repaired outage compiler behavior and outputs."""

from __future__ import annotations

import ast
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
MAINTENANCE_PATH = Path("/app/data/maintenance_windows.json")
ALT_INPUT_PATH = Path("/tests/fixtures/alt_outages.json")
FIXTURE_PATH = Path("/tests/fixtures/expected_outputs.json")
FIXTURE = json.loads(FIXTURE_PATH.read_text())

SEVERITY_RANK = {"minor": 1, "major": 2, "critical": 3}
SEVERITY_ORDER = ("critical", "major", "minor")
PRIORITY_ORDER = ("critical", "high", "medium")
SERVICE_ALIASES = {
    "authentication": "auth",
    "payments": "billing",
    "search-api": "search",
}


def _run_pipeline(
    pipeline: Path = PIPELINE,
    input_path: Path = INPUT_PATH,
    output_dir: Path = OUTPUT_DIR,
) -> subprocess.CompletedProcess[str]:
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


def _load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _normalize_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def _normalize_service(value: object) -> str:
    normalized = str(value if value is not None else "").strip().lower()
    return SERVICE_ALIASES.get(normalized, normalized)


def _normalize_severity(value: object) -> str:
    normalized = str(value if value is not None else "").strip().lower()
    return normalized if normalized in SEVERITY_RANK else "minor"


def _normalize_ms(value: object) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


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
        normalized["service"] = _normalize_service(normalized.get("service", ""))
        normalized["severity"] = _normalize_severity(normalized.get("severity", ""))
        normalized["planned"] = _normalize_bool(normalized.get("planned", False))
        normalized["start_ms"] = _normalize_ms(normalized.get("start_ms", 0))
        normalized["end_ms"] = _normalize_ms(normalized.get("end_ms", 0))
        if normalized["end_ms"] < normalized["start_ms"]:
            normalized["end_ms"] = normalized["start_ms"]

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


def _maintenance_by_service(rows: list[dict]) -> dict[str, list[tuple[int, int]]]:
    out: dict[str, list[tuple[int, int]]] = {}
    for row in rows:
        service = _normalize_service(row.get("service", ""))
        start = _normalize_ms(row.get("start_ms", 0))
        end = _normalize_ms(row.get("end_ms", 0))
        if end <= start:
            continue
        out.setdefault(service, []).append((start, end))
    merged_out: dict[str, list[tuple[int, int]]] = {}
    for service in out:
        intervals = sorted(out[service])
        merged: list[list[int]] = []
        for start, end in intervals:
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
        merged_out[service] = [(start, end) for start, end in merged]
    return merged_out


def _overlap_ms(start_a: int, end_a: int, start_b: int, end_b: int) -> int:
    return max(0, min(end_a, end_b) - max(start_a, start_b))


def _merge_unplanned(
    canonical_rows: list[dict], maintenance_rows: list[dict]
) -> tuple[dict[str, list[dict]], int, dict[str, list[tuple[int, int]]]]:
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
            block["source_incident_ids"] = sorted(block["source_incident_ids"])
            block["duration_ms"] = block["end_ms"] - block["start_ms"]
            overlap_spans: list[tuple[int, int]] = []
            for start, end in maintenance.get(service, []):
                span_start = max(block["start_ms"], start)
                span_end = min(block["end_ms"], end)
                if span_end > span_start:
                    overlap_spans.append((span_start, span_end))
            overlap = sum(span_end - span_start for span_start, span_end in overlap_spans)
            block["maintenance_overlap_ms"] = overlap
            block["maintenance_span_count"] = len(overlap_spans)
            block["billable_duration_ms"] = max(block["duration_ms"] - overlap, 0)
            block["window_signature"] = hashlib.sha1(
                (
                    f"{service}|{block['start_ms']}|{block['end_ms']}|"
                    f"{','.join(block['source_incident_ids'])}|{block['max_severity']}"
                ).encode("utf-8")
            ).hexdigest()[:10]

        windows[service] = merged

    return windows, planned_excluded_count, maintenance


def _queue_from_windows(windows: dict[str, list[dict]]) -> list[dict]:
    rows: list[dict] = []
    for service, blocks in windows.items():
        for block in blocks:
            if block["billable_duration_ms"] < 220:
                continue

            if (
                (block["max_severity"] == "critical" and block["billable_duration_ms"] >= 280)
                or block["billable_duration_ms"] >= 650
                or block["critical_incident_count"] >= 2
            ):
                priority = "critical"
            elif (
                block["billable_duration_ms"] >= 320
                or (block["incident_count"] >= 3 and block["max_severity"] in {"major", "critical"})
                or (block["maintenance_overlap_ms"] == 0 and block["duration_ms"] >= 450)
            ):
                priority = "high"
            else:
                priority = "medium"

            ids_csv = ",".join(block["source_incident_ids"])
            signature = hashlib.sha1(
                (
                    f"{service}|{block['start_ms']}|{block['end_ms']}|"
                    f"{ids_csv}|{block['window_signature']}"
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
                    "priority": priority,
                    "outage_signature": signature,
                }
            )

    rank = {name: idx for idx, name in enumerate(PRIORITY_ORDER)}
    rows.sort(
        key=lambda row: (
            rank[row["priority"]],
            -row["billable_duration_ms"],
            -row["critical_incident_count"],
            -row["maintenance_span_count"],
            -row["incident_count"],
            row["service"],
            row["start_ms"],
        )
    )
    return rows


def _build_summary(
    raw_rows: list[dict],
    canonical_rows: list[dict],
    maintenance: dict[str, list[tuple[int, int]]],
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
    canonical_input_checksum = hashlib.sha256(
        "\n".join(
            (
                f"{row['incident_id']}|{row['service']}|{row['start_ms']}|{row['end_ms']}|"
                f"{row['severity']}|{1 if row['planned'] else 0}"
            )
            for row in canonical_rows
        ).encode("utf-8")
    ).hexdigest()
    checksum = hashlib.sha256(
        "|".join(row["outage_signature"] for row in queue).encode("utf-8")
    ).hexdigest()
    maintenance_compaction_checksum = hashlib.sha256(
        "\n".join(
            f"{service}|{start}|{end}"
            for service in sorted(maintenance)
            for start, end in maintenance[service]
        ).encode("utf-8")
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
        "total_maintenance_span_count": total_maintenance_span_count,
        "total_billable_downtime_ms": total_billable,
        "longest_window_ms": longest_window,
        "queued_window_count": len(queue),
        "planned_excluded_count": planned_excluded_count,
        "critical_window_count": critical_window_count,
        "canonical_input_checksum": canonical_input_checksum,
        "queue_signature_checksum": checksum,
        "maintenance_compaction_checksum": maintenance_compaction_checksum,
    }


def _expected_from_input(path: Path) -> tuple[dict, dict[str, list[dict]], list[dict]]:
    raw_rows = _load_json(path)
    maintenance_rows = _load_json(MAINTENANCE_PATH)
    canonical_rows = _canonicalize(raw_rows)
    windows, planned_count, maintenance = _merge_unplanned(canonical_rows, maintenance_rows)
    queue = _queue_from_windows(windows)
    summary = _build_summary(raw_rows, canonical_rows, maintenance, windows, queue, planned_count)
    return summary, windows, queue


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
    return _load_jsonl(QUEUE_PATH)


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
    assert set(summary.keys()) == {
        "schema_version",
        "raw_incident_count",
        "unique_incident_ids",
        "canonical_incident_count",
        "service_count",
        "severity_counts",
        "total_unplanned_downtime_ms",
        "total_maintenance_overlap_ms",
        "total_maintenance_span_count",
        "total_billable_downtime_ms",
        "longest_window_ms",
        "queued_window_count",
        "planned_excluded_count",
        "critical_window_count",
        "canonical_input_checksum",
        "queue_signature_checksum",
        "maintenance_compaction_checksum",
    }
    assert summary["schema_version"] == "outage-windows-v1"
    assert list(summary["severity_counts"].keys()) == list(SEVERITY_ORDER)
    assert len(summary["canonical_input_checksum"]) == 64
    assert len(summary["queue_signature_checksum"]) == 64


def test_summary_matches_expected_computation(summary: dict):
    expected_summary, _, _ = _expected_from_input(INPUT_PATH)
    assert summary == expected_summary


def test_service_windows_match_expected_computation(windows: dict[str, list[dict]]):
    _, expected_windows, _ = _expected_from_input(INPUT_PATH)
    assert windows == expected_windows


def test_queue_matches_expected_computation(queue_rows: list[dict]):
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
        "maintenance_span_count",
        "billable_duration_ms",
        "incident_count",
        "critical_incident_count",
        "source_incident_ids",
        "max_severity",
        "window_signature",
        "priority",
        "outage_signature",
    }
    for row in queue_rows:
        assert set(row.keys()) == expected_keys
        assert isinstance(row["source_incident_ids"], list)
        assert row["source_incident_ids"] == sorted(row["source_incident_ids"])
        assert len(row["window_signature"]) == 10
        assert len(row["outage_signature"]) == 12


def test_priority_rules(queue_rows: list[dict]):
    for row in queue_rows:
        if (
            (row["max_severity"] == "critical" and row["billable_duration_ms"] >= 280)
            or row["billable_duration_ms"] >= 650
            or row["critical_incident_count"] >= 2
        ):
            assert row["priority"] == "critical"
        elif (
            row["billable_duration_ms"] >= 320
            or (row["incident_count"] >= 3 and row["max_severity"] in {"major", "critical"})
            or (row["maintenance_overlap_ms"] == 0 and row["duration_ms"] >= 450)
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
            -row["critical_incident_count"],
            -row["maintenance_span_count"],
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
                "maintenance_span_count",
                "billable_duration_ms",
                "incident_count",
                "critical_incident_count",
                "source_incident_ids",
                "max_severity",
                "window_signature",
            }


def test_maintenance_math_consistency(summary: dict, windows: dict[str, list[dict]]):
    total_duration = sum(block["duration_ms"] for blocks in windows.values() for block in blocks)
    total_overlap = sum(
        block["maintenance_overlap_ms"] for blocks in windows.values() for block in blocks
    )
    total_spans = sum(block["maintenance_span_count"] for blocks in windows.values() for block in blocks)
    total_billable = sum(
        block["billable_duration_ms"] for blocks in windows.values() for block in blocks
    )
    assert summary["total_unplanned_downtime_ms"] == total_duration
    assert summary["total_maintenance_overlap_ms"] == total_overlap
    assert summary["total_maintenance_span_count"] == total_spans
    assert summary["total_billable_downtime_ms"] == total_billable
    assert total_billable <= total_duration


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
        queue = _load_jsonl(out / "incident_queue.jsonl")
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
        rerun_queue = _load_jsonl(rerun_dir / "incident_queue.jsonl")
        assert rerun_summary == summary
        assert rerun_queue == queue_rows


def test_pipeline_supports_alternate_input():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "alt"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(input_path=ALT_INPUT_PATH, output_dir=out)
        assert result.returncode == 0, result.stderr
        summary = _load_json(out / "downtime_summary.json")
        queue_rows = _load_jsonl(out / "incident_queue.jsonl")
        expected_summary, _, expected_queue = _expected_from_input(ALT_INPUT_PATH)
        assert summary == expected_summary
        assert queue_rows == expected_queue


def test_pipeline_supports_custom_output_dir():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "custom-output"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(output_dir=out)
        assert result.returncode == 0, result.stderr
        actual_files = {path.name for path in out.iterdir() if path.is_file()}
        assert actual_files == {"downtime_summary.json", "service_windows.json", "incident_queue.jsonl"}


def test_cli_defaults_work_and_match_explicit_run():
    with tempfile.TemporaryDirectory() as tmp:
        explicit_out = Path(tmp) / "explicit"
        explicit_out.mkdir(parents=True, exist_ok=True)
        explicit = _run_pipeline(input_path=INPUT_PATH, output_dir=explicit_out)
        assert explicit.returncode == 0, explicit.stderr

        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        implicit = subprocess.run(
            ["python3", str(PIPELINE)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert implicit.returncode == 0, implicit.stderr

        assert _load_json(SUMMARY_PATH) == _load_json(explicit_out / "downtime_summary.json")
        assert _load_json(WINDOWS_PATH) == _load_json(explicit_out / "service_windows.json")
        assert _load_jsonl(QUEUE_PATH) == _load_jsonl(explicit_out / "incident_queue.jsonl")


def test_maintenance_source_path_affects_output():
    original = MAINTENANCE_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "no_maintenance"
            out.mkdir(parents=True, exist_ok=True)
            result = _run_pipeline(input_path=INPUT_PATH, output_dir=out)
            assert result.returncode == 0, result.stderr
            summary = _load_json(out / "downtime_summary.json")
            assert summary["total_maintenance_overlap_ms"] == 0
            assert summary["total_billable_downtime_ms"] == summary["total_unplanned_downtime_ms"]
    finally:
        MAINTENANCE_PATH.write_text(original)


def test_alias_normalization_and_unknown_severity_defaults_to_minor():
    rows = [
        {"incident_id": "n1", "service": " Authentication ", "start_ms": 10, "end_ms": 80, "severity": " MAJOR ", "planned": False},
        {"incident_id": "n2", "service": "payments", "start_ms": 90, "end_ms": 200, "severity": "weird", "planned": False},
        {"incident_id": "n3", "service": "search-api", "start_ms": 210, "end_ms": 280, "severity": "critical", "planned": False},
    ]
    canonical = _canonicalize(rows)
    assert [row["service"] for row in canonical] == ["auth", "billing", "search"]
    assert canonical[1]["severity"] == "minor"


def test_ms_coercion_and_end_floor_normalization():
    rows = [
        {"incident_id": "m1", "service": "auth", "start_ms": " 200 ", "end_ms": "100", "severity": "major", "planned": False},
        {"incident_id": "m2", "service": "auth", "start_ms": "bad", "end_ms": " bad ", "severity": "minor", "planned": False},
    ]
    canonical = _canonicalize(rows)
    by_id = {row["incident_id"]: row for row in canonical}
    assert by_id["m1"]["start_ms"] == 200
    assert by_id["m1"]["end_ms"] == 200
    assert by_id["m2"]["start_ms"] == 0
    assert by_id["m2"]["end_ms"] == 0


def test_dedupe_tie_break_chain():
    rows = [
        {"incident_id": "d1", "service": "auth", "start_ms": 10, "end_ms": 200, "severity": "major", "planned": True},
        {"incident_id": "d1", "service": "auth", "start_ms": 20, "end_ms": 200, "severity": "major", "planned": False},
        {"incident_id": "d1", "service": "billing", "start_ms": 30, "end_ms": 200, "severity": "major", "planned": False},
        {"incident_id": "d1", "service": "auth", "start_ms": 30, "end_ms": 200, "severity": "critical", "planned": False},
    ]
    canonical = _canonicalize(rows)
    assert len(canonical) == 1
    assert canonical[0]["severity"] == "critical"
    assert canonical[0]["planned"] is False
    assert canonical[0]["start_ms"] == 30
    assert canonical[0]["service"] == "auth"


def test_stitch_gap_30_merge_and_window_signature():
    rows = [
        {"incident_id": "g1", "service": "auth", "start_ms": 100, "end_ms": 200, "severity": "major", "planned": False},
        {"incident_id": "g2", "service": "auth", "start_ms": 230, "end_ms": 260, "severity": "critical", "planned": False},
    ]
    maintenance = []
    windows, _, _ = _merge_unplanned(_canonicalize(rows), maintenance)
    assert len(windows["auth"]) == 1
    block = windows["auth"][0]
    assert block["start_ms"] == 100
    assert block["end_ms"] == 260
    assert block["incident_count"] == 2
    assert block["critical_incident_count"] == 1
    assert len(block["window_signature"]) == 10


def test_queue_priority_uses_critical_incident_count_override():
    windows = {
        "auth": [
            {
                "start_ms": 10,
                "end_ms": 300,
                "duration_ms": 290,
                "maintenance_overlap_ms": 90,
                "maintenance_span_count": 2,
                "billable_duration_ms": 200,
                "incident_count": 3,
                "critical_incident_count": 2,
                "source_incident_ids": ["a", "b", "c"],
                "max_severity": "major",
                "window_signature": "1234567890",
            }
        ]
    }
    queue = _queue_from_windows(windows)
    assert len(queue) == 0  # below inclusion threshold still excluded

    windows["auth"][0]["billable_duration_ms"] = 220
    queue = _queue_from_windows(windows)
    assert len(queue) == 1
    assert queue[0]["priority"] == "critical"


def test_queue_signature_includes_window_signature():
    windows = {
        "auth": [
            {
                "start_ms": 10,
                "end_ms": 400,
                "duration_ms": 390,
                "maintenance_overlap_ms": 0,
                "maintenance_span_count": 0,
                "billable_duration_ms": 390,
                "incident_count": 2,
                "critical_incident_count": 1,
                "source_incident_ids": ["x1", "x2"],
                "max_severity": "critical",
                "window_signature": "aaaaaaaaaa",
            }
        ]
    }
    queue_a = _queue_from_windows(windows)
    windows["auth"][0]["window_signature"] = "bbbbbbbbbb"
    queue_b = _queue_from_windows(windows)
    assert queue_a[0]["outage_signature"] != queue_b[0]["outage_signature"]


def test_summary_checksum_fields_are_consistent(summary: dict, queue_rows: list[dict]):
    expected_queue_checksum = hashlib.sha256(
        "|".join(row["outage_signature"] for row in queue_rows).encode("utf-8")
    ).hexdigest()
    assert summary["queue_signature_checksum"] == expected_queue_checksum

    canonical = _canonicalize(_load_json(INPUT_PATH))
    expected_input_checksum = hashlib.sha256(
        "\n".join(
            (
                f"{row['incident_id']}|{row['service']}|{row['start_ms']}|{row['end_ms']}|"
                f"{row['severity']}|{1 if row['planned'] else 0}"
            )
            for row in canonical
        ).encode("utf-8")
    ).hexdigest()
    assert summary["canonical_input_checksum"] == expected_input_checksum

    maintenance = _maintenance_by_service(_load_json(MAINTENANCE_PATH))
    expected_maintenance_checksum = hashlib.sha256(
        "\n".join(
            f"{service}|{start}|{end}"
            for service in sorted(maintenance)
            for start, end in maintenance[service]
        ).encode("utf-8")
    ).hexdigest()
    assert summary["maintenance_compaction_checksum"] == expected_maintenance_checksum


def test_maintenance_overlap_uses_compacted_non_overlapping_spans():
    canonical_rows = _canonicalize(
        [
            {
                "incident_id": "mwin",
                "service": "Payments",
                "start_ms": 90,
                "end_ms": 260,
                "severity": "major",
                "planned": False,
            }
        ]
    )
    maintenance_rows = [
        {"service": "billing", "start_ms": 100, "end_ms": 150},
        {"service": "billing", "start_ms": 140, "end_ms": 200},
        {"service": "payments", "start_ms": 200, "end_ms": 230},
        {"service": "billing", "start_ms": 230, "end_ms": 250},
    ]
    windows, _, maintenance = _merge_unplanned(canonical_rows, maintenance_rows)
    assert maintenance["billing"] == [(100, 250)]
    block = windows["billing"][0]
    assert block["maintenance_overlap_ms"] == 150
    assert block["maintenance_span_count"] == 1
