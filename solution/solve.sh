#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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
