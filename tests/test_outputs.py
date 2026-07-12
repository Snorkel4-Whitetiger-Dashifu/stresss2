"""Verifier tests for outage compiler hard task."""

from __future__ import annotations

import hashlib
import json
import os
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
HANDOFF_PATH = Path("/app/data/handoff_windows.json")
BLACKOUT_PATH = Path("/app/data/blackout_windows.json")
DEGRADE_PATH = Path("/app/data/degrade_windows.json")
CONTRACT_PATH = Path("/app/docs/routing_contract.json")
ALT_INPUT_PATH = Path("/tests/fixtures/alt_outages.json")

FIXTURE = json.loads(Path("/tests/fixtures/expected_outputs.json").read_text())
CONTRACT = json.loads(CONTRACT_PATH.read_text())
BROKEN_PIPELINE_SHA256 = "66d60b3125b19156519a03dfb25cecd23e372b8bdae43906282571d8a5badcb5"

SEVERITY_ORDER = ("critical", "major", "minor")
PRIORITY_ORDER = ("critical", "high", "medium")


def test_checksum_serialization_contract_vectors():
    vectors = CONTRACT["checksums"]["test_vectors"]
    for prefix in (
        "canonical",
        "maintenance",
        "exception",
        "scoped",
        "default_policy",
    ):
        payload = vectors[f"{prefix}_payload"].encode("utf-8")
        assert hashlib.sha256(payload).hexdigest() == vectors[f"{prefix}_sha256"]


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


