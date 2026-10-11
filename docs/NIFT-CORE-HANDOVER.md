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

Only seven `readlink` calls appear in each complete local diagnostic. Do not transplant a claim of repeated filesystem canonicalization from Build Systems. Pure lexical normalization/allocation costs require CPU/allocation evidence. The strace percentages describe time inside traced syscalls, not the total program runtime. The cloud trace independently confirms the same 20,000-call increment (21,373 to 41,373). Local and cloud traces are separate diagnostics, not accepted performance rows.


## Prioritized core work after publication review

### P0 — exactly-once chained-call evaluation

Frozen no-filesystem reproducer: `repro/inline-loop.f`; paired control: `repro/bound-loop.f`. Run the pinned binary with one `walk|3` line followed by EOF. Inline: three CALLED lines; bound: one; both return the same one-element array. Cloud controls confirm the same outcome. The rejected rename adapter demonstrates why this is correctness-critical: the first rename succeeds, an unintended second execution encounters ENOENT. Accepted adapters bind the result and pass full state/output oracles.

Read-only source investigation identifies a likely speculative-dispatch mechanism. In pinned `src/ParserExpression.cpp:2695`, the postfix known-method list omits `stringify`. At line 2733 the unknown-method module fallback evaluates the receiver before checking whether its value is an object; an effectful array-returning receiver can therefore run and then fall through. The presentation handler at line 2644 and generic postfix receiver evaluation at line 3917 are additional execution paths to inspect. These source sites show an unsafe pattern to investigate, but do not prove which three paths were traversed in the read-loop case. No instrumentation or core patch was added. Trace handler entry/handled/result transitions against the retained reproducer before claiming a complete root cause.

Core acceptance: decide dispatch without executing a receiver speculatively, or preserve exactly one evaluated receiver across handling; test chained effects, arrays/objects/scalars, read-loop and non-loop contexts, errors, destructive filesystem calls and serialization. Do not solve it only by prescribing temporary variables to users.

### P1 — metadata-bearing iteration and selective inspection

Walk 10k: 21,373 newfstatat; stat/filter 10k: 41,373; read 10k: 51,373. The extra 20,000 calls match status + size for every explicit file stat. `inspect_path` at line 4567 queries status, then size for regular files; type-only `is_dir`/`is_file`/`exists` also use the full inspector. Directory traversal receives names and reacquires type metadata. Investigate entries carrying reusable type/size/timestamps and distinct cheap type checks. Instrument calls per logical file at each API layer. Preserve fresh-versus-cached metadata contracts, errors, races, symlink behavior and traversal confinement; do not introduce a silently stale global cache. Four cloud readlinks do not establish repeated filesystem canonicalization.

### P1 — allocation/value/path churn

Retain `diagnostics/stat.heaptrack.zst` and decoded `stat-heaptrack.txt` in canonical evidence. 5,578,191 allocation calls, 1,111,623 temporary allocations, 19.37 MB printed peak heap. The leading string-construction group has 936,118 calls; a condition `trim_copy` stack has 100,000 calls. That identifies concrete strings/condition processing, not a complete allocation decomposition. CPU samples also show expression evaluation, malloc, string construction and balanced scanning. Instrument owned path bytes, substring/normalization copies, RuntimeValue deep copies, container capacities and temporary conversions independently. Consider source views/prepared expressions and reserved containers while preserving value-copy independence and resource lifetimes. Instrumentation timings are not accepted benchmark medians.

### P1/P2 — separate bulk I/O from scalar checksum execution

Read/checksum 100k takes 148.707s in Nift; the 100 MiB bulk-read endpoints contract is much less extreme. Read profiles contain AST evaluation (8.62% self), RuntimeValue destruction (5.86%), move assignment (3.53%), statement dispatch (3.39%) and variable lookup (2.90%). These sampled shares are diagnostic, with unresolved symbols elsewhere. In a future core investigation, isolate full-byte read, byte iteration, integer arithmetic, conversion and loop dispatch using identical inputs/output checks. Do not subtract medians of different contracts, or replace the accepted portable checksum with a native digest and call it the same benchmark.

### Capability work

Timestamp-bearing metadata; native SHA-256 or a named cryptographic hash API; safe recursive removal/copy with explicit root/symlink/error semantics. Current file-only remove is not complete recursive cleanup. These belong in core, not the experiment adapter.

## Shared runtime leads — three signals, not one proven cause

Template Engines retained a 3.641258 ms large request-context literal render versus 0.002193 ms engine-default control, showing context-copy cost; the official large loop is 113.578 ms, so copying alone cannot explain it. Its short CPU profile includes expression/string/allocation work. Concurrency demonstrates 3.950× four-worker scaling yet expensive absolute scalar CPU work; profiles include AST/value handling, and source suggests binding/registry snapshot amplification. Filesystem independently shows value lifetime/dispatch, condition trimming, millions of allocations and metadata amplification. Prepared-expression reuse, value-copy ownership and scalar dispatch are plausible shared optimization targets. Worker-registry growth, render-context copying and filesystem stat duplication are different mechanisms until profiling/instrumentation establishes overlap. Preserve the individual campaigns and investigate in the core workspace.
