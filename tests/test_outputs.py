"""Verifier tests for outage compiler hard task."""

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
MAINTENANCE_PATH = Path("/app/data/maintenance_windows.json")
POLICY_PATH = Path("/app/data/response_policies.json")
EXCEPTIONS_PATH = Path("/app/data/routing_exceptions.json")
ALT_INPUT_PATH = Path("/tests/fixtures/alt_outages.json")

FIXTURE = json.loads(Path("/tests/fixtures/expected_outputs.json").read_text())

SEVERITY_ORDER = ("critical", "major", "minor")
PRIORITY_ORDER = ("critical", "high", "medium")


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


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


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
    assert PIPELINE.exists(), f"pipeline missing at {PIPELINE}"


def test_outputs_exist():
    for path in (SUMMARY_PATH, WINDOWS_PATH, QUEUE_PATH):
        assert path.exists(), f"missing required output: {path}"


def test_output_dir_contains_exactly_three_files():
    names = {p.name for p in OUTPUT_DIR.iterdir() if p.is_file()}
    assert names == {"downtime_summary.json", "service_windows.json", "incident_queue.jsonl"}


def test_primary_summary_exact_fixture(summary: dict):
    assert summary == FIXTURE["primary"]["summary"]


def test_primary_windows_exact_fixture(windows: dict[str, list[dict]]):
    assert windows == FIXTURE["primary"]["windows"]


def test_primary_queue_exact_fixture(queue_rows: list[dict]):
    assert queue_rows == FIXTURE["primary"]["queue_rows"]


def test_alternate_input_exact_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "alt"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(input_path=ALT_INPUT_PATH, output_dir=out)
        assert result.returncode == 0, result.stderr
        assert _load_json(out / "downtime_summary.json") == FIXTURE["alternate"]["summary"]
        assert _load_json(out / "service_windows.json") == FIXTURE["alternate"]["windows"]
        assert _load_jsonl(out / "incident_queue.jsonl") == FIXTURE["alternate"]["queue_rows"]


def test_summary_schema_and_order(summary: dict):
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
        "total_suppression_overlap_ms",
        "total_boost_overlap_ms",
        "total_billable_downtime_ms",
        "longest_window_ms",
        "queued_window_count",
        "priority_counts",
        "max_escalation_score",
        "max_exception_balance_score",
        "planned_excluded_count",
        "critical_window_count",
        "canonical_input_checksum",
        "queue_signature_checksum",
        "maintenance_compaction_checksum",
        "exception_compaction_checksum",
        "policy_checksum",
    }
    assert summary["schema_version"] == "outage-windows-v1"
    assert list(summary["severity_counts"].keys()) == list(SEVERITY_ORDER)
    assert list(summary["priority_counts"].keys()) == list(PRIORITY_ORDER)
    assert len(summary["canonical_input_checksum"]) == 64
    assert len(summary["queue_signature_checksum"]) == 64
    assert len(summary["maintenance_compaction_checksum"]) == 64
    assert len(summary["exception_compaction_checksum"]) == 64
    assert len(summary["policy_checksum"]) == 64


def test_window_shape_and_sorting(windows: dict[str, list[dict]]):
    expected_keys = {
        "start_ms",
        "end_ms",
        "duration_ms",
        "maintenance_overlap_ms",
        "maintenance_span_count",
        "suppression_overlap_ms",
        "boost_overlap_ms",
        "billable_duration_ms",
        "incident_count",
        "critical_incident_count",
        "source_incident_ids",
        "max_severity",
        "window_signature",
    }
    assert list(windows.keys()) == sorted(windows.keys())
    for blocks in windows.values():
        starts = [b["start_ms"] for b in blocks]
        assert starts == sorted(starts)
        for block in blocks:
            assert set(block.keys()) == expected_keys
            assert block["duration_ms"] == block["end_ms"] - block["start_ms"]
            assert block["billable_duration_ms"] == max(
                block["duration_ms"] - block["maintenance_overlap_ms"], 0
            )
            assert block["source_incident_ids"] == sorted(block["source_incident_ids"])


