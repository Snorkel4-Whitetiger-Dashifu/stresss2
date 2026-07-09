The outage compiler in `/app/workflow/compile_outages.py` is wrong and must be repaired.

Keep the CLI interface:
- `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default input is `/app/data/outages.json`
- default output dir is `/app/output`

The repaired compiler must emit exactly three files under the output dir:
- `downtime_summary.json`
- `service_windows.json`
- `incident_queue.jsonl`

Required behavior:
1. Canonicalize records:
   - normalize `service` and `severity` to lowercase
   - dedupe by `incident_id`, keeping the record with the highest `end_ms`
2. Planned incidents (`planned=true`) are excluded from merged windows and queue output, but still counted in `severity_counts`.
3. Merge unplanned intervals per service when intervals overlap or touch (`next.start_ms <= current.end_ms`).
4. For each merged window, compute:
   - `start_ms`, `end_ms`, `duration_ms` (`end_ms - start_ms`)
   - `incident_count`
   - `max_severity` using rank `critical > major > minor`
5. Queue rules:
   - include merged windows with `duration_ms >= 250`
   - assign `priority`:
     - `critical` if `max_severity == "critical"` OR `duration_ms >= 700`
     - `high` if `duration_ms >= 400`
     - otherwise `medium`
   - sort queue by priority (`critical > high > medium`), then `duration_ms` descending, then `service` ascending, then `start_ms` ascending
   - write `incident_queue.jsonl` as compact JSON lines (`json.dumps(..., separators=(",", ":"))`)
6. Summary file schema:
   - `schema_version`: `"outage-windows-v1"`
   - `raw_incident_count`
   - `unique_incident_ids`
   - `canonical_incident_count`
   - `service_count`
   - `severity_counts` with keys in order: `critical`, `major`, `minor`
   - `total_unplanned_downtime_ms`
   - `queued_window_count`
   - `planned_excluded_count`
7. `service_windows.json` must be a flat map: `{service: [window, ...]}` with services sorted alphabetically and windows sorted by `start_ms`.

Do not hardcode outputs. Compute everything from the provided input data.
