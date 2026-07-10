Repair `/app/workflow/compile_outages.py` by fixing a regression in outage window compilation used by incident routing.

Keep the CLI behavior unchanged:
- command: `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default `--input`: `/app/data/outages.json`
- default `--output-dir`: `/app/output`
- maintenance data must be loaded from `/app/data/maintenance_windows.json`

The program must create exactly these files in the chosen output directory (and no extra files):
- `downtime_summary.json`
- `service_windows.json`
- `incident_queue.jsonl`

Use this processing flow.

1) Canonicalize and deduplicate incidents.
- normalize `service` and `severity` with `str(value).strip().lower()`
- coerce `planned` as:
  - string values `"true"`, `"1"`, `"yes"` (case-insensitive) => `True`
  - boolean values remain booleans
  - all other values use Python truthiness
- deduplicate by `incident_id`, keeping the row with largest `end_ms`

2) Build windows from unplanned incidents only.
- incidents with `planned=True` are excluded from merged windows and queue rows, but still counted in summary severity totals
- merge intervals per normalized service, including touching intervals (`next.start_ms <= current.end_ms`)
- each merged window computes:
  - `duration_ms = end_ms - start_ms`
  - `incident_count`
  - `source_incident_ids` sorted ascending
  - `max_severity` using rank `critical > major > minor`

3) Apply maintenance overlap (same normalized service only).
- overlap formula: `max(0, min(end_a, end_b) - max(start_a, start_b))`
- `maintenance_overlap_ms` is the sum of overlaps between a merged window and all service-matched maintenance windows
- `billable_duration_ms = max(duration_ms - maintenance_overlap_ms, 0)`

Output schema contracts:

`service_windows.json` is a flat map `{service: [window, ...]}` with services sorted ascending and windows sorted by `start_ms` ascending. Each window contains exactly:
`start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `billable_duration_ms`, `incident_count`, `source_incident_ids`, `max_severity`.

`incident_queue.jsonl` contains one compact JSON object per line (`json.dumps(row, separators=(",", ":"))`). Include only windows where `billable_duration_ms >= 250`. Each row contains exactly:
`window_id`, `service`, `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `billable_duration_ms`, `incident_count`, `source_incident_ids`, `max_severity`, `priority`, `outage_signature`.

Queue rules:
- `window_id = "{service}:{start_ms}-{end_ms}"`
- `outage_signature`: SHA1 of `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}"`, first 12 lowercase hex chars
- priority:
  - `critical` if (`max_severity == "critical"` and `billable_duration_ms >= 300`) or `billable_duration_ms >= 700`
  - `high` if `billable_duration_ms >= 350` or (`incident_count >= 3` and `max_severity` in `{"major", "critical"}`)
  - otherwise `medium`
- final queue sort key:
  1. priority rank (`critical > high > medium`)
  2. `billable_duration_ms` descending
  3. `incident_count` descending
  4. `service` ascending
  5. `start_ms` ascending

`downtime_summary.json` contains exactly:
`schema_version`, `raw_incident_count`, `unique_incident_ids`, `canonical_incident_count`, `service_count`, `severity_counts`, `total_unplanned_downtime_ms`, `total_maintenance_overlap_ms`, `total_billable_downtime_ms`, `longest_window_ms`, `queued_window_count`, `planned_excluded_count`, `queue_signature_checksum`.

Summary rules:
- `schema_version` must be `"outage-windows-v1"`
- `severity_counts` key order is `critical`, `major`, `minor`
- `queue_signature_checksum` is SHA256 of `"|".join(outage_signature values in final queue order)` and must be 64 lowercase hex chars

Constraints:
- preserve `/app/workflow/.compile_outages.original` unchanged
- do not read or import verifier artifacts from `/tests`
- do not hardcode answers; compute results from `/app/data/outages.json` and `/app/data/maintenance_windows.json`
