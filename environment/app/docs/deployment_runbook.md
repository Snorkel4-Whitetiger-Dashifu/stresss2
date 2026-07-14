# Outage Compile — Deployment Runbook

Operational deployment contract for the outage routing compile on responder hosts. This document defines the required deployment state; the compile's output contract lives in `routing_contract.json` and its behavioral record in the rollout review log.

## Service account

The compile runs as the dedicated system account `svc-outage`. The account has no interactive login shell (`/usr/sbin/nologin`).

## Wrapper

Operations invokes the compiler only through `/usr/local/bin/compile-outages`:

- mode `0755`, owned by root
- forwards all arguments to `python3 /app/workflow/compile_outages.py`
- concurrency guard: when the lock file `/var/lock/outage-compile.lock` exists, the wrapper must exit with status `75` (EX_TEMPFAIL) without invoking the compiler or writing any output

Stale locks left behind by crashed runs are removed during recovery, not worked around.

## Schedule

The compile is scheduled through a cron drop-in at `/etc/cron.d/outage-compile`, mode `0644`, containing exactly this job line:

```
*/5 * * * * svc-outage /usr/local/bin/compile-outages --input /app/data/outages.json --output-dir /app/output
```

## Output directory

`/app/output` is owned `svc-outage:svc-outage` with mode `0750`. World-writable output directories are a rollout defect and must not survive recovery.
