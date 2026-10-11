# Implementation notes

2026-10-11: Source inspection finds ls (sorted names), is_dir/is_file/stat (size/type), streams, copy/move and file-only remove. No public SHA-256 or mtime accessor located. Avoid FFI or helper shortcuts. Directory sorting is unavoidable for Nift ls; peers use ordinary iteration and disclose the boundary. Recursive deletion requires a separate capability check.
