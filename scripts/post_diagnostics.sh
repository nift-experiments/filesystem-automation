#!/usr/bin/env bash
# Run only after BOTH official cohorts have completed; never blend profiles into timings.
set -euo pipefail
cd /opt/filesystem/suite
test -f work/official/complete.json
test -f work/filter-suite/work/official/complete.json
mkdir -p work/diagnostics
# An Ubuntu perf wrapper may require a different installed kernel-tool path.
if [ ! -s work/diagnostics/stat-perf-self.txt ]; then
 for candidate in /usr/lib/linux-tools/*/perf /usr/lib/linux-tools-*/perf; do
  if [ -x "$candidate" ]; then
   printf '%s\n' "$candidate" > work/diagnostics/perf-tool-path.txt
   "$candidate" --version > work/diagnostics/perf-version.txt
   if "$candidate" record -e cpu-clock -F 99 -g --call-graph dwarf -o work/diagnostics/stat-recovered.perf.data -- work/nift-source/nift adapters/nift.f < work/diagnostics/stat.request > work/diagnostics/stat-recovered-perf.stdout 2> work/diagnostics/stat-recovered-perf.stderr; then
    "$candidate" report --stdio --no-children --percent-limit 0.5 -i work/diagnostics/stat-recovered.perf.data > work/diagnostics/stat-perf-self.txt
   fi
   break
  fi
 done
fi
if [ ! -f work/reuse/observations.json ]; then
 python3 scripts/reuse_probe.py > work/diagnostics/reuse.log 2>&1
fi
root="$PWD/work/fixtures/10000"
printf 'read|%s|%s|10000|0\n' "$root" "$PWD/work/diagnostic-dest" > work/diagnostics/read.request
strace -f -c -o work/diagnostics/read.strace work/nift-source/nift adapters/nift.f < work/diagnostics/read.request > work/diagnostics/read.stdout 2> work/diagnostics/read.stderr
perfbin="$(command -v perf || true)"
if [ -f work/diagnostics/perf-tool-path.txt ]; then perfbin="$(cat work/diagnostics/perf-tool-path.txt)"; fi
if [ -n "$perfbin" ] && "$perfbin" record -e cpu-clock -F 99 -g --call-graph dwarf -o work/diagnostics/read.perf.data -- work/nift-source/nift adapters/nift.f < work/diagnostics/read.request > work/diagnostics/read-perf.stdout 2> work/diagnostics/read-perf.stderr; then
 "$perfbin" report --stdio --no-children --percent-limit 0.5 -i work/diagnostics/read.perf.data > work/diagnostics/read-perf-self.txt
fi
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends heaptrack > work/diagnostics/heaptrack-install.log 2>&1
heaptrack --version > work/diagnostics/heaptrack-version.txt 2>&1
heaptrack -o work/diagnostics/stat.heaptrack work/nift-source/nift adapters/nift.f < work/diagnostics/stat.request > work/diagnostics/stat-heaptrack.stdout 2> work/diagnostics/stat-heaptrack.stderr
shopt -s nullglob
traces=(work/diagnostics/stat.heaptrack*.gz work/diagnostics/stat.heaptrack*.zst)
test ${#traces[@]} -eq 1
heaptrack_print -f "${traces[0]}" > work/diagnostics/stat-heaptrack.txt 2> work/diagnostics/stat-heaptrack-print.stderr
printf 'POST-CAMPAIGN ALLOCATION DIAGNOSTIC COMPLETE\n'