def test_queue_required_fields_and_lengths(queue_rows: list[dict]):
    expected = {
        "window_id",
        "service",
        "start_ms",
        "end_ms",
        "duration_ms",
        "maintenance_overlap_ms",
        "maintenance_span_count",
        "suppression_overlap_ms",
        "boost_overlap_ms",
        "billable_duration_ms",
        "incident_count",
        "critical_incident_count",
        "source_incident_ids",
        "max_severity",
        "window_signature",
        "policy_profile",
        "policy_queue_min_ms",
        "effective_queue_min_ms",
        "exception_balance_score",
        "escalation_score",
        "priority",
        "outage_signature",
    }
    for row in queue_rows:
        assert set(row.keys()) == expected
        assert row["priority"] in PRIORITY_ORDER
        assert len(row["window_signature"]) == 10
        assert len(row["outage_signature"]) == 12


def test_priority_rules_are_enforced(queue_rows: list[dict]):
    for row in queue_rows:
        assert row["billable_duration_ms"] >= row["effective_queue_min_ms"]
        assert row["effective_queue_min_ms"] >= 0
        assert row["policy_profile"] in {"default", "auth", "billing", "search"}
        assert isinstance(row["exception_balance_score"], int)


def test_queue_sorted_with_all_tiebreaks(queue_rows: list[dict]):
    rank = {name: i for i, name in enumerate(PRIORITY_ORDER)}
    sort_keys = [
        (
            rank[row["priority"]],
            -row["escalation_score"],
            -row["exception_balance_score"],
            -row["billable_duration_ms"],
            -row["critical_incident_count"],
            -row["maintenance_span_count"],
            -row["incident_count"],
            row["service"],
            row["start_ms"],
        )
        for row in queue_rows
    ]
    assert sort_keys == sorted(sort_keys)


def test_jsonl_compact_format():
    for line in QUEUE_PATH.read_text().splitlines():
        if not line.strip():
            continue
        parsed = json.loads(line)
        assert ": " not in line
        assert json.dumps(parsed, separators=(",", ":")) == line


def test_maintenance_math_consistency(summary: dict, windows: dict[str, list[dict]]):
    total_duration = sum(b["duration_ms"] for blocks in windows.values() for b in blocks)
    total_overlap = sum(b["maintenance_overlap_ms"] for blocks in windows.values() for b in blocks)
    total_spans = sum(b["maintenance_span_count"] for blocks in windows.values() for b in blocks)
    total_suppression = sum(b["suppression_overlap_ms"] for blocks in windows.values() for b in blocks)
    total_boost = sum(b["boost_overlap_ms"] for blocks in windows.values() for b in blocks)
    total_billable = sum(b["billable_duration_ms"] for blocks in windows.values() for b in blocks)
    assert summary["total_unplanned_downtime_ms"] == total_duration
    assert summary["total_maintenance_overlap_ms"] == total_overlap
    assert summary["total_maintenance_span_count"] == total_spans
    assert summary["total_suppression_overlap_ms"] == total_suppression
    assert summary["total_boost_overlap_ms"] == total_boost
    assert summary["total_billable_downtime_ms"] == total_billable


def test_checksum_fields_match_fixture(summary: dict):
    assert summary["canonical_input_checksum"] == FIXTURE["primary"]["summary"]["canonical_input_checksum"]
    assert summary["queue_signature_checksum"] == FIXTURE["primary"]["summary"]["queue_signature_checksum"]
    assert (
        summary["maintenance_compaction_checksum"]
        == FIXTURE["primary"]["summary"]["maintenance_compaction_checksum"]
    )
    assert (
        summary["exception_compaction_checksum"]
        == FIXTURE["primary"]["summary"]["exception_compaction_checksum"]
    )
    assert summary["policy_checksum"] == FIXTURE["primary"]["summary"]["policy_checksum"]


def test_original_snapshot_preserved():
    assert ORIGINAL_PIPELINE.exists()
    digest = hashlib.sha256(ORIGINAL_PIPELINE.read_bytes()).hexdigest()
    assert digest == FIXTURE["broken_pipeline_sha256"]


def test_pipeline_does_not_reference_test_artifacts():
    code = PIPELINE.read_text()
    for token in ("/tests", "expected_outputs.json", "fixtures/alt_outages.json", "test_outputs.py"):
        assert token not in code


def test_broken_snapshot_is_wrong():
    with tempfile.TemporaryDirectory() as tmp:
        broken = Path(tmp) / "compile_outages.py"
        out = Path(tmp) / "broken_out"
        shutil.copy(ORIGINAL_PIPELINE, broken)
        result = _run_pipeline(pipeline=broken, output_dir=out)
        assert result.returncode == 0, result.stderr
        queue = _load_jsonl(out / "incident_queue.jsonl")
        assert len(queue) == FIXTURE["broken_queue_count"]
        assert queue != FIXTURE["primary"]["queue_rows"]


