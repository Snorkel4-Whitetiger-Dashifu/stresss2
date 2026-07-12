Repair `/app/workflow/compile_outages.py` for an on-call incident-routing workflow.

Keep this CLI unchanged:
- `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default input `/app/data/outages.json`
- default output dir `/app/output`

The workflow is operationally scoped (pager-routing), not an analytics batch job. It must be deterministic, idempotent, and produce routing outputs used by human responders.

## Required Inputs (fixed paths)
- `/app/data/maintenance_windows.json`
- `/app/data/response_policies.json`
- `/app/data/routing_exceptions.json`
- `/app/data/handoff_windows.json`
- `/app/data/blackout_windows.json`
- `/app/data/degrade_windows.json`

## Required Outputs (exactly 3 files)
- `downtime_summary.json`
- `service_windows.json`
- `incident_queue.jsonl`

## Outcome Contract
- Canonicalize and dedupe incidents deterministically.
- Build merged outage windows from unplanned incidents.
- Apply overlap/attenuation domains in this order:
  1) maintenance
  2) routing exceptions
  3) handoff
  4) blackout
  5) degrade
- Compute queue inclusion thresholds, pressure scores, signatures, priorities, and final sort order deterministically.
- Use compact JSONL (`json.dumps(..., separators=(",", ":"))`).

## Schema + Formula Source of Truth
All exact field names, default policy values, overlap semantics, score formulas, checksum line formats, and sort tie-breaks are defined in:
- `/app/docs/routing_contract.json`

You must match that contract exactly.

Important clarifications that are also normative in the contract:
- `window_signature` is a 10-character truncated SHA-1 identifier (not a full hash and not a descriptive label).
- `outage_signature` is the first 12 lowercase SHA-1 hex characters; `queue_digest` is the first 10. Their exact payloads and test vectors are in the contract.
- `downtime_summary.json` uses a flat top-level schema; required aggregate/checksum fields are not nested under helper objects.
- `billable_duration_ms` is maintenance-only, while handoff/blackout/degrade attenuation applies sequentially to adjusted/routed/dispatchable billable fields.
- `policy_profile` is serialized as `default` or the canonical service name for overrides (no prefixes).
- Intervals are half-open. Handoff/blackout/degrade segment counts come from the compacted union of matching `all` and maximum-severity overlap spans.
- Normalize `planned` before dedupe and exclusion; nonzero numeric values such as `2` are true.

## Guardrails
- Keep `/app/workflow/.compile_outages.original` unchanged.
- Do not read/import verifier artifacts from `/tests`.
- Support alternate `--input` files and custom `--output-dir`.