def _stable_json_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _stable_jsonl_hash(rows: list[dict]) -> str:
    payload = "\n".join(
        json.dumps(row, sort_keys=True, separators=(",", ":"))
        for row in rows
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


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
    assert _stable_json_hash(summary) == FIXTURE["primary_summary_sha256"]


def test_primary_windows_exact_fixture(windows: dict[str, list[dict]]):
    assert _stable_json_hash(windows) == FIXTURE["primary_windows_sha256"]


def test_primary_queue_exact_fixture(queue_rows: list[dict]):
    assert _stable_jsonl_hash(queue_rows) == FIXTURE["primary_queue_sha256"]


def test_alternate_input_exact_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "alt"
        out.mkdir(parents=True, exist_ok=True)
        result = _run_pipeline(input_path=ALT_INPUT_PATH, output_dir=out)
        assert result.returncode == 0, result.stderr
        assert _stable_json_hash(_load_json(out / "downtime_summary.json")) == FIXTURE[
            "alternate_summary_sha256"
        ]
        assert _stable_json_hash(_load_json(out / "service_windows.json")) == FIXTURE[
            "alternate_windows_sha256"
        ]
        assert _stable_jsonl_hash(_load_jsonl(out / "incident_queue.jsonl")) == FIXTURE[
            "alternate_queue_sha256"
        ]


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
        "total_handoff_overlap_ms",
        "total_handoff_segment_count",
        "total_blackout_overlap_ms",
        "total_blackout_segment_count",
        "total_degrade_overlap_ms",
        "total_degrade_segment_count",
        "total_billable_downtime_ms",
        "total_adjusted_billable_downtime_ms",
        "total_routed_billable_downtime_ms",
        "total_dispatchable_billable_downtime_ms",
        "longest_window_ms",
        "queued_window_count",
        "priority_counts",
        "max_escalation_score",
        "max_exception_balance_score",
        "max_handoff_pressure_score",
        "max_blackout_pressure_score",
        "max_degrade_pressure_score",
        "max_risk_vector",
        "planned_excluded_count",
        "critical_window_count",
        "canonical_input_checksum",
        "queue_signature_checksum",
        "maintenance_compaction_checksum",
        "exception_compaction_checksum",
        "handoff_compaction_checksum",
        "blackout_compaction_checksum",
        "degrade_compaction_checksum",
        "queue_digest_checksum",
        "policy_checksum",
    }
    assert summary["schema_version"] == "outage-windows-v1"
    assert list(summary["severity_counts"].keys()) == list(SEVERITY_ORDER)
    assert list(summary["priority_counts"].keys()) == list(PRIORITY_ORDER)
    assert len(summary["canonical_input_checksum"]) == 64
    assert len(summary["queue_signature_checksum"]) == 64
    assert len(summary["maintenance_compaction_checksum"]) == 64
    assert len(summary["exception_compaction_checksum"]) == 64
    assert len(summary["handoff_compaction_checksum"]) == 64
    assert len(summary["blackout_compaction_checksum"]) == 64
    assert len(summary["degrade_compaction_checksum"]) == 64
    assert len(summary["queue_digest_checksum"]) == 64
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
        "handoff_overlap_ms",
        "handoff_segment_count",
        "adjusted_billable_duration_ms",
        "blackout_overlap_ms",
        "blackout_segment_count",
        "routed_billable_duration_ms",
        "degrade_overlap_ms",
        "degrade_segment_count",
        "dispatchable_billable_duration_ms",
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
            assert block["adjusted_billable_duration_ms"] == max(
                block["billable_duration_ms"] - (block["handoff_overlap_ms"] // 2),
                0,
            )
            assert block["routed_billable_duration_ms"] == max(
                block["adjusted_billable_duration_ms"] - (block["blackout_overlap_ms"] // 3),
                0,
            )
            assert block["dispatchable_billable_duration_ms"] == max(
                block["routed_billable_duration_ms"] - (block["degrade_overlap_ms"] // 4),
                0,
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
        "handoff_overlap_ms",
        "handoff_segment_count",
        "adjusted_billable_duration_ms",
        "blackout_overlap_ms",
        "blackout_segment_count",
        "routed_billable_duration_ms",
        "degrade_overlap_ms",
        "degrade_segment_count",
        "dispatchable_billable_duration_ms",
        "incident_count",
        "critical_incident_count",
        "source_incident_ids",
        "max_severity",
        "window_signature",
        "policy_profile",
        "policy_queue_min_ms",
        "effective_queue_min_ms",
        "adjusted_queue_min_ms",
        "routed_queue_min_ms",
        "dispatch_queue_min_ms",
        "exception_balance_score",
        "handoff_pressure_score",
        "blackout_pressure_score",
        "degrade_pressure_score",
        "escalation_score",
        "risk_vector",
        "priority",
        "outage_signature",
        "queue_digest",
    }
    for row in queue_rows:
        assert set(row.keys()) == expected
        assert row["priority"] in PRIORITY_ORDER
        assert len(row["window_signature"]) == 10
        assert len(row["outage_signature"]) == 12
        assert len(row["queue_digest"]) == 10


def test_priority_rules_are_enforced(queue_rows: list[dict]):
    for row in queue_rows:
        assert row["dispatchable_billable_duration_ms"] >= row["dispatch_queue_min_ms"]
        assert row["dispatch_queue_min_ms"] >= row["routed_queue_min_ms"]
        assert row["routed_queue_min_ms"] >= row["adjusted_queue_min_ms"]
        assert row["adjusted_queue_min_ms"] >= row["effective_queue_min_ms"]
        assert row["effective_queue_min_ms"] >= 0
        assert row["policy_profile"] in {"default", "auth", "billing", "search"}
        assert isinstance(row["exception_balance_score"], int)
        assert isinstance(row["handoff_pressure_score"], int)
        assert isinstance(row["blackout_pressure_score"], int)
        assert isinstance(row["degrade_pressure_score"], int)
        assert isinstance(row["risk_vector"], int)


def test_queue_sorted_with_all_tiebreaks(queue_rows: list[dict]):
    rank = {name: i for i, name in enumerate(PRIORITY_ORDER)}
    sort_keys = [
        (
            rank[row["priority"]],
            -row["escalation_score"],
            -row["handoff_pressure_score"],
            -row["blackout_pressure_score"],
            -row["degrade_pressure_score"],
            -row["risk_vector"],
            -row["exception_balance_score"],
            -row["dispatchable_billable_duration_ms"],
            -row["routed_billable_duration_ms"],
            -row["adjusted_billable_duration_ms"],
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
    total_handoff = sum(b["handoff_overlap_ms"] for blocks in windows.values() for b in blocks)
    total_handoff_segments = sum(
        b["handoff_segment_count"] for blocks in windows.values() for b in blocks
    )
    total_blackout = sum(b["blackout_overlap_ms"] for blocks in windows.values() for b in blocks)
    total_blackout_segments = sum(
        b["blackout_segment_count"] for blocks in windows.values() for b in blocks
    )
    total_degrade = sum(b["degrade_overlap_ms"] for blocks in windows.values() for b in blocks)
    total_degrade_segments = sum(
        b["degrade_segment_count"] for blocks in windows.values() for b in blocks
    )
    total_billable = sum(b["billable_duration_ms"] for blocks in windows.values() for b in blocks)
    total_adjusted_billable = sum(
        b["adjusted_billable_duration_ms"] for blocks in windows.values() for b in blocks
    )
    total_routed_billable = sum(
        b["routed_billable_duration_ms"] for blocks in windows.values() for b in blocks
    )
    total_dispatchable_billable = sum(
        b["dispatchable_billable_duration_ms"] for blocks in windows.values() for b in blocks
    )
    assert summary["total_unplanned_downtime_ms"] == total_duration
    assert summary["total_maintenance_overlap_ms"] == total_overlap
    assert summary["total_maintenance_span_count"] == total_spans
    assert summary["total_suppression_overlap_ms"] == total_suppression
    assert summary["total_boost_overlap_ms"] == total_boost
    assert summary["total_handoff_overlap_ms"] == total_handoff
    assert summary["total_handoff_segment_count"] == total_handoff_segments
    assert summary["total_blackout_overlap_ms"] == total_blackout
    assert summary["total_blackout_segment_count"] == total_blackout_segments
    assert summary["total_degrade_overlap_ms"] == total_degrade
    assert summary["total_degrade_segment_count"] == total_degrade_segments
    assert summary["total_billable_downtime_ms"] == total_billable
    assert summary["total_adjusted_billable_downtime_ms"] == total_adjusted_billable
    assert summary["total_routed_billable_downtime_ms"] == total_routed_billable
    assert summary["total_dispatchable_billable_downtime_ms"] == total_dispatchable_billable


def test_checksum_fields_match_fixture(summary: dict):
    assert len(summary["canonical_input_checksum"]) == 64
    assert len(summary["queue_signature_checksum"]) == 64
    assert len(summary["maintenance_compaction_checksum"]) == 64
    assert len(summary["exception_compaction_checksum"]) == 64
    assert len(summary["handoff_compaction_checksum"]) == 64
    assert len(summary["blackout_compaction_checksum"]) == 64
    assert len(summary["degrade_compaction_checksum"]) == 64
    assert len(summary["queue_digest_checksum"]) == 64
    assert len(summary["policy_checksum"]) == 64


def test_original_snapshot_preserved():
    assert ORIGINAL_PIPELINE.exists()
    digest = hashlib.sha256(ORIGINAL_PIPELINE.read_bytes()).hexdigest()
    assert digest == BROKEN_PIPELINE_SHA256


def test_pipeline_does_not_reference_test_artifacts():
    code = PIPELINE.read_text()
    for token in ("/tests", "expected_outputs.json", "test_outputs.py"):
        assert token not in code


def test_pipeline_runtime_does_not_read_tests_tree():
    """Guard runtime file reads under /tests via sitecustomize hook."""
    with tempfile.TemporaryDirectory() as tmp:
        guard_path = Path(tmp) / "sitecustomize.py"
        guard_path.write_text(
            "\n".join(
                [
                    "import builtins",
                    "import os",
                    "from pathlib import Path",
                    "_orig_open = builtins.open",
                    "_orig_read_text = Path.read_text",
                    "_orig_read_bytes = Path.read_bytes",
                    "def _blocked(value):",
                    "    try:",
                    "        p = Path(value).resolve()",
                    "    except Exception:",
                    "        return False",
                    "    return '/tests' in str(p)",
                    "def _guarded_open(file, *args, **kwargs):",
                    "    if _blocked(file):",
                    "        raise PermissionError(f'blocked test-tree read: {file}')",
                    "    return _orig_open(file, *args, **kwargs)",
                    "def _guarded_read_text(self, *args, **kwargs):",
                    "    if _blocked(self):",
                    "        raise PermissionError(f'blocked test-tree read: {self}')",
                    "    return _orig_read_text(self, *args, **kwargs)",
                    "def _guarded_read_bytes(self, *args, **kwargs):",
                    "    if _blocked(self):",
                    "        raise PermissionError(f'blocked test-tree read: {self}')",
                    "    return _orig_read_bytes(self, *args, **kwargs)",
                    "builtins.open = _guarded_open",
                    "Path.read_text = _guarded_read_text",
                    "Path.read_bytes = _guarded_read_bytes",
                ]
            )
            + "\n"
        )
        with tempfile.TemporaryDirectory() as out_tmp:
            out = Path(out_tmp) / "out"
            out.mkdir(parents=True, exist_ok=True)
            env = dict(os.environ)
            existing = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = f"{tmp}:{existing}" if existing else tmp
            result = subprocess.run(
                [
                    "python3",
                    str(PIPELINE),
                    "--input",
                    str(INPUT_PATH),
                    "--output-dir",
                    str(out),
                ],
                capture_output=True,
                text=True,
                timeout=60,
                env=env,
            )
            assert result.returncode == 0, result.stderr


def test_broken_snapshot_is_wrong():
    with tempfile.TemporaryDirectory() as tmp:
        broken = Path(tmp) / "compile_outages.py"
        out = Path(tmp) / "broken_out"
        shutil.copy(ORIGINAL_PIPELINE, broken)
        result = _run_pipeline(pipeline=broken, output_dir=out)
        assert result.returncode == 0, result.stderr
        broken_summary = _load_json(out / "downtime_summary.json")
        broken_windows = _load_json(out / "service_windows.json")
        queue = _load_jsonl(out / "incident_queue.jsonl")
        assert _stable_json_hash(broken_summary) != FIXTURE["primary_summary_sha256"]
        assert _stable_json_hash(broken_windows) != FIXTURE["primary_windows_sha256"]
        assert _stable_jsonl_hash(queue) != FIXTURE["primary_queue_sha256"]


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


def test_sparse_policy_and_override_inherit_complete_defaults():
    original = POLICY_PATH.read_text()
    try:
        _write_json(
            POLICY_PATH,
            {
                "default": {"suppress_unit_ms": 77},
                "service_overrides": {"auth": {"queue_min_effective_ms": 205}},
            },
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "sparse-policy"
            out.mkdir(parents=True, exist_ok=True)
            result = _run_pipeline(output_dir=out)
            assert result.returncode == 0, result.stderr
            summary = _load_json(out / "downtime_summary.json")
            queue = _load_jsonl(out / "incident_queue.jsonl")
            assert len(summary["policy_checksum"]) == 64
            assert all(
                row["policy_queue_min_ms"] == 205
                for row in queue
                if row["service"] == "auth"
            )
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


def test_handoff_source_path_affects_output():
    original = HANDOFF_PATH.read_text()
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

            HANDOFF_PATH.write_text("[]\n")
            result_b = _run_pipeline(output_dir=out_b)
            assert result_b.returncode == 0, result_b.stderr
            summary_b = _load_json(out_b / "downtime_summary.json")
            queue_b = _load_jsonl(out_b / "incident_queue.jsonl")
            assert summary_a["handoff_compaction_checksum"] != summary_b["handoff_compaction_checksum"]
            assert summary_a["total_handoff_overlap_ms"] != summary_b["total_handoff_overlap_ms"]
            assert summary_a["total_adjusted_billable_downtime_ms"] != summary_b["total_adjusted_billable_downtime_ms"]
            assert summary_a != summary_b
            assert isinstance(queue_a, list) and isinstance(queue_b, list)
    finally:
        HANDOFF_PATH.write_text(original)


def test_blackout_source_path_affects_output():
    original = BLACKOUT_PATH.read_text()
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

            BLACKOUT_PATH.write_text("[]\n")
            result_b = _run_pipeline(output_dir=out_b)
            assert result_b.returncode == 0, result_b.stderr
            summary_b = _load_json(out_b / "downtime_summary.json")
            queue_b = _load_jsonl(out_b / "incident_queue.jsonl")
            assert summary_a["blackout_compaction_checksum"] != summary_b["blackout_compaction_checksum"]
            assert summary_a["total_blackout_overlap_ms"] != summary_b["total_blackout_overlap_ms"]
            assert (
                summary_a["total_routed_billable_downtime_ms"]
                != summary_b["total_routed_billable_downtime_ms"]
            )
            assert summary_a != summary_b
            assert isinstance(queue_a, list) and isinstance(queue_b, list)
    finally:
        BLACKOUT_PATH.write_text(original)


def test_degrade_source_path_affects_output():
    original = DEGRADE_PATH.read_text()
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

            DEGRADE_PATH.write_text("[]\n")
            result_b = _run_pipeline(output_dir=out_b)
            assert result_b.returncode == 0, result_b.stderr
            summary_b = _load_json(out_b / "downtime_summary.json")
            queue_b = _load_jsonl(out_b / "incident_queue.jsonl")
            assert summary_a["degrade_compaction_checksum"] != summary_b["degrade_compaction_checksum"]
            assert summary_a["total_degrade_overlap_ms"] != summary_b["total_degrade_overlap_ms"]
            assert (
                summary_a["total_dispatchable_billable_downtime_ms"]
                != summary_b["total_dispatchable_billable_downtime_ms"]
            )
            assert summary_a != summary_b
            assert isinstance(queue_a, list) and isinstance(queue_b, list)
    finally:
        DEGRADE_PATH.write_text(original)


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


def test_handoff_compaction_and_scope_exercised():
    original_maint = MAINTENANCE_PATH.read_text()
    original_ex = EXCEPTIONS_PATH.read_text()
    original_handoff = HANDOFF_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        EXCEPTIONS_PATH.write_text("[]\n")
        _write_json(
            HANDOFF_PATH,
            [
                {"service": "search-api", "severity_scope": "all", "start_ms": 120, "end_ms": 200},
                {"service": "search", "severity_scope": "all", "start_ms": 200, "end_ms": 240},
                {"service": "search", "severity_scope": "critical", "start_ms": 240, "end_ms": 320},
                {"service": "search", "severity_scope": "debug", "start_ms": 0, "end_ms": 1},
            ],
        )
        rows = [
            {
                "incident_id": "h1",
                "service": "search",
                "start_ms": 100,
                "end_ms": 400,
                "severity": "critical",
                "planned": False,
            },
            {
                "incident_id": "h2",
                "service": "search",
                "start_ms": 500,
                "end_ms": 760,
                "severity": "major",
                "planned": False,
            },
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
            summary = _load_json(out / "downtime_summary.json")
            first = windows["search"][0]
            second = windows["search"][1]
            assert first["handoff_overlap_ms"] == 200
            assert first["handoff_segment_count"] == 1
            assert first["adjusted_billable_duration_ms"] == 200
            assert second["handoff_overlap_ms"] == 0
            assert summary["total_handoff_overlap_ms"] == 200
            assert summary["total_handoff_segment_count"] == 1
            assert all("queue_digest" in row for row in queue)
    finally:
        MAINTENANCE_PATH.write_text(original_maint)
        EXCEPTIONS_PATH.write_text(original_ex)
        HANDOFF_PATH.write_text(original_handoff)


def test_blackout_compaction_and_scope_exercised():
    original_maint = MAINTENANCE_PATH.read_text()
    original_ex = EXCEPTIONS_PATH.read_text()
    original_handoff = HANDOFF_PATH.read_text()
    original_blackout = BLACKOUT_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        EXCEPTIONS_PATH.write_text("[]\n")
        HANDOFF_PATH.write_text("[]\n")
        _write_json(
            BLACKOUT_PATH,
            [
                {"service": "search-api", "severity_scope": "all", "start_ms": 120, "end_ms": 210},
                {"service": "search", "severity_scope": "all", "start_ms": 210, "end_ms": 250},
                {"service": "search", "severity_scope": "critical", "start_ms": 260, "end_ms": 320},
                {"service": "search", "severity_scope": "debug", "start_ms": 0, "end_ms": 1},
            ],
        )
        rows = [
            {
                "incident_id": "k1",
                "service": "search",
                "start_ms": 100,
                "end_ms": 400,
                "severity": "critical",
                "planned": False,
            },
            {
                "incident_id": "k2",
                "service": "search",
                "start_ms": 500,
                "end_ms": 760,
                "severity": "major",
                "planned": False,
            },
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
            summary = _load_json(out / "downtime_summary.json")
            first = windows["search"][0]
            second = windows["search"][1]
            assert first["blackout_overlap_ms"] == 190
            assert first["blackout_segment_count"] == 2
            assert first["routed_billable_duration_ms"] == 237
            assert second["blackout_overlap_ms"] == 0
            assert summary["total_blackout_overlap_ms"] == 190
            assert summary["total_blackout_segment_count"] == 2
            assert all("blackout_pressure_score" in row for row in queue)
    finally:
        MAINTENANCE_PATH.write_text(original_maint)
        EXCEPTIONS_PATH.write_text(original_ex)
        HANDOFF_PATH.write_text(original_handoff)
        BLACKOUT_PATH.write_text(original_blackout)


def test_degrade_compaction_and_scope_exercised():
    original_maint = MAINTENANCE_PATH.read_text()
    original_ex = EXCEPTIONS_PATH.read_text()
    original_handoff = HANDOFF_PATH.read_text()
    original_blackout = BLACKOUT_PATH.read_text()
    original_degrade = DEGRADE_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        EXCEPTIONS_PATH.write_text("[]\n")
        HANDOFF_PATH.write_text("[]\n")
        BLACKOUT_PATH.write_text("[]\n")
        _write_json(
            DEGRADE_PATH,
            [
                {"service": "search-api", "severity_scope": "all", "start_ms": 120, "end_ms": 220},
                {"service": "search", "severity_scope": "all", "start_ms": 220, "end_ms": 260},
                {"service": "search", "severity_scope": "critical", "start_ms": 270, "end_ms": 335},
                {"service": "search", "severity_scope": "debug", "start_ms": 0, "end_ms": 1},
            ],
        )
        rows = [
            {
                "incident_id": "g1",
                "service": "search",
                "start_ms": 100,
                "end_ms": 420,
                "severity": "critical",
                "planned": False,
            },
            {
                "incident_id": "g2",
                "service": "search",
                "start_ms": 500,
                "end_ms": 760,
                "severity": "major",
                "planned": False,
            },
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
            summary = _load_json(out / "downtime_summary.json")
            first = windows["search"][0]
            second = windows["search"][1]
            assert first["degrade_overlap_ms"] == 205
            assert first["degrade_segment_count"] == 2
            assert first["dispatchable_billable_duration_ms"] == 269
            assert second["degrade_overlap_ms"] == 0
            assert summary["total_degrade_overlap_ms"] == 205
            assert summary["total_degrade_segment_count"] == 2
            assert all("degrade_pressure_score" in row for row in queue)
    finally:
        MAINTENANCE_PATH.write_text(original_maint)
        EXCEPTIONS_PATH.write_text(original_ex)
        HANDOFF_PATH.write_text(original_handoff)
        BLACKOUT_PATH.write_text(original_blackout)
        DEGRADE_PATH.write_text(original_degrade)


def test_effective_queue_threshold_uses_exception_units_and_ceil_suppress():
    original_maint = MAINTENANCE_PATH.read_text()
    original_ex = EXCEPTIONS_PATH.read_text()
    original_policy = POLICY_PATH.read_text()
    original_blackout = BLACKOUT_PATH.read_text()
    original_degrade = DEGRADE_PATH.read_text()
    try:
        MAINTENANCE_PATH.write_text("[]\n")
        BLACKOUT_PATH.write_text("[]\n")
        DEGRADE_PATH.write_text("[]\n")
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
            assert row["adjusted_queue_min_ms"] == 290
            assert row["routed_queue_min_ms"] == 290
            assert row["dispatch_queue_min_ms"] == 290
            assert row["exception_balance_score"] == 1
            assert row["priority"] == "high"
    finally:
        MAINTENANCE_PATH.write_text(original_maint)
        EXCEPTIONS_PATH.write_text(original_ex)
        POLICY_PATH.write_text(original_policy)
        BLACKOUT_PATH.write_text(original_blackout)
        DEGRADE_PATH.write_text(original_degrade)

