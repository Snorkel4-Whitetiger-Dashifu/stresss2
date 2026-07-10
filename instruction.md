You are the on-call SRE fixing a broken outage rollup job used by pager routing. Repair `/app/workflow/compile_outages.py` so outputs are deterministic and satisfy strict routing math.

Keep the CLI contract exactly as-is:
- `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default input: `/app/data/outages.json`
- default output dir: `/app/output`
- maintenance windows are always loaded from `/app/data/maintenance_windows.json`

The run must write exactly three files (no extras): `downtime_summary.json`, `service_windows.json`, `incident_queue.jsonl`.

Processing requirements:
1. Canonicalize incidents:
   - normalize `service` and `severity` with `str(...).strip().lower()`
   - service aliases: `authentication -> auth`, `payments -> billing`, `search-api -> search`
   - normalize `start_ms` and `end_ms` with `int(str(...).strip())`; invalid values become `0`
   - if `end_ms < start_ms`, set `end_ms = start_ms`
   - normalize `planned`:
     - bool stays bool
     - strings: only `"true"`, `"1"`, `"yes"` are `True`; all other strings are `False`
     - non-string, non-bool values use Python `bool(value)`
   - normalize unknown severity to `minor`
2. Deduplicate by `incident_id`, keeping row with greatest `end_ms`.
   - tie-breaks in order:
     1) higher severity rank (`critical > major > minor`)
     2) prefer `planned == False`
     3) greater `start_ms`
     4) lexicographically greater normalized `service`
3. Build windows from unplanned incidents only (planned still counted in `severity_counts`).
   - merge per normalized service
   - stitch rule: merge when `next.start_ms <= current.end_ms + 30`
4. For each merged window compute:
   - `duration_ms = end_ms - start_ms`
   - `incident_count`
   - sorted `source_incident_ids`
   - `max_severity` by rank
   - `critical_incident_count`
   - `window_signature`: first 10 lowercase hex chars of SHA1 over `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}|{max_severity}"`
5. Maintenance overlap:
   - same-service windows only
   - overlap formula: `max(0, min(end_a, end_b) - max(start_a, start_b))`
   - `maintenance_overlap_ms`: summed overlap
   - `billable_duration_ms = max(duration_ms - maintenance_overlap_ms, 0)`

Queue behavior:
- include windows when `billable_duration_ms >= 220`
- `window_id`: `"{service}:{start_ms}-{end_ms}"`
- `outage_signature`: first 12 lowercase hex chars of SHA1 over `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}|{window_signature}"`
- priority:
  - `critical` if (`max_severity == "critical"` and `billable_duration_ms >= 280`) OR `billable_duration_ms >= 650` OR `critical_incident_count >= 2`
  - `high` if `billable_duration_ms >= 320` OR (`incident_count >= 3` and `max_severity` in `{"major", "critical"}`) OR (`maintenance_overlap_ms == 0` and `duration_ms >= 450`)
  - else `medium`
- sort order: priority rank (`critical > high > medium`), `billable_duration_ms` desc, `critical_incident_count` desc, `incident_count` desc, `service` asc, `start_ms` asc
- JSONL must be compact (`json.dumps(row, separators=(",", ":"))`)

Output contracts (exact keys):
- `service_windows.json`: flat `{service: [window, ...]}`; service keys asc, window list sorted by `start_ms` asc.
- each window must contain exactly:
  - `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `billable_duration_ms`, `incident_count`, `critical_incident_count`, `source_incident_ids`, `max_severity`, `window_signature`
- `incident_queue.jsonl` rows must contain exactly:
  - `window_id`, `service`, `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `billable_duration_ms`, `incident_count`, `critical_incident_count`, `source_incident_ids`, `max_severity`, `window_signature`, `priority`, `outage_signature`
- `downtime_summary.json` must contain exactly:
  - `schema_version`, `raw_incident_count`, `unique_incident_ids`, `canonical_incident_count`, `service_count`, `severity_counts`, `total_unplanned_downtime_ms`, `total_maintenance_overlap_ms`, `total_billable_downtime_ms`, `longest_window_ms`, `queued_window_count`, `planned_excluded_count`, `critical_window_count`, `canonical_input_checksum`, `queue_signature_checksum`

Summary specifics:
- `schema_version` is `"outage-windows-v1"`
- `severity_counts` key order: `critical`, `major`, `minor`
- `critical_window_count`: number of merged windows where `max_severity == "critical"`
- `canonical_input_checksum`: SHA256 over canonical rows in canonical order (`service`, `start_ms`, `incident_id`) using line format `incident_id|service|start_ms|end_ms|severity|planned_int`, `planned_int` in `{0,1}`
- `queue_signature_checksum`: lowercase SHA256 of `"|".join(outage_signature values in final queue order)`

Keep `/app/workflow/.compile_outages.original` unchanged and do not read/import verifier artifacts from `/tests`.
