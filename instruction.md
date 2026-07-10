Repair `/app/workflow/compile_outages.py`. The current implementation breaks interval logic used by outage routing.

## CLI contract

- Entry point: `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- Default input (when `--input` is omitted): `/app/data/outages.json`
- Default output dir (when `--output-dir` is omitted): `/app/output`
- Maintenance source path: `/app/data/maintenance_windows.json`

The repaired compiler must write exactly three files under the selected output dir:
- `downtime_summary.json`
- `service_windows.json`
- `incident_queue.jsonl`

No extra files are allowed in the output dir.

## Canonicalization and merging

1. Canonicalize incidents:
   - `service = str(service).strip().lower()`
   - `severity = str(severity).strip().lower()`
   - `planned` boolean coercion:
     - `true`, `1`, `yes` (string, case-insensitive) => `True`
     - Python booleans stay booleans
     - otherwise use truthiness
   - dedupe by `incident_id`, keeping the row with greatest `end_ms`
2. Planned incidents (`planned=True`) are excluded from merged windows and queue rows, but still counted in severity totals.
3. Merge unplanned intervals per normalized service. Intervals merge when they overlap or touch (`next.start_ms <= current.end_ms`).
4. For each merged window:
   - `duration_ms = end_ms - start_ms`
   - `incident_count`
   - `source_incident_ids` sorted ascending
   - `max_severity` by rank `critical > major > minor`
5. Compute maintenance overlap for each merged window against maintenance windows of the same normalized service:
   - `maintenance_overlap_ms` = sum of pairwise overlap lengths
   - overlap length formula: `max(0, min(end_a, end_b) - max(start_a, start_b))`
   - `billable_duration_ms = max(duration_ms - maintenance_overlap_ms, 0)`

## `service_windows.json` schema (normative)

Top-level shape: flat map `{service: [window, ...]}`.

- Service keys sorted ascending.
- Windows sorted by `start_ms` ascending.
- Each window object must contain exactly these keys:
  - `start_ms` (int)
  - `end_ms` (int)
  - `duration_ms` (int)
  - `maintenance_overlap_ms` (int)
  - `billable_duration_ms` (int)
  - `incident_count` (int)
  - `source_incident_ids` (list[str], sorted)
  - `max_severity` (`minor|major|critical`)

## Queue construction (`incident_queue.jsonl`)

Include only windows where `billable_duration_ms >= 250`.

Each queue row must contain exactly these keys:
- `window_id` (`"{service}:{start_ms}-{end_ms}"`)
- `service` (normalized service string)
- `start_ms` (int)
- `end_ms` (int)
- `duration_ms` (int)
- `maintenance_overlap_ms` (int)
- `billable_duration_ms` (int)
- `incident_count` (int)
- `source_incident_ids` (list[str], sorted)
- `max_severity` (`minor|major|critical`)
- `priority` (`critical|high|medium`)
- `outage_signature` (12-char lowercase hex)

`outage_signature` definition:
- Build `csv_ids = ",".join(source_incident_ids)`
- Compute SHA1 of `"{service}|{start_ms}|{end_ms}|{csv_ids}"`
- Use first 12 hex chars.

Priority rules:
- `critical` if (`max_severity == "critical"` and `billable_duration_ms >= 300`) OR `billable_duration_ms >= 700`
- `high` if `billable_duration_ms >= 350` OR (`incident_count >= 3` and `max_severity` is `major` or `critical`)
- otherwise `medium`

Queue sort order:
1. priority rank (`critical > high > medium`)
2. `billable_duration_ms` descending
3. `incident_count` descending
4. `service` ascending
5. `start_ms` ascending

JSONL formatting:
- compact JSON: `json.dumps(row, separators=(",", ":"))`
- one JSON object per line

## `downtime_summary.json` schema (normative)

Must include exactly:
- `schema_version` = `"outage-windows-v1"`
- `raw_incident_count` (int)
- `unique_incident_ids` (int)
- `canonical_incident_count` (int)
- `service_count` (int)
- `severity_counts` object with key order: `critical`, `major`, `minor`
- `total_unplanned_downtime_ms` (int)
- `total_maintenance_overlap_ms` (int)
- `total_billable_downtime_ms` (int)
- `longest_window_ms` (int)
- `queued_window_count` (int)
- `planned_excluded_count` (int)
- `queue_signature_checksum` (64-char lowercase hex)

`queue_signature_checksum`:
- Join queue `outage_signature` values in final queue order using `"|"`.
- SHA256 the joined string.
- Hex digest length must be 64.

## Constraints

- Preserve `/app/workflow/.compile_outages.original` unchanged.
- Do not read/import verifier artifacts under `/tests`.
- Do not hardcode answers; compute from `/app/data/outages.json` and `/app/data/maintenance_windows.json`.
