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

## Guardrails
- Keep `/app/workflow/.compile_outages.original` unchanged.
- Do not read/import verifier artifacts from `/tests`.
- Support alternate `--input` files and custom `--output-dir`.
