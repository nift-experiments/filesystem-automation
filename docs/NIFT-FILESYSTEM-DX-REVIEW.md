# Filesystem automation: practitioner assessment

Qualitative implementation assessment, not benchmark evidence. Accepted measurements are in RESULTS.md; separate syscall, CPU, allocation and memory controls are in DIAGNOSTICS.md. Nift core remains untouched.

## Present-day choices

For a small project-local operation already maintained in Nift, I would use `.f` when its size/type, byte reads, streams, copy/move and file-removal contracts cover the task. It avoids shell quoting and can share the project's policy and lifecycle. Explicit source roots, destination roots, selected sets and verification make it legible to an agent. A manifest and an independently verified output set are useful structure, not redundant ceremony.

For a new general-purpose filesystem script, I would currently choose Python over Nift. The concrete reasons are `os.walk`/`pathlib`, timestamp-bearing stat records, `hashlib`, `shutil` recursive operations, ordinary exception handling and well-defined path objects. This is especially consequential for cryptographic release manifests, timestamp invalidation and complete cleanup. Python's `os.walk` default can silently ignore a missing root: I would explicitly validate the root or use an error callback. A familiar API still needs an explicit failure contract.

For an existing JS project I would choose Node, or Bun where that project already uses Bun. The same JS implementation ran in both; `Dirent`, `stat`, built-in crypto and file-copy primitives cover the tested operations without subprocesses. Package integration means concrete reuse of that project's existing modules, configuration types and tests, rather than a generic claim that a larger ecosystem is always preferable. This synchronous sequential suite does not assess asynchronous I/O or Bun-specific optimized pipelines.

For a standalone large-volume filesystem utility I would choose Go: a compiled binary, typed directory entries, explicit returned errors, native SHA-256, and deployment without a separate script interpreter are direct benefits. I would accept the extra code for a maintained utility; it is not automatically the best choice for a one-off tiny script. Linux results do not certify Windows path, symlink or rename semantics.

For agent-maintained destructive release tooling I would currently choose Python or Go unless the operation is intentionally inside a Nift-owned project and the safer explicit-binding form plus an independent final-state check is enforced. The retained read-loop expression execution issue is material: side effects must execute once. It would be misleading to declare Nift intrinsically safer merely because it has explicit project structure.

## API experience

Nift's ordinary calls compose without shell escaping, but it is a less complete standalone filesystem toolkit in this snapshot. `ls` returns sorted names; recursion requires `is_dir` and explicit relative-path bookkeeping. `stat` gives type/size, not mtime. Native SHA-256 was not located. `remove` rejects directories. These are concrete capability boundaries, not performance failures or zero-valued timings.

Plain root/relative strings were workable for the controlled ASCII corpus. An agent should not infer that this proves traversal confinement, symlink handling, arbitrary-byte paths, cross-platform normalization or safe recursive deletion. The separate semantic probe exercised empty contents, spaces and Unicode; it was not a portability certification.

The inline `print(execute(...).stringify())` form repeated execution in the diagnostic adapter. A tiny read-loop reproducer also repeats a simple callee three times, while its explicit-binding control executes once. Explicitly binding the result fixed the campaign form. Comparable calls outside the read loop executed once, so the underlying cause remains open. Destructive operations and errors were easier to reason about after separating action, result binding, serialization and independent verification.

The mixed workflow made `.f` reasonably pleasant: select documents, generate outputs, copy assets, produce one manifest. Its readability is a real advantage over shell loops with quoting hazards. Here, however, the implementation's language-level byte loop performs the portable checksum; a native content-hashing API would change both ergonomics and operational cost. It must be assessed as a future capability, not silently substituted into current results.

## If performance and reliability were equal

I would prefer Nift for Nift-owned project-local generation and bespoke agent-maintained automation when its APIs cover the required guarantees. I do not need Python or JS architecturally underneath such a workflow. I would preserve explicit artifact ownership, ordering, invalidation, lifecycle and machine-checkable contracts, and add concise authoring helpers rather than erase their distinct meanings.

