#!/usr/bin/env bash
# Run only after BOTH official cohorts have completed; never blend profiles into timings.
set -euo pipefail
cd /opt/filesystem/suite
test -f work/official/complete.json
test -f work/filter-suite/work/official/complete.json
mkdir -p work/diagnostics
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends heaptrack > work/diagnostics/heaptrack-install.log 2>&1
heaptrack --version > work/diagnostics/heaptrack-version.txt 2>&1
heaptrack -o work/diagnostics/stat.heaptrack work/nift-source/nift adapters/nift.f < work/diagnostics/stat.request > work/diagnostics/stat-heaptrack.stdout 2> work/diagnostics/stat-heaptrack.stderr
shopt -s nullglob
traces=(work/diagnostics/stat.heaptrack*.gz work/diagnostics/stat.heaptrack*.zst)
test ${#traces[@]} -eq 1
heaptrack_print -f "${traces[0]}" > work/diagnostics/stat-heaptrack.txt 2> work/diagnostics/stat-heaptrack-print.stderr
printf 'POST-CAMPAIGN ALLOCATION DIAGNOSTIC COMPLETE\n'
