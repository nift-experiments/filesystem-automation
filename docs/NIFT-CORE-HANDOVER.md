# Nift filesystem investigation handover (local stage)

Core snapshot: 445f4d3545cf031bcce4bf77a2b4a61ffb3b4c4f. No core changes in this workspace.

## Side-effecting chained call inside a read loop can repeat execution

Retained semantic harness: scripts/semantics.py. A small three-file fixture includes an empty file, spaces and Unicode. Diagnostic source uses the campaign adapter with print("EXECUTE") at execute entry and the inline print(execute(...).stringify()) protocol expression. This produced three EXECUTE entries for one request. The explicit result binding produced one. Initial rename work completed its first traversal, then attempted the first rename again and failed with ENOENT. Retain the rejected full adapter, stdout/stderr and paired explicit-binding control under work/semantics. Short constant-return call probes do not reproduce, so do not assert a general rule that every chained call is repeated. Reduce the dynamic/complex-function case further in the core workspace.

Further reduction: `repro/inline-loop.f` needs no filesystem fixture. One `walk|3` input produces three CALLED lines and one result; `repro/bound-loop.f` produces one CALLED line and the identical result. Similar calls outside the read loop execute once. This isolates a loop-context/expression interaction, not a proven parser or evaluator root cause. Retain both controls and the broader rejected adapter.

Expected benefit: ensure effectful callable expressions are evaluated exactly once before member access/serialization; protect destructive automation and prevent duplicated reads/copies. Preserve ordinary evaluation/error/lifetime semantics. The campaign works around this only with a normal explicit result binding, certified once and final-state oracle checked.

## API gaps

stat returns exists/type/size, not modification time. No located public native SHA-256. remove rejects directories. This constrains timestamp scans, cryptographic manifests and complete recursive cleanup. Do not use FFI or external helpers to disguise these gaps. Consider explicit stat timestamp fields, native byte/file hashing and carefully scoped recursive-removal contracts with clear symlink/root/error semantics.

## Performance investigation pending cloud

Local 100k corpus: Nift traversal ~12s, stat ~28s, full-byte portable checksum ~119s, copy ~45s. These are local feasibility observations, not accepted cloud results. Use cloud strace/perf results to separate API path/stat overhead from interpreter checksum work; do not assume the previous build-system diagnosis applies. Ordinary API traversal requires separate is_dir checks and per-directory sorted ls. Investigate metadata reuse and repeated path resolution only with direct evidence.

## Local syscall evidence (separate from official cloud timings)

The 10k-file local traces show 21,376 `newfstatat` calls for walk and 41,376 for stat; filter has the same 41,376. The additional 20,000 calls match two queries per explicit file stat. In the frozen `src/ParserExpression.cpp:4567`, `inspect_path` calls `std::filesystem::status`, then `file_size` for regular files. `is_dir`, `is_file` and `exists` also use this complete inspector, so a type-only regular-file check fetches an unused size. This is a concrete metadata-reuse opportunity. Preserve error/race/symlink semantics when consolidating queries; do not trade correctness for a stale cache.

Only seven `readlink` calls appear in each complete local diagnostic. Do not transplant a claim of repeated filesystem canonicalization from Build Systems. Pure lexical normalization/allocation costs require CPU/allocation evidence. The strace percentages describe time inside traced syscalls, not the total program runtime. These counts are a local diagnostic pending cloud confirmation, not accepted performance rows.
