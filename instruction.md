The outage compiler in `/app/workflow/compile_outages.py` is wrong and must be repaired.

Keep the CLI interface:
- `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default input is `/app/data/outages.json`
- default output dir is `/app/output`

The repaired compiler must emit exactly three files under the output dir:
- `downtime_summary.json`
- `service_windows.json`
- `incident_queue.jsonl`

The compiler must also load maintenance windows from:
- `/app/data/maintenance_windows.json`

Required behavior:
1. Canonicalize incident records:
   - normalize `service` and `severity` with `strip().lower()`
   - normalize `planned` so boolean-like strings (`"true"`, `"1"`, `"yes"`) are treated as true
   - dedupe by `incident_id`, keeping the record with the highest `end_ms`
2. Planned incidents (`planned=true`) are excluded from merged windows and queue output, but still counted in `severity_counts`.
3. Merge unplanned intervals per service when intervals overlap or touch (`next.start_ms <= current.end_ms`).
4. For each merged window, compute:
   - `start_ms`, `end_ms`, `duration_ms` (`end_ms - start_ms`)
   - `incident_count`
   - `source_incident_ids` (sorted ascending)
   - `max_severity` using rank `critical > major > minor`
5. For each merged window, compute maintenance overlap against windows with the same normalized service:
   - `maintenance_overlap_ms` = total overlap with maintenance windows
   - `billable_duration_ms` = `max(duration_ms - maintenance_overlap_ms, 0)`
6. `service_windows.json` schema:
   - flat map `{service: [window, ...]}`
   - services sorted alphabetically
   - windows sorted by `start_ms`
   - each window has exactly:
     - `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `billable_duration_ms`
     - `incident_count`, `source_incident_ids`, `max_severity`
7. Queue rules:
   - include merged windows with `billable_duration_ms >= 250`
   - each queue row must include exactly:
     - `window_id` (format: `"{service}:{start_ms}-{end_ms}"`)
     - `service`, `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `billable_duration_ms`
     - `incident_count`, `source_incident_ids`, `max_severity`, `priority`, `outage_signature`
   - `outage_signature` = first 12 hex chars of `sha1("{service}|{start_ms}|{end_ms}|{csv_ids}")`
   - assign `priority`:
     - `critical` if (`max_severity == "critical"` and `billable_duration_ms >= 300`) OR `billable_duration_ms >= 700`
     - `high` if `billable_duration_ms >= 350` OR (`incident_count >= 3` and `max_severity` in `{"major","critical"}`)
     - otherwise `medium`
   - sort queue by priority (`critical > high > medium`), then `billable_duration_ms` descending, then `incident_count` descending, then `service` ascending, then `start_ms` ascending
   - write `incident_queue.jsonl` as compact JSON lines (`json.dumps(..., separators=(",", ":"))`)
8. Summary file schema:
   - `schema_version`: `"outage-windows-v1"`
   - `raw_incident_count`
   - `unique_incident_ids`
   - `canonical_incident_count`
   - `service_count`
   - `severity_counts` with keys in order: `critical`, `major`, `minor`
   - `total_unplanned_downtime_ms`
   - `total_maintenance_overlap_ms`
   - `total_billable_downtime_ms`
   - `longest_window_ms`
   - `queued_window_count`
   - `planned_excluded_count`
   - `queue_signature_checksum` (sha256 of queue signatures joined with `|`, queue order)
9. Preserve `/app/workflow/.compile_outages.original` unchanged.
10. Output directory contract is strict: write exactly the three files listed above (no extras).
11. The repaired pipeline must not read/import verifier artifacts under `/tests` (for example fixtures or test helper modules).

Do not hardcode outputs. Compute everything from `/app/data/outages.json` and `/app/data/maintenance_windows.json`.
