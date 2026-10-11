# Separate diagnostics, not accepted timing samples

Official node: AMD EPYC 7642, Ubuntu 24.04.4, kernel 6.8.0-134-generic, four CPU affinity, ext4. Frozen Nift snapshot 445f4d3545cf031bcce4bf77a2b4a61ffb3b4c4f. perf 6.8.12 and heaptrack 1.5.0. No core edits or host security/cache-policy changes.

## Metadata syscall evidence

10,000-file cloud walk: 21,373 newfstatat, 1,362 getdents64, 687 openat. Stat and basename filter: 41,373 newfstatat, the same directory/open counts. Read/checksum: 51,373 newfstatat and 10,687 openat. Each trace has only four readlink calls. Traced stat syscall time totals 0.260s; its 84.35% newfstatat share is a fraction of traced syscall time, not of total execution.

The extra 20,000 metadata queries match two per explicit file stat. Frozen Parser::inspect_path performs status and then file_size on regular files. Type-only predicates use that same full inspector. There is a concrete metadata reuse opportunity, with error/race/symlink semantics to preserve. Four readlinks do not establish the Build Systems canonicalization diagnosis in this corpus.

## CPU and allocations

The 99Hz cpu-clock DWARF stat profile has 313 samples, no lost samples. Self samples include expression evaluation, malloc (3.51%), string construction (3.19%) and balanced-expression scanning (1.92%); leading libc addresses remain unsymbolized and are not assigned invented function names. The read profile has approximately 1.4k samples, no losses; AST evaluation, RuntimeValue lifetime/assignment and variable lookup are visible. Full-byte checksum work is an interpreter workload as well as filesystem work. These diagnostic profiles are not official timings or precise causal percentages of the entire performance gap.

Heaptrack stat: 5,578,191 allocation calls; 1,111,623 temporary allocations; peak heap 19.37M as printed. The string-construction group has 936,118 allocations; condition trim_copy alone has a 100,000-call stack. Retain the complete symbolized report and compressed raw trace. This supports investigating prepared expressions, repeated parsing/string copying and runtime-value allocation alongside filesystem metadata queries. Instrumented runtime/RSS include profiler overhead and are not substituted into accepted distributions.

## RSS accounting and post-exec control

The official Python supervisor forks with preexec affinity setup. wait4 ru_maxrss covers the child before exec as well as the runtime, causing a growing inherited memory floor. A cloud /usr/bin/true control recorded 8.395 MiB from the small parent and 72.492 MiB after allocating 64 MiB in the parent. Do not rank runtime memory from equal floored values, or subtract an invented constant. Official raw values and distributions remain unchanged and clearly labelled.

A separate correctness-checked single-request walk probe reads /proc VmHWM after the response and before exit, after exec. It is diagnostic, not a replacement official cohort:

| Files | Nift | Python | Node | Bun | Go |
|---|---:|---:|---:|---:|---:|
| 1,000 | 8.848 | 16.043 | 53.250 | 27.801 | 4.477 |
| 10,000 | 26.184 | 18.953 | 67.543 | 33.090 | 9.262 |
| 100,000 | 193.871 | 45.961 | 128.738 | 79.500 | 64.145 |

Values are MiB, one probe per cell. Exact output hashes match the frozen walk oracle. Materialized path inventories and serialization count toward runtime memory. This does not certify long-running memory safety.

## Repeated requests

Ten stat/1,000 requests in one Nift process: 314.831–353.605 ms and resident snapshots 8.383–8.832 MiB. No progressive latency increase appears in this limited probe. Small RSS growth does appear; do not infer a leak or transplant Concurrency registry conclusions. Full five-runtime observations are retained separately.

## Rejected local attempts

Inline serialization inside a read loop executed a callee three times. repro/inline-loop.f versus bound-loop.f reduces this without filesystem work; the measured cloud binary confirms three versus one calls after the campaign. Accepted adapters bind the result once. The initial supplement used a symlink root, which Go WalkDir does not traverse; exact-output certification rejected it. Resolving the common root before passing it to every adapter fixed parity. Neither attempt contributes accepted measurements.

## Collection recovery

Local disk capacity filled during the second evidence copy. The complete cloud archive and extracted files remained intact. Only campaign-generated local fixture/destination trees were removed; generator and all canonical manifests are retained. The partial supplement copy was recopied, then both independent output and distribution/reset auditors passed all 15,016 observations. This did not change or rerun cloud measurements.
