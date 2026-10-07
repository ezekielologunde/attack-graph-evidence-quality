#!/usr/bin/env bash
# Read-only checks. No package installation, job submission or environment dump.
set -u
date -u
for command in qlimits quota qstat; do
  if command -v "$command" >/dev/null 2>&1; then
    printf '\n%s\n' "$command"
    timeout 20 "$command" 2>&1 || true
  fi
done
command -v python3 || true
python3 --version 2>&1 || true
command -v git || true
git --version 2>&1 || true
command -v qsub || true
printf '\nPBS resource information\n'
timeout 20 qstat -Qf express 2>&1 || true