def test_pipeline_rerun_idempotent(summary: dict, windows: dict[str, list[dict]], queue_rows: list[dict]):
    with tempfile.TemporaryDirectory() as tmp:
        rerun = Path(tmp) / "rerun"
        rerun.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(output_dir=rerun)
        assert result.returncode == 0, result.stderr
        assert _load_json(rerun / "downtime_summary.json") == summary
        assert _load_json(rerun / "service_windows.json") == windows
        assert _load_jsonl(rerun / "incident_queue.jsonl") == queue_rows


def test_pipeline_supports_custom_output_dir():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "custom"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(output_dir=out)
        assert result.returncode == 0, result.stderr
        files = {p.name for p in out.iterdir() if p.is_file()}
        assert files == {"downtime_summary.json", "service_windows.json", "incident_queue.jsonl"}


def test_cli_defaults_work_and_match_explicit_run():
    with tempfile.TemporaryDirectory() as tmp:
        explicit_out = Path(tmp) / "explicit"
        explicit_out.mkdir(parents=True, exist_ok=True)
        explicit = _run_pipeline(input_path=INPUT_PATH, output_dir=explicit_out)
        assert explicit.returncode == 0, explicit.stderr

        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        implicit = subprocess.run(["python3", str(PIPELINE)], capture_output=True, text=True, timeout=60)
        assert implicit.returncode == 0, implicit.stderr
        assert _load_json(SUMMARY_PATH) == _load_json(explicit_out / "downtime_summary.json")
        assert _load_json(WINDOWS_PATH) == _load_json(explicit_out / "service_windows.json")
        assert _load_jsonl(QUEUE_PATH) == _load_jsonl(explicit_out / "incident_queue.jsonl")


def test_maintenance_source_path_affects_output():
    original = MAINTENANCE_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nomaint"
            out.mkdir(parents=True, exist_ok=True)
            result = _run_pipeline(output_dir=out)
            assert result.returncode == 0, result.stderr
            summary = _load_json(out / "downtime_summary.json")
            assert summary["total_maintenance_overlap_ms"] == 0
            assert summary["total_maintenance_span_count"] == 0
    finally:
        MAINTENANCE_PATH.write_text(original)


def test_policy_source_path_affects_output():
    original = POLICY_PATH.read_text()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            out_a = Path(tmp) / "a"
            out_b = Path(tmp) / "b"
            out_a.mkdir(parents=True, exist_ok=True)
            out_b.mkdir(parents=True, exist_ok=True)
            result_a = _run_pipeline(output_dir=out_a)
            assert result_a.returncode == 0, result_a.stderr
            summary_a = _load_json(out_a / "downtime_summary.json")
            queue_a = _load_jsonl(out_a / "incident_queue.jsonl")

            strict_policy = {
                "default": {
                    "queue_min_effective_ms": 10000,
                    "critical_p1_min_ms": 10000,
                    "critical_threshold_ms": 10000,
                    "high_threshold_ms": 10000,
                    "no_overlap_high_duration_ms": 10000,
                    "critical_count_for_critical": 10,
                    "no_overlap_bonus": 0,
                    "segment_bonus": 0,
                    "severity_weight": {"critical": 1, "major": 1, "minor": 1},
                    "score_threshold_critical": 999,
                    "score_threshold_high": 999
                },
                "service_overrides": {}
            }
            _write_json(POLICY_PATH, strict_policy)
            result_b = _run_pipeline(output_dir=out_b)
            assert result_b.returncode == 0, result_b.stderr
            summary_b = _load_json(out_b / "downtime_summary.json")
            queue_b = _load_jsonl(out_b / "incident_queue.jsonl")
            assert summary_a["queued_window_count"] > summary_b["queued_window_count"]
            assert len(queue_b) == 0
            assert summary_a["policy_checksum"] != summary_b["policy_checksum"]
            assert len(queue_a) > 0
    finally:
        POLICY_PATH.write_text(original)


