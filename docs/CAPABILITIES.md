# Capability boundaries

All five: native in-language enumeration, size/type inspection, byte reads, stream writes, copy, same-filesystem rename, per-file deletion, portable checksum, canonical TSV manifests and controlled content-based mirroring.

Nift native SHA-256: no located public API; direct sha256 probe rejected. Nift timestamp detection: stat returns exists/type/size with no mtime. These cells are unavailable. File-only deletion leaves directories deliberately; native recursive directory removal is not represented as equivalent. Glob parity is qualitative/omitted. No FFI or external helper supplies missing capabilities.

Semantic probes retain Unicode/space/empty-file traversal and missing-directory behavior. Python os.walk returns an empty traversal for a missing tree by default; other participants may signal failure. Campaign fixtures have certified readable roots, so this difference is recorded outside timing and should matter to safety review.

Nift inline chained workload/result serialization reproduced three executions; explicit result binding reproduced one. Destructive workloads use explicit binding and independent final-state checks. This is a core-handover finding, not silently discarded adapter noise.
