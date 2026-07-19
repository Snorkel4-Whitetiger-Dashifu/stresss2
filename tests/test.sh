#!/usr/bin/env bash
set -uo pipefail

mkdir -p /logs/verifier

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    echo 0 > /logs/verifier/reward.txt
    exit 0
fi

TEST_DIR="${TEST_DIR:-/tests}"
TEST_PATTERN="${TEST_PATTERN:-test_*.py}"

python3 -m pytest -o cache_dir=/tmp/pytest_cache \
  --ctrf /logs/verifier/ctrf.json \
  -o python_files="${TEST_PATTERN}" \
  "${TEST_DIR}" -rA
RC=$?

if [ "$RC" -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
else
    echo 0 > /logs/verifier/reward.txt
fi
