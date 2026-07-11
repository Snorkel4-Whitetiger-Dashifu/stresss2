You are the on-call SRE fixing a broken outage rollup job used by pager routing. Repair `/app/workflow/compile_outages.py` so outputs are deterministic and satisfy strict routing math.

Keep the CLI contract exactly as-is:
- `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default input: `/app/data/outages.json`
- default output dir: `/app/output`
- maintenance windows are always loaded from `/app/data/maintenance_windows.json`
- routing policies are always loaded from `/app/data/response_policies.json`
- routing exceptions are always loaded from `/app/data/routing_exceptions.json`
- handoff windows are always loaded from `/app/data/handoff_windows.json`
- blackout windows are always loaded from `/app/data/blackout_windows.json`
- degrade windows are always loaded from `/app/data/degrade_windows.json`

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
6. Routing exceptions:
   - canonicalize `/app/data/routing_exceptions.json` before overlap math:
     - normalize `service` using the same alias mapping as incidents
     - normalize `start_ms` / `end_ms` with the same int-coercion rule; ignore rows where `end_ms <= start_ms`
     - normalize `action` with `str(action).strip().lower()`; allowed actions are only `suppress` and `boost`; ignore others
     - compact per `(service, action)` by merging overlapping or touching intervals (`next.start_ms <= current.end_ms`)
   - same-service overlap only
   - per window compute:
     - `suppression_overlap_ms`: total overlap against compacted `suppress` intervals, except any intersection with boost intervals is assigned to boost (boost precedence)
     - `boost_overlap_ms`: total overlap against compacted `boost` intervals (includes boost-precedence intersections)
7. Handoff windows:
   - canonicalize `/app/data/handoff_windows.json` before overlap math:
     - normalize `service` using the same alias mapping
     - normalize `severity_scope` with `str(...).strip().lower()`; allowed values only `all`, `major`, `critical`
     - normalize `start_ms` / `end_ms` with the same int-coercion rule; ignore rows where `end_ms <= start_ms`
     - compact per `(service, severity_scope)` by merging overlapping or touching intervals
   - per merged window, collect overlap spans from same-service scopes `{all, max_severity}` and union/compact those spans
   - compute:
     - `handoff_overlap_ms`: total union overlap against handoff spans
     - `handoff_segment_count`: number of compacted handoff spans
     - `adjusted_billable_duration_ms = max(billable_duration_ms - (handoff_overlap_ms // 2), 0)`
   - `window_signature`: first 10 lowercase hex chars of SHA1 over `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}|{max_severity}|{handoff_segment_count}"`
8. Blackout windows:
   - canonicalize `/app/data/blackout_windows.json` before overlap math:
     - normalize `service` using the same alias mapping
     - normalize `severity_scope` with `str(...).strip().lower()`; allowed values only `all`, `major`, `critical`
     - normalize `start_ms` / `end_ms` with the same int-coercion rule; ignore rows where `end_ms <= start_ms`
     - compact per `(service, severity_scope)` by merging overlapping or touching intervals
   - per merged window, collect overlap spans from same-service scopes `{all, max_severity}` and union/compact those spans
   - compute:
     - `blackout_overlap_ms`: total union overlap against blackout spans
     - `blackout_segment_count`: number of compacted blackout spans
     - `routed_billable_duration_ms = max(adjusted_billable_duration_ms - (blackout_overlap_ms // 3), 0)`
   - `window_signature`: first 10 lowercase hex chars of SHA1 over `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}|{max_severity}|{handoff_segment_count}|{blackout_segment_count}"`
9. Degrade windows:
   - canonicalize `/app/data/degrade_windows.json` before overlap math:
     - normalize `service` using the same alias mapping
     - normalize `severity_scope` with `str(...).strip().lower()`; allowed values only `all`, `major`, `critical`
     - normalize `start_ms` / `end_ms` with the same int-coercion rule; ignore rows where `end_ms <= start_ms`
     - compact per `(service, severity_scope)` by merging overlapping or touching intervals
   - per merged window, collect overlap spans from same-service scopes `{all, max_severity}` and union/compact those spans
   - compute:
     - `degrade_overlap_ms`: total union overlap against degrade spans
     - `degrade_segment_count`: number of compacted degrade spans
     - `dispatchable_billable_duration_ms = max(routed_billable_duration_ms - (degrade_overlap_ms // 4), 0)`
   - `window_signature`: first 10 lowercase hex chars of SHA1 over `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}|{max_severity}|{handoff_segment_count}|{blackout_segment_count}|{degrade_segment_count}"`

Queue behavior:
- resolve policy per normalized service from `/app/data/response_policies.json`:
  - use `default` profile, then apply `service_overrides[service]` when present
  - numeric policy fields are int-coerced; missing override fields inherit from default
  - if fields are missing in malformed policy input, apply these defaults before service overrides:
    - `queue_min_effective_ms=220`
    - `critical_p1_min_ms=280`
    - `critical_threshold_ms=650`
    - `high_threshold_ms=320`
    - `no_overlap_high_duration_ms=450`
    - `critical_count_for_critical=2`
    - `no_overlap_bonus=4`
    - `segment_bonus=1`
    - `score_threshold_critical=34`
    - `score_threshold_high=18`
    - `suppress_penalty_ms=40`
    - `boost_credit_ms=30`
    - `suppress_unit_ms=50`
    - `boost_unit_ms=50`
    - `min_queue_floor_ms=120`
    - `boost_force_critical_ms=140`
    - `boost_high_relief_ms=40`
    - `handoff_penalty_ms=35`
    - `handoff_unit_ms=60`
    - `handoff_force_critical_ms=150`
    - `handoff_high_relief_ms=50`
    - `blackout_penalty_ms=45`
    - `blackout_unit_ms=70`
    - `blackout_force_critical_ms=200`
    - `blackout_high_relief_ms=55`
    - `degrade_penalty_ms=30`
    - `degrade_unit_ms=80`
    - `degrade_force_critical_ms=170`
    - `degrade_high_relief_ms=45`
    - `severity_weight={"critical":5,"major":3,"minor":1}`
  - severity weights are merged key-wise (`critical`, `major`, `minor`)
- define:
  - `suppress_units = 0` when `suppression_overlap_ms == 0`, else `ceil(suppression_overlap_ms / max(policy.suppress_unit_ms, 1))`
  - `boost_units = boost_overlap_ms // max(policy.boost_unit_ms, 1)`
  - `effective_queue_min_ms = max(policy.queue_min_effective_ms + suppress_units * policy.suppress_penalty_ms - boost_units * policy.boost_credit_ms, policy.min_queue_floor_ms)`
  - `handoff_units = handoff_overlap_ms // max(policy.handoff_unit_ms, 1)`
  - `adjusted_queue_min_ms = effective_queue_min_ms + handoff_units * policy.handoff_penalty_ms`
  - `blackout_units = blackout_overlap_ms // max(policy.blackout_unit_ms, 1)`
  - `routed_queue_min_ms = adjusted_queue_min_ms + blackout_units * policy.blackout_penalty_ms`
  - `degrade_units = degrade_overlap_ms // max(policy.degrade_unit_ms, 1)`
  - `dispatch_queue_min_ms = routed_queue_min_ms + degrade_units * policy.degrade_penalty_ms`
- include windows when `dispatchable_billable_duration_ms >= dispatch_queue_min_ms`
- `window_id`: `"{service}:{start_ms}-{end_ms}"`
- `exception_balance_score = boost_units - suppress_units`
- `handoff_pressure_score` from probe window `[end_ms-180, end_ms+1)`:
  - `all_probe_ms`: overlap with compacted handoff `(service, all)` intervals
  - `severity_probe_ms`: overlap with compacted handoff `(service, max_severity)` intervals
  - `handoff_pressure_score = (all_probe_ms // 30) + (severity_probe_ms // 20) + handoff_segment_count`
- `blackout_pressure_score` from probe window `[end_ms-240, end_ms+1)`:
  - `all_probe_ms`: overlap with compacted blackout `(service, all)` intervals
  - `severity_probe_ms`: overlap with compacted blackout `(service, max_severity)` intervals
  - `blackout_pressure_score = (all_probe_ms // 36) + (severity_probe_ms // 24) + blackout_segment_count`
- `degrade_pressure_score` from probe window `[end_ms-210, end_ms+1)`:
  - `all_probe_ms`: overlap with compacted degrade `(service, all)` intervals
  - `severity_probe_ms`: overlap with compacted degrade `(service, max_severity)` intervals
  - `degrade_pressure_score = (all_probe_ms // 34) + (severity_probe_ms // 23) + degrade_segment_count`
- `escalation_score`:
  - `(dispatchable_billable_duration_ms // 60)`
  - `+ incident_count * 2`
  - `+ critical_incident_count * 3`
  - `+ policy.no_overlap_bonus` if `maintenance_overlap_ms == 0`
  - `+ maintenance_span_count * policy.segment_bonus`
  - `+ policy.severity_weight[max_severity]`
  - `+ exception_balance_score * 2`
  - `+ handoff_pressure_score * 2`
  - `+ blackout_pressure_score * 2`
- `risk_vector = escalation_score + blackout_pressure_score + (degrade_pressure_score * 2)`
- `outage_signature`: first 12 lowercase hex chars of SHA1 over `"{service}|{start_ms}|{end_ms}|{','.join(source_incident_ids)}|{window_signature}|{max_severity}|{maintenance_span_count}|{policy_profile}|{suppression_overlap_ms}|{boost_overlap_ms}|{effective_queue_min_ms}|{adjusted_queue_min_ms}|{handoff_overlap_ms}|{handoff_pressure_score}|{blackout_overlap_ms}|{blackout_pressure_score}|{routed_queue_min_ms}|{degrade_overlap_ms}|{degrade_pressure_score}|{dispatch_queue_min_ms}|{exception_balance_score}"`
- `queue_digest`: first 10 lowercase hex chars of SHA1 over `"{window_id}|{priority}|{escalation_score}|{handoff_pressure_score}|{blackout_pressure_score}|{degrade_pressure_score}|{risk_vector}"`
- priority:
  - `critical` if (`max_severity == "critical"` and `dispatchable_billable_duration_ms >= policy.critical_p1_min_ms`) OR `dispatchable_billable_duration_ms >= policy.critical_threshold_ms` OR `critical_incident_count >= policy.critical_count_for_critical` OR `escalation_score >= policy.score_threshold_critical` OR `boost_overlap_ms >= policy.boost_force_critical_ms` OR `handoff_overlap_ms >= policy.handoff_force_critical_ms` OR `blackout_overlap_ms >= policy.blackout_force_critical_ms` OR `degrade_overlap_ms >= policy.degrade_force_critical_ms` OR `risk_vector >= policy.score_threshold_critical + 4`
  - `high` if `dispatchable_billable_duration_ms >= policy.high_threshold_ms` OR (`incident_count >= 3` and `max_severity` in `{"major", "critical"}`) OR (`maintenance_overlap_ms == 0` and `duration_ms >= policy.no_overlap_high_duration_ms`) OR `escalation_score >= policy.score_threshold_high` OR (`exception_balance_score > 0` and `dispatchable_billable_duration_ms >= max(policy.high_threshold_ms - policy.boost_high_relief_ms, 0))` OR (`handoff_pressure_score > 0` and `dispatchable_billable_duration_ms >= max(policy.high_threshold_ms - policy.handoff_high_relief_ms, 0))` OR (`blackout_pressure_score > 0` and `dispatchable_billable_duration_ms >= max(policy.high_threshold_ms - policy.blackout_high_relief_ms, 0))` OR (`degrade_pressure_score > 0` and `dispatchable_billable_duration_ms >= max(policy.high_threshold_ms - policy.degrade_high_relief_ms, 0))` OR `risk_vector >= policy.score_threshold_high + 2`
  - else `medium`
- sort order: priority rank (`critical > high > medium`), `escalation_score` desc, `handoff_pressure_score` desc, `blackout_pressure_score` desc, `degrade_pressure_score` desc, `risk_vector` desc, `exception_balance_score` desc, `dispatchable_billable_duration_ms` desc, `routed_billable_duration_ms` desc, `adjusted_billable_duration_ms` desc, `critical_incident_count` desc, `maintenance_span_count` desc, `incident_count` desc, `service` asc, `start_ms` asc
- JSONL must be compact (`json.dumps(row, separators=(",", ":"))`)

Output contracts (exact keys):
- `service_windows.json`: flat `{service: [window, ...]}`; service keys asc, window list sorted by `start_ms` asc.
- each window must contain exactly:
  - `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `maintenance_span_count`, `suppression_overlap_ms`, `boost_overlap_ms`, `billable_duration_ms`, `handoff_overlap_ms`, `handoff_segment_count`, `adjusted_billable_duration_ms`, `blackout_overlap_ms`, `blackout_segment_count`, `routed_billable_duration_ms`, `degrade_overlap_ms`, `degrade_segment_count`, `dispatchable_billable_duration_ms`, `incident_count`, `critical_incident_count`, `source_incident_ids`, `max_severity`, `window_signature`
- `incident_queue.jsonl` rows must contain exactly:
  - `window_id`, `service`, `start_ms`, `end_ms`, `duration_ms`, `maintenance_overlap_ms`, `maintenance_span_count`, `suppression_overlap_ms`, `boost_overlap_ms`, `billable_duration_ms`, `handoff_overlap_ms`, `handoff_segment_count`, `adjusted_billable_duration_ms`, `blackout_overlap_ms`, `blackout_segment_count`, `routed_billable_duration_ms`, `degrade_overlap_ms`, `degrade_segment_count`, `dispatchable_billable_duration_ms`, `incident_count`, `critical_incident_count`, `source_incident_ids`, `max_severity`, `window_signature`, `policy_profile`, `policy_queue_min_ms`, `effective_queue_min_ms`, `adjusted_queue_min_ms`, `routed_queue_min_ms`, `dispatch_queue_min_ms`, `exception_balance_score`, `handoff_pressure_score`, `blackout_pressure_score`, `degrade_pressure_score`, `escalation_score`, `risk_vector`, `priority`, `outage_signature`, `queue_digest`
- `downtime_summary.json` must contain exactly:
  - `schema_version`, `raw_incident_count`, `unique_incident_ids`, `canonical_incident_count`, `service_count`, `severity_counts`, `total_unplanned_downtime_ms`, `total_maintenance_overlap_ms`, `total_maintenance_span_count`, `total_suppression_overlap_ms`, `total_boost_overlap_ms`, `total_handoff_overlap_ms`, `total_handoff_segment_count`, `total_blackout_overlap_ms`, `total_blackout_segment_count`, `total_degrade_overlap_ms`, `total_degrade_segment_count`, `total_billable_downtime_ms`, `total_adjusted_billable_downtime_ms`, `total_routed_billable_downtime_ms`, `total_dispatchable_billable_downtime_ms`, `longest_window_ms`, `queued_window_count`, `priority_counts`, `max_escalation_score`, `max_exception_balance_score`, `max_handoff_pressure_score`, `max_blackout_pressure_score`, `max_degrade_pressure_score`, `max_risk_vector`, `planned_excluded_count`, `critical_window_count`, `canonical_input_checksum`, `queue_signature_checksum`, `maintenance_compaction_checksum`, `exception_compaction_checksum`, `handoff_compaction_checksum`, `blackout_compaction_checksum`, `degrade_compaction_checksum`, `queue_digest_checksum`, `policy_checksum`

Summary specifics:
- `schema_version` is `"outage-windows-v1"`
- `severity_counts` key order: `critical`, `major`, `minor`
- `priority_counts` key order: `critical`, `high`, `medium`
- `critical_window_count`: number of merged windows where `max_severity == "critical"`
- `max_escalation_score`: max queue-row `escalation_score` (0 if queue empty)
- `max_exception_balance_score`: max queue-row `exception_balance_score` (0 if queue empty)
- `max_handoff_pressure_score`: max queue-row `handoff_pressure_score` (0 if queue empty)
- `max_blackout_pressure_score`: max queue-row `blackout_pressure_score` (0 if queue empty)
- `max_degrade_pressure_score`: max queue-row `degrade_pressure_score` (0 if queue empty)
- `max_risk_vector`: max queue-row `risk_vector` (0 if queue empty)
- `canonical_input_checksum`: SHA256 over canonical rows in canonical order (`service`, `start_ms`, `incident_id`) using line format `incident_id|service|start_ms|end_ms|severity|planned_int`, `planned_int` in `{0,1}`
- `queue_signature_checksum`: lowercase SHA256 of `"|".join(outage_signature values in final queue order)`
- `maintenance_compaction_checksum`: lowercase SHA256 over canonical merged maintenance windows in canonical order (`service`, `start_ms`, `end_ms`) using newline-joined line format `service|start_ms|end_ms`
- `exception_compaction_checksum`: lowercase SHA256 over canonical compacted routing exceptions using order (`service`, then `action` in `boost`, `suppress`, then `start_ms`, `end_ms`) and line format `service|action|start_ms|end_ms`
- `handoff_compaction_checksum`: lowercase SHA256 over canonical compacted handoff windows using order (`service`, `severity_scope`, `start_ms`, `end_ms`) and line format `service|severity_scope|start_ms|end_ms`
- `blackout_compaction_checksum`: lowercase SHA256 over canonical compacted blackout windows using order (`service`, `severity_scope`, `start_ms`, `end_ms`) and line format `service|severity_scope|start_ms|end_ms`
- `degrade_compaction_checksum`: lowercase SHA256 over canonical compacted degrade windows using order (`service`, `severity_scope`, `start_ms`, `end_ms`) and line format `service|severity_scope|start_ms|end_ms`
- `queue_digest_checksum`: lowercase SHA256 of `"|".join(queue_digest values in final queue order)`
- `policy_checksum`: lowercase SHA256 over canonical policy lines in this order:
  - default line first, then one line per overridden service sorted by service name
  - each line format:
    `profile|queue_min_effective_ms|critical_p1_min_ms|critical_threshold_ms|high_threshold_ms|no_overlap_high_duration_ms|critical_count_for_critical|no_overlap_bonus|segment_bonus|score_threshold_critical|score_threshold_high|suppress_penalty_ms|boost_credit_ms|suppress_unit_ms|boost_unit_ms|min_queue_floor_ms|boost_force_critical_ms|boost_high_relief_ms|handoff_penalty_ms|handoff_unit_ms|handoff_force_critical_ms|handoff_high_relief_ms|blackout_penalty_ms|blackout_unit_ms|blackout_force_critical_ms|blackout_high_relief_ms|degrade_penalty_ms|degrade_unit_ms|degrade_force_critical_ms|degrade_high_relief_ms|weight_critical|weight_major|weight_minor`

Keep `/app/workflow/.compile_outages.original` unchanged and do not read/import verifier artifacts from `/tests`.