def test_exception_source_path_affects_output():
    original = EXCEPTIONS_PATH.read_text()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            out_a = Path(tmp) / "a"
            out_b = Path(tmp) / "b"
            out_a.mkdir(parents=True, exist_ok=True)
            out_b.mkdir(parents=True, exist_ok=True)
            result_a = _run_pipeline(output_dir=out_a)
            assert result_a.returncode == 0, result_a.stderr
            summary_a = _load_json(out_a / "downtime_summary.json")
            queue_a = _load_jsonl(out_a / "incident_queue.jsonl")

            EXCEPTIONS_PATH.write_text("[]\n")
            result_b = _run_pipeline(output_dir=out_b)
            assert result_b.returncode == 0, result_b.stderr
            summary_b = _load_json(out_b / "downtime_summary.json")
            queue_b = _load_jsonl(out_b / "incident_queue.jsonl")
            assert summary_a["exception_compaction_checksum"] != summary_b["exception_compaction_checksum"]
            assert summary_a["total_boost_overlap_ms"] != summary_b["total_boost_overlap_ms"]
            assert summary_a["total_suppression_overlap_ms"] != summary_b["total_suppression_overlap_ms"]
            assert queue_a != queue_b
    finally:
        EXCEPTIONS_PATH.write_text(original)


