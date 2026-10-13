# Candidate refresh readiness — 2026-10-13

Candidate: committed `main` SHA `7f7e487c47a87e871dfef53345e2b71288008bff`. Use a fresh independent core clone, exact detached checkout and empty pre-build porcelain status. Untracked local core material is excluded. Historical measurements and docs remain frozen. These are preparation instructions, not a certification claim; freeze the new suite SHA only after correctness/capability gates pass.

Build with the Makefile's normal `-O2` configuration, record compiler/version/flags, source SHA, CLI SHA-256 and embedded library/adapter hashes where applicable. No sanitizer/instrumentation flags in official timing. Installers accept `NIFT_SOURCE_SHA` (full lowercase 40-digit SHA); absent override preserves historical behavior. Capture `make -n`/build log and effective flags in the shared campaign receipt. Do not reuse a local old `work/nift-source` clone for this campaign.

Comparator policy: retain historical exact versions for direct contract comparison, verify download checksums/lockfiles, and disclose these are pinned versions rather than an unsupported claim of latest. Any comparator update requires its own recorded pin and historical-comparability caveat. New series metadata may be provided with `NIFT_BENCH_VERSIONS_JSON` to filesystem/template runners; historical `docs/VERSIONS.json` stays unchanged.

Baseline suite: `97aab31427708f4864b6a685839829a8f4175fb8`; original primary `999defe8dae3f9d15e9a17225e6014020be04574`, filter supplement `5af31b2036046009c11411fe72f6193c3febf057`. Historical pins: Python 3.15.0 ordinary GIL portable, Node 24.21.0, Bun 1.4.3, Go 1.27.2, uv 0.13.0. CLI build: `NIFT_SOURCE_SHA=<candidate> bash scripts/install.sh`.

Small complete primary operation/reset certification in isolated refresh clone:

```sh
FS_STANDALONE_TOOLS=1 python3 scripts/local.py 20
python3 scripts/semantics.py
python3 scripts/refresh_semantic_gates.py
```

Standalone mode prevents historical local cert from accidentally using sibling concurrency's old Nift/tools. Cert covers all principal 1k-defined kinds/variants at 20 files, verifies output plus fixture mutations. It does not certify 100MiB boundaries; retain an untimed exact check for both 10×10MiB and 100×1MiB large-read/write/stream-write shapes before official full run. `run.py --quick` is the full-shape certification (all historical cases, one observation each), costly but complete, in a separate fresh directory, never confused with official sample counts.

```sh
python3 scripts/run.py --quick --directory work/refresh-shape-certify
python3 scripts/audit.py work/refresh-shape-certify --quick-certify
python3 scripts/audit_distributions.py work/refresh-shape-certify
```

The explicit `--quick-certify` audit requires a quick-identity marker and independently recomputes the full fixture/output/reset matrix with one sample and no warmup. Default audit still requires official counts and rejects quick identity; sparse certification is never presented as accepted measurements. Official: `python3 scripts/run.py --directory work/refresh-official`; `python3 scripts/audit.py work/refresh-official`; `python3 scripts/audit_distributions.py work/refresh-official`.

Filter generator accepts `FS_FILTER_BASE_SHA=<new frozen suite SHA>`; old default stays original primary. Generated supplement must be committed/frozen separately after local predicate/reset/oracle certification. It currently creates `work/filter-suite`, copies tracked source at BASE and symlinks tools/fixtures; start from an isolated empty refresh clone. Preserve realpath root fix for Go WalkDir.

Capability gates: stat output, SHA-256 rejection/support, recursive deletion, missing path, Unicode/space paths and **inline execute count == 1**. The historical semantics script records diagnostics; additive `refresh_semantic_gates.py` now enforces the pinned candidate, five edge-path oracles, missing-path behavior, current capability gaps and exactly-once assertions. A repeated-execution failure blocks acceptance; newly present APIs require a documented supported supplement. Candidate committed ParserExpression has no `mtime`/`sha256` identifiers; verify behavior instead of assuming missing merely from grep. Keep portable checksum and true cryptographic SHA separate. Native additions are supplements, not silent old-contract substitutions.

Memory: frozen wait4 preexec RSS has inherited-parent floor. Do not rank runtimes from that field. Retain raw historic metric for comparability disclosure, publish corrected post-exec VmHWM control separately via `scripts/postexec_memory_probe.py`. Follow existing fixtures and ordinary affinity when refreshing syscall/allocation diagnostics; profiles are outside timing.
