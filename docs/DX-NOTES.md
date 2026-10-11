# Implementation notes

2026-10-11: Source inspection finds ls (sorted names), is_dir/is_file/stat (size/type), streams, copy/move and file-only remove. No public SHA-256 or mtime accessor located. Avoid FFI or helper shortcuts. Directory sorting is unavoidable for Nift ls; peers use ordinary iteration and disclose the boundary. Recursive deletion requires a separate capability check.

Small-fixture implementation: standalone Nift reserves `name` for metadata; explicit `fname` avoids the conflict. Bytes require indexed iteration rather than JSON-array `for`. Public ls yields sorted names; canonical manifest follows the sorted recursive traversal without a separate collection-sort call. An inline execute(...).stringify() form unexpectedly repeated a destructive traversal; assigning the result before serialization passed rename/delete verification. Simple isolated stringify probes did not reproduce that behavior: root cause remains unresolved, retain the rejected adapter form for investigation rather than assert a parser cause.

Python 3.15.0 portable ordinary-GIL installed through uv. All five adapters passed 20-file exact row/output checks after explicit result binding. Full-size certification is in progress. No cloud provisioning or accepted timings yet.
