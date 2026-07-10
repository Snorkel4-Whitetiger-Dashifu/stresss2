You are the on-call SRE fixing a broken outage rollup job used by pager routing. Repair `/app/workflow/compile_outages.py` so the generated artifacts are deterministic and operationally correct.

Keep the CLI contract exactly as-is:
- `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default input is `/app/data/outages.json`
- default output dir is `/app/output`
- maintenance windows are always loaded from `/app/data/maintenance_windows.json`

The run must write exactly three files in the chosen output directory (no extras): `downtime_summary.json`, `service_windows.json`, and `incident_queue.jsonl`.

Processing requirements:
1. Canonicalize incidents by normalizing `service` and `severity` with `str(...).strip().lower()`, coercing `planned` as follows, and deduplicating by `incident_id` keeping the row with greatest `end_ms`.
   - if `planned` is a boolean, keep it unchanged
   - if `planned` is a string, only `"true"`, `"1"`, or `"yes"` (case-insensitive) are `True`; all other strings are `False`
   - for non-string, non-boolean values, use Python `bool(value)`
   - examples: `"yes"` -> `True`, `"TRUE"` -> `True`, `"no"` -> `False`, `"0"` -> `False`, `"random"` -> `False`
2. Build merged windows from unplanned incidents only (planned incidents still count in summary severity totals). Merge per normalized service and treat touching intervals as mergeable (`next.start_ms <= current.end_ms`).
3. For each merged window compute `duration_ms`, `incident_count`, sorted `source_incident_ids`, and `max_severity` with rank `critical > major > minor`.
4. Apply maintenance credit only from same-service maintenance windows using overlap `max(0, min(end_a, end_b) - max(start_a, start_b))`; set `maintenance_overlap_ms` to summed overlap and `billable_duration_ms` to `max(duration_ms - maintenance_overlap_ms, 0)`.

Queue behavior:
- Include windows only when `billable_duration_ms >= 250`.
- `window_id` format: `"{service}:{start_ms}-{end_ms}"`.
- `outage_signature`: first 12 lowercase hex chars of SHA1 over `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}"`.
- Priority is `critical` if (`max_severity == "critical"` and `billable_duration_ms >= 300`) or `billable_duration_ms >= 700`; else `high` if `billable_duration_ms >= 350` or (`incident_count >= 3` and `max_severity` is `major` or `critical`); else `medium`.
- Final queue ordering: priority rank (`critical > high > medium`), `billable_duration_ms` desc, `incident_count` desc, `service` asc, `start_ms` asc.
- JSONL rows must be compact (`json.dumps(row, separators=(",", ":"))`).

Output contracts (exact keys):

`service_windows.json` must be a flat map `{service: [window, ...]}` with service keys sorted ascending and windows sorted by `start_ms` ascending.

```json
{
  "auth": [
    {
      "start_ms": 100,
      "end_ms": 500,
      "duration_ms": 400,
      "maintenance_overlap_ms": 50,
      "billable_duration_ms": 350,
      "incident_count": 2,
      "source_incident_ids": ["i1", "i2"],
      "max_severity": "critical"
    }
  ]
}
```

`incident_queue.jsonl` rows must contain exactly:
`window_id`, `service`, `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `billable_duration_ms`, `incident_count`, `source_incident_ids`, `max_severity`, `priority`, `outage_signature`.

`downtime_summary.json` must contain exactly:
`schema_version`, `raw_incident_count`, `unique_incident_ids`, `canonical_incident_count`, `service_count`, `severity_counts`, `total_unplanned_downtime_ms`, `total_maintenance_overlap_ms`, `total_billable_downtime_ms`, `longest_window_ms`, `queued_window_count`, `planned_excluded_count`, `queue_signature_checksum`.

Summary specifics: `schema_version` is `"outage-windows-v1"`, `severity_counts` key order is `critical`, `major`, `minor`, and `queue_signature_checksum` is a 64-char lowercase SHA256 of `"|".join(outage_signature values in final queue order)`.

Keep `/app/workflow/.compile_outages.original` unchanged and do not read/import verifier artifacts from `/tests`.
