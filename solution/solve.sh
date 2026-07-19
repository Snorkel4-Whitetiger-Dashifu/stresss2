#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Inspect before changing anything (read-only) ---
# Read the deployment state the runbook requires.
cat /app/docs/deployment_runbook.md || true

# Read the output contract: schemas, key sets, identifier payloads, checksum encodings.
python3 -c "import json;print(json.dumps(json.load(open('/app/docs/routing_contract.json')),indent=2))"

# Locate the governing CAB entries. The log is long and mostly routine, so index the
# ticketed decisions first, then read the ones that govern each stage.
grep -n "CAB-" /app/incident/rollout_review_log.md | head -60 || true
python3 -c "import json;print(json.dumps(json.load(open('/app/docs/routing_contract.json'))['governing_entry_index'],indent=2))"

# Confirm which entries are superseded rather than governing.
grep -n "Superseded\|Revised" /app/incident/rollout_review_log.md | head -20 || true

# Inspect the current host state and the broken compiler before touching either.
ls -la /usr/local/bin/compile-outages /var/lock /app/output 2>&1 || true
getent passwd svc-outage || echo "svc-outage not provisioned"
ls -la /etc/cron.d/ 2>&1 || true
sed -n '1,60p' /app/workflow/compile_outages.py || true

# Read the operational inputs the compile reconciles.
ls -la /app/data || true
python3 -c "import json;d=json.load(open('/app/data/outages.json'));print(len(d),'incident rows')"

# --- Restore the deployment state defined in /app/docs/deployment_runbook.md ---

# Dedicated service account with no interactive shell.
if ! getent passwd svc-outage >/dev/null; then
  useradd --system --shell /usr/sbin/nologin svc-outage
fi

# Operator wrapper: executable, targets the live compiler, honors the lock.
cat > /usr/local/bin/compile-outages <<'EOF'
#!/bin/sh
LOCK=/var/lock/outage-compile.lock
if [ -e "$LOCK" ]; then
  echo "outage compile blocked by existing lock: $LOCK" >&2
  exit 75
fi
exec python3 /app/workflow/compile_outages.py "$@"
EOF
chmod 0755 /usr/local/bin/compile-outages

# Clear the stale lock left by the crashed rollout.
rm -f /var/lock/outage-compile.lock

# Reinstate the schedule.
printf '*/5 * * * * svc-outage /usr/local/bin/compile-outages --input /app/data/outages.json --output-dir /app/output\n' \
  > /etc/cron.d/outage-compile
chmod 0644 /etc/cron.d/outage-compile

# Output directory ownership and mode per runbook.
mkdir -p /app/output
chown svc-outage:svc-outage /app/output
chmod 0750 /app/output

# --- Restore the compiler itself and produce the responder outputs ---

cp "${SCRIPT_DIR}/compile_outages_fixed.py" /app/workflow/compile_outages.py
chmod +x /app/workflow/compile_outages.py

/usr/local/bin/compile-outages --input /app/data/outages.json --output-dir /app/output