def test_maintenance_compaction_and_span_count_exercised():
    original = MAINTENANCE_PATH.read_text()
    try:
        maintenance_rows = [
            {"service": "billing", "start_ms": 100, "end_ms": 150},
            {"service": "billing", "start_ms": 140, "end_ms": 170},
            {"service": "payments", "start_ms": 170, "end_ms": 190},
            {"service": "billing", "start_ms": 210, "end_ms": 240},
        ]
        _write_json(MAINTENANCE_PATH, maintenance_rows)

        rows = [
            {
                "incident_id": "m1",
                "service": "billing",
                "start_ms": 50,
                "end_ms": 300,
                "severity": "major",
                "planned": False,
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            in_path = Path(tmp) / "in.json"
            out = Path(tmp) / "out"
            _write_json(in_path, rows)
            out.mkdir(parents=True, exist_ok=True)
            result = _run_pipeline(input_path=in_path, output_dir=out)
            assert result.returncode == 0, result.stderr
            windows = _load_json(out / "service_windows.json")
            block = windows["billing"][0]
            assert block["maintenance_overlap_ms"] == 120
            assert block["maintenance_span_count"] == 2
    finally:
        MAINTENANCE_PATH.write_text(original)


def test_dedupe_tie_break_chain_exercised():
    original = MAINTENANCE_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        rows = [
            {"incident_id": "d1", "service": "payments", "start_ms": 100, "end_ms": 200, "severity": "major", "planned": True},
            {"incident_id": "d1", "service": "billing", "start_ms": 120, "end_ms": 200, "severity": "major", "planned": False},
            {"incident_id": "d1", "service": "auth", "start_ms": 130, "end_ms": 200, "severity": "critical", "planned": False},
            {"incident_id": "d1", "service": "billing", "start_ms": 130, "end_ms": 200, "severity": "critical", "planned": False},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            in_path = Path(tmp) / "in.json"
            out = Path(tmp) / "out"
            _write_json(in_path, rows)
            out.mkdir(parents=True, exist_ok=True)
            result = _run_pipeline(input_path=in_path, output_dir=out)
            assert result.returncode == 0, result.stderr
            windows = _load_json(out / "service_windows.json")
            assert list(windows.keys()) == ["billing"]
            block = windows["billing"][0]
            assert block["start_ms"] == 130
            assert block["max_severity"] == "critical"
            assert block["source_incident_ids"] == ["d1"]
    finally:
        MAINTENANCE_PATH.write_text(original)


def test_planned_coercion_aliases_and_unknown_severity_exercised():
    original = MAINTENANCE_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        rows = [
            {"incident_id": "p1", "service": "authentication", "start_ms": 10, "end_ms": 300, "severity": "major", "planned": "no"},
            {"incident_id": "p2", "service": "search-api", "start_ms": 20, "end_ms": 260, "severity": "weird", "planned": "yes"},
            {"incident_id": "p3", "service": "payments", "start_ms": 30, "end_ms": 280, "severity": "critical", "planned": 2},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            in_path = Path(tmp) / "in.json"
            out = Path(tmp) / "out"
            _write_json(in_path, rows)
            out.mkdir(parents=True, exist_ok=True)
            result = _run_pipeline(input_path=in_path, output_dir=out)
            assert result.returncode == 0, result.stderr
            summary = _load_json(out / "downtime_summary.json")
            windows = _load_json(out / "service_windows.json")
            assert summary["planned_excluded_count"] == 2
            assert summary["severity_counts"] == {"critical": 1, "major": 1, "minor": 1}
            assert list(windows.keys()) == ["auth"]
    finally:
        MAINTENANCE_PATH.write_text(original)


def test_exception_compaction_and_balance_exercised():
    original_maint = MAINTENANCE_PATH.read_text()
    original_ex = EXCEPTIONS_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        _write_json(
            EXCEPTIONS_PATH,
            [
                {"service": "search-api", "start_ms": 100, "end_ms": 180, "action": "boost"},
                {"service": "search", "start_ms": 170, "end_ms": 220, "action": "boost"},
                {"service": "search", "start_ms": 210, "end_ms": 260, "action": "suppress"},
                {"service": "search", "start_ms": 260, "end_ms": 280, "action": "suppress"},
                {"service": "search", "start_ms": 280, "end_ms": 280, "action": "boost"},
            ],
        )
        rows = [
            {
                "incident_id": "e1",
                "service": "search",
                "start_ms": 90,
                "end_ms": 360,
                "severity": "major",
                "planned": False,
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            in_path = Path(tmp) / "in.json"
            out = Path(tmp) / "out"
            _write_json(in_path, rows)
            out.mkdir(parents=True, exist_ok=True)
            result = _run_pipeline(input_path=in_path, output_dir=out)
            assert result.returncode == 0, result.stderr
            windows = _load_json(out / "service_windows.json")
            queue = _load_jsonl(out / "incident_queue.jsonl")
            block = windows["search"][0]
            assert block["boost_overlap_ms"] == 120
            assert block["suppression_overlap_ms"] == 60
            assert queue[0]["effective_queue_min_ms"] == 220
            assert queue[0]["exception_balance_score"] == 1
    finally:
        MAINTENANCE_PATH.write_text(original_maint)
        EXCEPTIONS_PATH.write_text(original_ex)


def test_effective_queue_threshold_uses_exception_units_and_ceil_suppress():
    original_maint = MAINTENANCE_PATH.read_text()
    original_ex = EXCEPTIONS_PATH.read_text()
    original_policy = POLICY_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        _write_json(
            EXCEPTIONS_PATH,
            [
                {"service": "auth", "start_ms": 0, "end_ms": 120, "action": "suppress"},
                {"service": "authentication", "start_ms": 60, "end_ms": 180, "action": "boost"},
            ],
        )
        _write_json(
            POLICY_PATH,
            {
                "default": {
                    "queue_min_effective_ms": 250,
                    "critical_p1_min_ms": 280,
                    "critical_threshold_ms": 650,
                    "high_threshold_ms": 320,
                    "no_overlap_high_duration_ms": 450,
                    "critical_count_for_critical": 2,
                    "no_overlap_bonus": 0,
                    "segment_bonus": 0,
                    "suppress_penalty_ms": 50,
                    "boost_credit_ms": 20,
                    "suppress_unit_ms": 50,
                    "boost_unit_ms": 40,
                    "min_queue_floor_ms": 150,
                    "boost_force_critical_ms": 999,
                    "boost_high_relief_ms": 30,
                    "severity_weight": {"critical": 5, "major": 3, "minor": 1},
                    "score_threshold_critical": 999,
                    "score_threshold_high": 999
                },
                "service_overrides": {}
            },
        )
        rows = [
            {
                "incident_id": "q1",
                "service": "auth",
                "start_ms": 0,
                "end_ms": 300,
                "severity": "major",
                "planned": False,
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            in_path = Path(tmp) / "in.json"
            out = Path(tmp) / "out"
            _write_json(in_path, rows)
            out.mkdir(parents=True, exist_ok=True)
            result = _run_pipeline(input_path=in_path, output_dir=out)
            assert result.returncode == 0, result.stderr
            queue = _load_jsonl(out / "incident_queue.jsonl")
            assert len(queue) == 1
            row = queue[0]
            assert row["effective_queue_min_ms"] == 290
            assert row["exception_balance_score"] == 1
            assert row["priority"] == "high"
    finally:
        MAINTENANCE_PATH.write_text(original_maint)
        EXCEPTIONS_PATH.write_text(original_ex)
        POLICY_PATH.write_text(original_policy)

