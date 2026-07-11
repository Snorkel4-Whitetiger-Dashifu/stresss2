You are the on-call SRE fixing a broken outage rollup job used by pager routing. Repair `/app/workflow/compile_outages.py` so outputs are deterministic and satisfy strict routing math.

Keep the CLI contract exactly as-is:
- `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default input: `/app/data/outages.json`
- default output dir: `/app/output`
- maintenance windows are always loaded from `/app/data/maintenance_windows.json`
- routing policies are always loaded from `/app/data/response_policies.json`

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
   - canonicalize maintenance windows before overlap math:
     - normalize `service` with the same alias mapping as incidents
     - normalize `start_ms` / `end_ms` with the same int-coercion rule; ignore rows where `end_ms <= start_ms`
     - merge per service when windows overlap or touch (`next.start_ms <= current.end_ms`)
   - same-service windows only
   - overlap formula per segment: `max(0, min(end_a, end_b) - max(start_a, start_b))`
   - `maintenance_overlap_ms`: summed overlap against canonical merged maintenance windows (no double-counting)
   - `maintenance_span_count`: number of distinct overlap spans contributing to `maintenance_overlap_ms`
   - `billable_duration_ms = max(duration_ms - maintenance_overlap_ms, 0)`

Queue behavior:
- resolve policy per normalized service from `/app/data/response_policies.json`:
  - use `default` profile, then apply `service_overrides[service]` when present
  - numeric policy fields are int-coerced; missing override fields inherit from default
  - the `default` profile is authoritative and must include:
    `queue_min_effective_ms`, `critical_p1_min_ms`, `critical_threshold_ms`, `high_threshold_ms`, `no_overlap_high_duration_ms`, `critical_count_for_critical`, `no_overlap_bonus`, `segment_bonus`, `score_threshold_critical`, `score_threshold_high`, and `severity_weight`
  - if `critical_p1_min_ms` is absent in a malformed policy file, treat it as `280` for robustness
  - severity weights are merged key-wise (`critical`, `major`, `minor`)
- include windows when `billable_duration_ms >= policy.queue_min_effective_ms`
- `window_id`: `"{service}:{start_ms}-{end_ms}"`
- `escalation_score`:
  - `(billable_duration_ms // 60)`
  - `+ incident_count * 2`
  - `+ critical_incident_count * 3`
  - `+ policy.no_overlap_bonus` if `maintenance_overlap_ms == 0`
  - `+ maintenance_span_count * policy.segment_bonus`
  - `+ policy.severity_weight[max_severity]`
- `outage_signature`: first 12 lowercase hex chars of SHA1 over `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}|{window_signature}|{max_severity}|{maintenance_span_count}|{policy_profile}"`
- priority:
  - `critical` if (`max_severity == "critical"` and `billable_duration_ms >= policy.critical_p1_min_ms`) OR `billable_duration_ms >= policy.critical_threshold_ms` OR `critical_incident_count >= policy.critical_count_for_critical` OR `escalation_score >= policy.score_threshold_critical`
  - `high` if `billable_duration_ms >= policy.high_threshold_ms` OR (`incident_count >= 3` and `max_severity` in `{"major", "critical"}`) OR (`maintenance_overlap_ms == 0` and `duration_ms >= policy.no_overlap_high_duration_ms`) OR `escalation_score >= policy.score_threshold_high`
  - else `medium`
- sort order: priority rank (`critical > high > medium`), `escalation_score` desc, `billable_duration_ms` desc, `critical_incident_count` desc, `maintenance_span_count` desc, `incident_count` desc, `service` asc, `start_ms` asc
- JSONL must be compact (`json.dumps(row, separators=(",", ":"))`)

Output contracts (exact keys):
- `service_windows.json`: flat `{service: [window, ...]}`; service keys asc, window list sorted by `start_ms` asc.
- each window must contain exactly:
  - `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `maintenance_span_count`, `billable_duration_ms`, `incident_count`, `critical_incident_count`, `source_incident_ids`, `max_severity`, `window_signature`
- `incident_queue.jsonl` rows must contain exactly:
  - `window_id`, `service`, `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `maintenance_span_count`, `billable_duration_ms`, `incident_count`, `critical_incident_count`, `source_incident_ids`, `max_severity`, `window_signature`, `policy_profile`, `policy_queue_min_ms`, `escalation_score`, `priority`, `outage_signature`
- `downtime_summary.json` must contain exactly:
  - `schema_version`, `raw_incident_count`, `unique_incident_ids`, `canonical_incident_count`, `service_count`, `severity_counts`, `total_unplanned_downtime_ms`, `total_maintenance_overlap_ms`, `total_maintenance_span_count`, `total_billable_downtime_ms`, `longest_window_ms`, `queued_window_count`, `priority_counts`, `max_escalation_score`, `planned_excluded_count`, `critical_window_count`, `canonical_input_checksum`, `queue_signature_checksum`, `maintenance_compaction_checksum`, `policy_checksum`

Summary specifics:
- `schema_version` is `"outage-windows-v1"`
- `severity_counts` key order: `critical`, `major`, `minor`
- `critical_window_count`: number of merged windows where `max_severity == "critical"`
- `canonical_input_checksum`: SHA256 over canonical rows in canonical order (`service`, `start_ms`, `incident_id`) using line format `incident_id|service|start_ms|end_ms|severity|planned_int`, `planned_int` in `{0,1}`
- `queue_signature_checksum`: lowercase SHA256 of `"|".join(outage_signature values in final queue order)`
- `maintenance_compaction_checksum`: lowercase SHA256 over canonical merged maintenance windows in canonical order (`service`, `start_ms`, `end_ms`) using newline-joined line format `service|start_ms|end_ms`
- `priority_counts` key order: `critical`, `high`, `medium`
- `max_escalation_score`: max queue-row `escalation_score` (0 if queue empty)
- `policy_checksum`: lowercase SHA256 over canonical policy lines in this order:
  - default line first, then one line per overridden service sorted by service name
  - each line format:
    `profile|queue_min_effective_ms|critical_p1_min_ms|critical_threshold_ms|high_threshold_ms|no_overlap_high_duration_ms|critical_count_for_critical|no_overlap_bonus|segment_bonus|score_threshold_critical|score_threshold_high|weight_critical|weight_major|weight_minor`

Keep `/app/workflow/.compile_outages.original` unchanged and do not read/import verifier artifacts from `/tests`.
