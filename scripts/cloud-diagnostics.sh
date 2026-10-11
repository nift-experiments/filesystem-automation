#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p work/diagnostics
root="$PWD/work/fixtures/10000"
for kind in walk stat filter; do
 printf '%s|%s|%s|10000|10\n' "$kind" "$root" "$PWD/work/diagnostic-dest" > "work/diagnostics/$kind.request"
 strace -f -c -o "work/diagnostics/$kind.strace" work/nift-source/nift adapters/nift.f < "work/diagnostics/$kind.request" > "work/diagnostics/$kind.stdout" 2> "work/diagnostics/$kind.stderr"
done
if command -v perf >/dev/null; then
 perf record -e cpu-clock -F 99 -g --call-graph dwarf -o work/diagnostics/stat.perf.data -- work/nift-source/nift adapters/nift.f < work/diagnostics/stat.request > work/diagnostics/stat-perf.stdout 2> work/diagnostics/stat-perf.stderr
 perf report --stdio --no-children --percent-limit 0.5 -i work/diagnostics/stat.perf.data > work/diagnostics/stat-perf-self.txt
fi
python3 scripts/reuse_probe.py > work/diagnostics/reuse.log 2>&1
