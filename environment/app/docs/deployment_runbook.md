# Outage Compile — Deployment Runbook

Operational deployment contract for the outage routing compile on responder hosts. This document defines the required deployment state; the compile's output contract lives in `routing_contract.json` and its behavioral record in the rollout review log.

## Service account

The *scheduled* compile runs under the dedicated system account `svc-outage` — that identity is selected by the cron drop-in below (the user field of the cron line), not by the wrapper. The account has no interactive login shell (`/usr/sbin/nologin`).

## Wrapper

Operations invokes the compiler only through `/usr/local/bin/compile-outages`:

- mode `0755`, owned by root
- forwards all arguments to `python3 /app/workflow/compile_outages.py`
- runs the compiler **as the invoking user**: the wrapper must not switch user, `su`, `sudo`, `setpriv`, `setuid`, or otherwise drop privileges — selecting the `svc-outage` identity is the cron drop-in's job, not the wrapper's. Invoked directly (e.g. by an operator or in a check), the wrapper runs the compiler as whoever ran it.
- concurrency guard: when the lock file `/var/lock/outage-compile.lock` exists, the wrapper must exit with status `75` (EX_TEMPFAIL) without invoking the compiler or writing any output

Stale locks left behind by crashed runs are removed during recovery, not worked around.

## Schedule

The compile is scheduled through a cron drop-in at `/etc/cron.d/outage-compile`, mode `0644`, containing exactly this job line:

```
*/5 * * * * svc-outage /usr/local/bin/compile-outages --input /app/data/outages.json --output-dir /app/output
```

## Output directory

`/app/output` is owned `svc-outage:svc-outage` with mode `0750`. World-writable output directories are a rollout defect and must not survive recovery.
