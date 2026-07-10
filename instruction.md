Repair `/app/workflow/compile_outages.py`. The current implementation breaks core interval logic used by on-call routing.

Keep the CLI contract:
- `python3 /app/workflow/compile_outages.py --input PATH --output-dir PATH`
- default input is `/app/data/outages.json`
- default output dir is `/app/output`
- maintenance windows are loaded from `/app/data/maintenance_windows.json`

The fixed compiler must write exactly three files under the output dir:
- `downtime_summary.json`
- `service_windows.json`
- `incident_queue.jsonl`

High-level requirements:
- Canonicalize incidents (`strip().lower()` normalization, boolean coercion, dedupe by highest `end_ms`).
- Build per-service merged windows using touch-aware interval merging.
- Subtract same-service maintenance overlap from each merged window to compute billable duration.
- Emit deterministic window metadata (including source IDs and max severity) and deterministic queue rows (IDs/signatures/priorities) with stable sorting.
- Queue inclusion and priority must be derived from billable duration, severity, and incident count.
- Summary must aggregate all derived totals (raw/canonical counts, severity counts, overlap/billable totals, longest window, queue count, checksum).
- JSONL output must be compact and output ordering must be deterministic.
- Preserve `/app/workflow/.compile_outages.original` unchanged.
- Do not write extra files and do not read/import verifier artifacts under `/tests`.

Do not hardcode answers. Compute all outputs from `/app/data/outages.json` and `/app/data/maintenance_windows.json`.
