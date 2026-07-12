#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp "${SCRIPT_DIR}/compile_outages_fixed.py" /app/workflow/compile_outages.py
chmod +x /app/workflow/compile_outages.py

python3 /app/workflow/compile_outages.py --input /app/data/outages.json --output-dir /app/output
