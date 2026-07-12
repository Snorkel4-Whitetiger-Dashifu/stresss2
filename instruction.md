Reconcile on-call routing state after a failed pager-policy rollout. The operational command `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH` is producing unsafe responder queues; restore its output while keeping that interface and the defaults `/app/data/outages.json` and `/app/output`. This is an SRE incident-response administration task, not application feature development.

Reconcile incidents with the maintenance, response-policy, routing-exception, handoff, blackout, and degradation records under `/app/data`. The restored compiler must canonicalize incident state, build unplanned service windows, apply those routing domains in operational order, and deterministically calculate inclusion thresholds, priorities, signatures, and checksums. It must remain idempotent and work with alternate incident inputs.

Produce exactly `downtime_summary.json`, `service_windows.json`, and compact `incident_queue.jsonl`. `/app/docs/routing_contract.json` is the normative runbook for source paths, normalization, interval semantics, policy resolution, formulas, schemas, identifier payloads, and ordering; match it exactly.

Preserve `/app/workflow/.compile_outages.original` unchanged and do not read or import anything from `/tests`.
