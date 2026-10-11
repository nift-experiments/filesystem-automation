# Filesystem / Project Automation

[Live Nift Labs report](https://lab.nift.dev/benchmarks/filesystem-automation/) · [Complete results](docs/RESULTS.md) · [Method](docs/METHOD.md) · [Practitioner judgement](docs/NIFT-FILESYSTEM-DX-REVIEW.md) · [Core handover](docs/NIFT-CORE-HANDOVER.md)

Nift, Python, Node, Bun and Go use native in-language APIs on deterministic Linux project trees. 77 scenarios; 752 supported cells; 14,264 measured samples and 752 separate warmups, all independently audited. Warm filesystem automation, not device speed. Primary suite 999defe8; separately frozen filter supplement 5af31b2; Nift source 445f4d3. No core edits.

Nift is usable for bounded project-local automation, but is not competitive for large-tree throughput in this snapshot. API gaps, exactly-once expression semantics and interpreter/metadata overhead have retained evidence. RSS launch-floor and post-exec controls are explicitly separated in [Diagnostics](docs/DIAGNOSTICS.md).

Canonical evidence belongs in nift-experiments/lab-evidence/benchmarks/filesystem-automation/20261011-v4110. Publication/teardown identities will be appended after live verification. Labs receives only compact summaries and report assets.
