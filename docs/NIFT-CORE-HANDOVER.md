# Nift filesystem investigation handover (accepted campaign and separate diagnostics)

Core snapshot: 445f4d3545cf031bcce4bf77a2b4a61ffb3b4c4f. No core changes in this workspace.

## Side-effecting chained call inside a read loop can repeat execution

Retained semantic harness: scripts/semantics.py. A small three-file fixture includes an empty file, spaces and Unicode. Diagnostic source uses the campaign adapter with print("EXECUTE") at execute entry and the inline print(execute(...).stringify()) protocol expression. This produced three EXECUTE entries for one request. The explicit result binding produced one. Initial rename work completed its first traversal, then attempted the first rename again and failed with ENOENT. Retain the rejected full adapter, stdout/stderr and paired explicit-binding control under work/semantics. Comparable calls outside the read loop execute once; do not assert that every chained call repeats. The no-filesystem reduction below is sufficient to start a focused core investigation.

Further reduction: `repro/inline-loop.f` needs no filesystem fixture. One `walk|3` input produces three CALLED lines and one result; `repro/bound-loop.f` produces one CALLED line and the identical result. Similar calls outside the read loop execute once. This isolates a loop-context/expression interaction, not a proven parser or evaluator root cause. The measured cloud binary confirms the same three-versus-one control after the campaign. Retain both controls and the broader rejected adapter.

Expected benefit: ensure effectful callable expressions are evaluated exactly once before member access/serialization; protect destructive automation and prevent duplicated reads/copies. Preserve ordinary evaluation/error/lifetime semantics. The campaign works around this only with a normal explicit result binding, certified once and final-state oracle checked.

## API gaps

stat returns exists/type/size, not modification time. No located public native SHA-256. remove rejects directories. This constrains timestamp scans, cryptographic manifests and complete recursive cleanup. Do not use FFI or external helpers to disguise these gaps. Consider explicit stat timestamp fields, native byte/file hashing and carefully scoped recursive-removal contracts with clear symlink/root/error semantics.

## Accepted performance and cloud diagnostics

RESULTS.md contains all 752 distributions. Booted Nift 100k walk 14.269s, stat 33.130s, read/full-byte checksum 148.707s, copy 59.349s. At 10k, generated pipeline is 17.730s and mixed workflow 8.553s. Supported outputs/reset states pass every independent audit. Capability and timing boundaries are explicit.

Cloud walk/stat/filter newfstatat counts are 21,373/41,373/41,373; read has 51,373. Only four readlinks occur per trace. CPU profiles show expression evaluation, runtime-value lifetime, variable lookup, allocation and string/condition scanning. Heaptrack stat records 5,578,191 allocation calls, 1,111,623 temporary allocations and a 100,000-call trim_copy condition stack. Full captures and reports remain in canonical evidence; DIAGNOSTICS.md separates them from accepted timings. Do not assign names to unsymbolized libc addresses or equate syscall-only percentages with total wall time.

Investigate in this order: exactly-once expression semantics; selective metadata inspection/entry reuse preserving races/errors/symlinks; prepared-expression and string/runtime-value allocation paths; native hashing and timestamp fields. Add instrumentation for lexical path normalization if claiming it as a cause; four readlinks do not prove repeated filesystem canonicalization. No fixes were attempted in this experiment workspace.

Official wait4 RSS includes the pre-exec Python supervisor image. A separate true-child control proves the inherited floor; the post-exec walk diagnostic avoids it. This is a supervisor accounting issue, not a Nift core memory claim. Retain raw values and do not subtract a constant. See DIAGNOSTICS.md for both controls.

## Local syscall evidence (separate from official cloud timings)

The 10k-file local traces show 21,376 `newfstatat` calls for walk and 41,376 for stat; filter has the same 41,376. The additional 20,000 calls match two queries per explicit file stat. In the frozen `src/ParserExpression.cpp:4567`, `inspect_path` calls `std::filesystem::status`, then `file_size` for regular files. `is_dir`, `is_file` and `exists` also use this complete inspector, so a type-only regular-file check fetches an unused size. This is a concrete metadata-reuse opportunity. Preserve error/race/symlink semantics when consolidating queries; do not trade correctness for a stale cache.

Only seven `readlink` calls appear in each complete local diagnostic. Do not transplant a claim of repeated filesystem canonicalization from Build Systems. Pure lexical normalization/allocation costs require CPU/allocation evidence. The strace percentages describe time inside traced syscalls, not the total program runtime. These counts are a local diagnostic pending cloud confirmation, not accepted performance rows.
