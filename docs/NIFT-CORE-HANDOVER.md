# Nift filesystem investigation handover (local stage)

Core snapshot: 445f4d3545cf031bcce4bf77a2b4a61ffb3b4c4f. No core changes in this workspace.

## Side-effecting chained call can repeat execution

Retained semantic harness: scripts/semantics.py. A small three-file fixture includes an empty file, spaces and Unicode. Diagnostic source uses the campaign adapter with print("EXECUTE") at execute entry and the inline print(execute(...).stringify()) protocol expression. This produced three EXECUTE entries for one request. The explicit result binding produced one. Initial rename work completed its first traversal, then attempted the first rename again and failed with ENOENT. Retain the rejected full adapter, stdout/stderr and paired explicit-binding control under work/semantics. Short constant-return call probes do not reproduce, so do not assert a general rule that every chained call is repeated. Reduce the dynamic/complex-function case further in the core workspace.

Expected benefit: ensure effectful callable expressions are evaluated exactly once before member access/serialization; protect destructive automation and prevent duplicated reads/copies. Preserve ordinary evaluation/error/lifetime semantics. The campaign works around this only with a normal explicit result binding, certified once and final-state oracle checked.

## API gaps

stat returns exists/type/size, not modification time. No located public native SHA-256. remove rejects directories. This constrains timestamp scans, cryptographic manifests and complete recursive cleanup. Do not use FFI or external helpers to disguise these gaps. Consider explicit stat timestamp fields, native byte/file hashing and carefully scoped recursive-removal contracts with clear symlink/root/error semantics.

## Performance investigation pending cloud

Local 100k corpus: Nift traversal ~12s, stat ~28s, full-byte portable checksum ~119s, copy ~45s. These are local feasibility observations, not accepted cloud results. Use cloud strace/perf results to separate API path/stat overhead from interpreter checksum work; do not assume the previous build-system diagnosis applies. Ordinary API traversal requires separate is_dir checks and per-directory sorted ls. Investigate metadata reuse and repeated path resolution only with direct evidence.