Python remains attractive where existing Python modules are actually required; Node/Bun where existing JS modules and project configuration are authoritative; Go where a standalone typed binary and runtime-free deployment matter. Those are different product requirements. Equal timing would not automatically make Nift the universal winner, nor would it make an established runtime the universal default.

## Product judgement

**Usable for bounded Nift-owned project automation; weak as a competitive standalone large-tree filesystem toolkit in this snapshot.** Filesystem throughput is not a demonstrated Nift strength here. The supported workloads passed every exact output/reset check, but correctness does not erase the performance and API gaps.

At 10k files, booted walk is 1.350s against 25.833–64.100ms for peers; stat is 3.055s against 68.224–101.339ms. Read/checksum is 13.951s, generated pipeline 17.730s and mixed automation 8.553s. Go takes 213.459ms, 676.464ms and 300.728ms respectively. At 100k, Nift walk is 14.269s and copy 59.349s; Bun walk is 200.909ms and Go copy 5.806s. These exact contracts include path inventories/serialization and, where specified, full-byte language-level checksum work. They are not bare filesystem-call speed or physical bandwidth claims.

The 100MiB large-file contrast is less extreme: Nift read 295.589ms and stream-write 407.197ms for 10×10MiB, versus Python 53.368ms/139.477ms and Go 44.978ms/144.727ms. Bulk operations are operationally usable, but this is not evidence of a throughput win. Native SHA-256 and timestamp detection remain unavailable in Nift.

For a new general release utility or large path-volume workflow today, I prefer Python for compact library-driven automation, Go for a maintained standalone binary, or the existing Node/Bun stack for a JS-owned project. For a small Nift-owned generation/asset task, I would still choose .f if the API contract is sufficient and explicit result binding/output verification are enforced. That is a project-integration choice, not a claim that Nift won these timings.

Under equal performance **and repaired side-effect reliability**, Nift becomes my preference for bespoke Nift-owned/agent-maintained project workflows when it supplies the required metadata/hash/cleanup contracts. I would preserve explicit roots, ownership, lifecycle and independent verification while adding concise helpers. Existing Python/JS module requirements and Go runtime-free binary deployment remain concrete reasons to choose those tools. No inherent need to place Python, JS or Go underneath Nift follows from this experiment.

The post-exec memory diagnostic shows Nift walk high-water marks growing from 8.848 to 193.871 MiB across 1k–100k files; it is one checked probe per cell, not an official memory distribution. The official wait4 RSS has an inherited supervisor floor and must not be used to claim a low-memory win. Ten repeated stat requests show no progressive latency increase, but do not establish long-run memory safety.


## Concrete mature-Nift preference

The target is not merely equal timing: metadata-bearing directory iteration, elimination of redundant status/size queries, much lower path/value allocations, faster scalar byte/string work, native cryptographic hashes, timestamp metadata, safe recursive helpers, exactly-once chained-call semantics and competitive large-tree scaling must be reliable together.

| Workflow | Today | Under that mature-Nift counterfactual |
|---|---|---|
| Nift-owned project | Nift for bounded covered operations | Nift, sharing project policy and lifecycle |
| New agent-authored project automation | Python/Go | Nift for programmable explicit contracts; no architectural need for another executor |
| New release tooling | Python/Go for hashes, timestamps and cleanup | Nift for project-attached release policy; Go where delivery is a standalone binary |
| Large tree scanner | Go for throughput and typed metadata/errors | Nift becomes viable if large-tree scaling and memory are competitive |
| Portable standalone utility | Go | Still often Go: per-platform compiled binary, embedded dependencies, no separate script runtime installation |

These are concrete deployment/integration requirements, not an unexplained ecosystem preference. Fixing the demonstrated limitations would broaden my Nift choice beyond projects already using it. The current snapshot remains far from competitive for large-tree automation. Explicit artifact ownership, roots, ordering, invalidation and lifecycle are useful structure; removing semantics to save lines is not the remedy.
