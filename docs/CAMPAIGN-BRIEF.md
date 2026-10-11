I’d call the repo **`nift-experiments/filesystem-automation`** and make the campaign explicitly about **filesystem/project automation**, not storage-device benchmarking.

I’d give Codex this:

> We’re starting the next Nift Labs benchmark:
>
> **Filesystem / Project Automation**
>
> The goal is to evaluate how well Nift performs for real project-tree automation compared with other scripting/runtime environments.
>
> This should answer:
>
> > How good is Nift at traversing, inspecting, filtering, hashing, transforming and rewriting large project trees?
>
> This is not a disk benchmark and should not be framed as one.
>
> ## Repository setup
>
> Create a new public repository:
>
> `nift-experiments/filesystem-automation`
>
> Clone it locally to:
>
> `/home/nick/Repositories/nift/nift-experiments/filesystem-automation`
>
> Confirm first that the remote/path do not already exist.
>
> Follow the established experiment conventions from:
>
> - build-systems;
> - task-runners;
> - template-engines;
> - concurrency.
>
> Canonical evidence belongs in:
>
> `/home/nick/Repositories/nift/nift-experiments/lab-evidence`
>
> Labs should receive only compact publication data and rendered assets.
>
> Do not put raw samples, traces, profiles, manifests or diagnostic corpora into `lab`.
>
> ---
>
> # 1. Core question
>
> Answer:
>
> > How effectively can Nift automate realistic filesystem/project-tree workloads, and how does it compare with contemporary scripting/runtime environments?
>
> Focus on:
>
> - traversal;
> - metadata/stat operations;
> - filtering;
> - hashing;
> - manifests;
> - copying;
> - moving/renaming;
> - directory mirroring;
> - many small reads/writes;
> - large-file operations;
> - change detection;
> - generated-file workflows;
> - mixed project-tree automation;
> - memory scaling;
> - authoring/DX.
>
> ---
>
> # 2. Participants
>
> Strong default field:
>
> - **Nift**
> - **Python**
> - **Node.js**
> - **Bun**
> - **Go**
>
> This gives:
>
> - Nift as the system under test;
> - Python as a mainstream automation language;
> - Node/Bun as JS scripting/runtime comparisons;
> - Go as a compiled filesystem/project-tooling reference.
>
> Keep the field compact.
>
> Ruby or another participant can be added only if it contributes something genuinely useful.
>
> Freeze exact versions.
>
> ---
>
> # 3. Fairness principle
>
> Compare equivalent high-level work.
>
> Each participant should use its normal filesystem APIs.
>
> Do not:
>
> - call external `find`, `cp`, `rsync`, `sha256sum`, etc. for one participant unless all participants use the same external-tool boundary;
> - give Nift a native helper that does the real workload in C++;
> - intentionally choose an inefficient API for peers.
>
> Use in-language operations unless a scenario is explicitly about subprocess orchestration.
>
> ---
>
> # 4. Separate runtime cost from filesystem effects
>
> Filesystem benchmarks are noisy because of:
>
> - page cache;
> - inode/dentry cache;
> - filesystem metadata cache;
> - storage-device state.
>
> Therefore publish separate boundaries where useful:
>
> ## Fresh invocation
>
> start runtime → perform operation → exit.
>
> ## Booted/persistent runtime
>
> runtime already alive → perform operation.
>
> ## Warm filesystem state
>
> fixture has been touched/prepared consistently.
>
> Do not claim this measures physical disk speed.
>
> Say explicitly:
>
> > These are project-automation workloads over a Linux filesystem with controlled fixture state.
>
> ---
>
> # 5. Canonical fixture trees
>
> Generate deterministic fixture trees outside timed regions.
>
> Suggested sizes:
>
> - **1,000 files**
> - **10,000 files**
> - **100,000 files**
>
> Maybe 250k/1m as a stress diagnostic only if practical.
>
> Use a realistic mix:
>
> - nested directories;
> - varying depths;
> - text files;
> - small JSON-like files;
> - medium source-like files;
> - a few larger assets.
>
> Keep:
>
> - exact path manifest;
> - sizes;
> - content hashes;
> - directory structure.
>
> Use the same fixture for all participants.
>
> ---
>
> # 6. Scenario A — recursive traversal
>
> Traverse every file and directory.
>
> Measure:
>
> - 1k;
> - 10k;
> - 100k.
>
> Return:
>
> - file count;
> - directory count;
> - exact deterministic aggregate over paths.
>
> Avoid sorting unless sorting is part of the scenario.
>
> If directory iteration order differs, canonicalize only outside the core traversal measurement or define an order-independent aggregate.
>
> ---
>
> # 7. Scenario B — traversal + metadata/stat
>
> For each file collect:
>
> - type;
> - size;
> - modification time or another common metadata field.
>
> Produce an exact aggregate.
>
> This is especially important because the Build Systems experiment previously exposed heavy metadata/path activity in Nift.
>
> Profile Nift if it performs poorly.
>
> Do not pre-decide the cause.
>
> ---
>
> # 8. Scenario C — path filtering
>
> Traverse tree and select files by:
>
> - extension;
> - basename pattern;
> - directory prefix;
> - size threshold.
>
> Have several selectivity levels:
>
> - ~1%;
> - ~10%;
> - ~50%.
>
> Verify exact selected path set/hash.
>
> Compare direct traversal/filter APIs rather than shell glob expansion unless globbing itself is a separate scenario.
>
> ---
>
> # 9. Scenario D — glob/pattern matching
>
> If all participants have reasonably comparable APIs, separately measure:
>
> - `**/*.md`
> - nested source extensions;
> - multiple patterns;
> - exclusions.
>
> If semantics differ too much, keep this qualitative or omit it.
>
> Do not force artificial parity.
>
> ---
>
> # 10. Scenario E — many small reads
>
> Read:
>
> - 1k;
> - 10k;
> - 100k
>
> small files.
>
> Compute:
>
> - total bytes;
> - deterministic content hash/aggregate.
>
> Distinguish:
>
> - synchronous sequential reading;
> - concurrent reading only if later included as a separately labeled scenario.
>
> This benchmark is primarily about automation/runtime overhead, not maximum storage bandwidth.
>
> ---
>
> # 11. Scenario F — fewer large reads
>
> Use something like:
>
> - 10 × 10 MiB;
> - 100 × 1 MiB
>
> or another controlled fixture.
>
> This provides contrast with many-small-file overhead.
>
> Clearly note page-cache effects.
>
> ---
>
> # 12. Scenario G — hashing
>
> Hash all files using the same algorithm where practical, e.g. SHA-256.
>
> Two versions:
>
> ## Metadata/path manifest hash
>
> Hash path + selected metadata.
>
> ## Content hash
>
> Hash file bytes.
>
> Ensure all participants use equivalent algorithm semantics.
>
> If crypto implementations differ radically due to native library acceleration, state that clearly.
>
> This is still useful operationally.
>
> ---
>
> # 13. Scenario H — manifest generation
>
> Produce a deterministic project manifest:
>
> ```text
> relative path
> size
> content hash
> selected metadata
> ```
>
> Serialize to a common format.
>
> Measure:
>
> - traversal;
> - metadata;
> - hashing;
> - serialization;
> - write.
>
> Validate exact canonical manifest hash.
>
> This is a very realistic project-automation workload.
>
> ---
>
> # 14. Scenario I — many small writes
>
> Generate:
>
> - 1k;
> - 10k;
> - perhaps 100k tiny files if practical.
>
> File contents should be deterministic and identical across participants.
>
> Setup destination outside timing.
>
> Include:
>
> - create new;
> - overwrite existing
>
> as separate cells if useful.
>
> Validate:
>
> - file count;
> - output hashes.
>
> ---
>
> # 15. Scenario J — large writes
>
> Write a smaller number of larger files.
>
> This helps distinguish:
>
> - per-file overhead;
> - throughput.
>
> Again, do not present this as raw disk benchmarking.
>
> ---
>
> # 16. Scenario K — copy tree
>
> Copy the canonical tree to a clean destination.
>
> Measure:
>
> - 1k;
> - 10k;
> - perhaps 100k.
>
> Validate:
>
> - exact destination path set;
> - file sizes;
> - selected/full content hashes.
>
> Use each runtime’s in-language copy APIs.
>
> Be explicit about metadata preservation semantics.
>
> If APIs preserve different metadata by default, either normalize options or scope correctness to the bytes/path contract.
>
> ---
>
> # 17. Scenario L — rename/move batches
>
> Rename:
>
> - 1k;
> - 10k
>
> files within the same filesystem.
>
> Include:
>
> - flat batch rename;
> - nested directory relocation.
>
> Validate exact resulting tree.
>
> Keep cross-filesystem moves out unless intentionally tested separately.
>
> ---
>
> # 18. Scenario M — delete batches
>
> Delete:
>
> - 1k;
> - 10k;
> - perhaps 100k
>
> files/directories.
>
> Validate exact empty/remaining tree.
>
> Setup outside timing.
>
> This is worth including if participant semantics remain straightforward.
>
> ---
>
> # 19. Scenario N — directory mirror / synchronize
>
> Create:
>
> - source tree;
> - destination tree with controlled differences.
>
> Difference profiles:
>
> - no changes;
> - 1% changed;
> - 10% changed;
> - 1% added/deleted;
> - mixed changes.
>
> Implement a simple canonical mirror:
>
> - detect needed changes;
> - copy changed/new files;
> - remove deleted paths if scenario requires;
> - preserve identical files.
>
> Verify destination exactness.
>
> This is one of the strongest real-world automation scenarios.
>
> ---
>
> # 20. Scenario O — change detection
>
> Compare:
>
> - mtime-based;
> - hash-based
>
> change detection where each participant can implement both.
>
> This is especially relevant to Nift’s own project model.
>
> Use controlled mutations:
>
> - content changed with newer mtime;
> - content unchanged but mtime changed;
> - content changed while mtime restored/manipulated if safely reproducible.
>
> Report these as distinct semantics.
>
> Do not imply mtime and hash modes provide the same guarantees.
>
> ---
>
> # 21. Scenario P — project clean-check
>
> Given:
>
> - manifest of expected generated outputs;
> - actual directory tree;
>
> identify:
>
> - missing files;
> - unexpected files;
> - modified files.
>
> Return exact result set.
>
> This resembles real build/release tooling.
>
> ---
>
> # 22. Scenario Q — generated-file pipeline
>
> Realistic project operation:
>
> 1. traverse input documents;
> 2. read metadata/content;
> 3. transform a small piece of data;
> 4. write one generated output per input;
> 5. create aggregate manifest.
>
> Use:
>
> - 1k;
> - 10k;
> - perhaps 100k if practical.
>
> This may be the most representative Nift scenario.
>
> Ensure transformation itself is lightweight enough that filesystem/runtime overhead remains visible.
>
> ---
>
> # 23. Scenario R — mixed project automation
>
> Build a realistic workflow:
>
> - scan project tree;
> - ignore configured directories;
> - select sources;
> - read small metadata;
> - hash a subset;
> - generate several outputs;
> - copy static assets;
> - write manifest;
> - verify result.
>
> This should be a separate headline scenario.
>
> Do not make it Nift-specific.
>
> ---
>
> # 24. Scenario S — path manipulation microbenchmark
>
> Only if worthwhile.
>
> Operations:
>
> - dirname;
> - basename;
> - extension;
> - join;
> - normalize;
> - relative path.
>
> Use many iterations in-memory.
>
> This can expose runtime/path-library overhead but should not dominate the report.
>
> Keep it clearly labeled as a microbenchmark.
>
> ---
>
> # 25. Scenario T — filesystem concurrency
>
> Optional secondary section, since concurrency was just benchmarked separately.
>
> If included:
>
> - bounded 4-worker read/hash;
> - bounded 4-worker file generation.
>
> Compare only as a filesystem automation scenario.
>
> Do not re-run a whole concurrency campaign.
>
> ---
>
> # 26. Correctness
>
> Every cell must validate its work.
>
> Use:
>
> - exact path sets;
> - counts;
> - deterministic hashes;
> - manifest hashes;
> - destination-tree comparison;
> - expected changed-file sets.
>
> Create an independent oracle.
>
> A participant that skipped filesystem work does not receive a valid timing.
>
> ---
>
> # 27. Fixture lifecycle
>
> Be rigorous about fixture preparation.
>
> For destructive scenarios:
>
> - restore fixture outside timing;
> - verify starting state;
> - perform measured operation;
> - verify final state;
> - restore for next sample.
>
> Do not let one participant benefit from a different fixture state.
>
> Retain fixture-generation source and canonical manifest.
>
> ---
>
> # 28. Cache-state policy
>
> Do not pretend we can fully control Linux filesystem caches cheaply.
>
> Prefer:
>
> - repeatable warm-state measurements;
> - clearly documented fixture preparation;
> - rotating participant order;
> - enough samples.
>
> If a cold-cache diagnostic is feasible without privileged/destructive host changes, keep it separate.
>
> Do not drop caches globally merely to manufacture a “cold disk” claim unless methodology is extremely controlled and justified.
>
> ---
>
> # 29. Sampling
>
> Use workload-sensitive sample counts:
>
> - very short cells: 50–100+;
> - moderate cells: 20–50;
> - multi-second cells: 5–10;
> - very expensive 100k destructive cells: 3–5 if needed.
>
> Warmups separate.
>
> Preserve all samples.
>
> No outlier deletion.
>
> ---
>
> # 30. Metrics
>
> Primary:
>
> - wall time.
>
> Also capture:
>
> - CPU time;
> - process RSS;
> - maximum child RSS where subprocesses exist;
> - files/sec;
> - MiB/sec where meaningful;
> - stat calls / open calls in diagnostics;
> - syscall counts for selected scenarios.
>
> Be cautious with derived throughput where work varies by file size.
>
> ---
>
> # 31. Nift-specific diagnostics
>
> We already have a strong reason to watch metadata/path overhead from the Build Systems benchmark.
>
> If Nift underperforms in:
>
> - traversal;
> - no-change scans;
> - stat-heavy workloads;
> - path filtering;
>
> profile with:
>
> - `strace -f -c`;
> - `perf`;
> - allocation profiling/counters;
> - path normalization counts;
> - stat/open/read call counts.
>
> Investigate:
>
> - repeated `stat` calls;
> - repeated canonicalization/normalization;
> - duplicated path allocations;
> - string copying;
> - unnecessary filesystem existence checks;
> - directory-entry metadata reuse opportunities;
> - hash-mode bookkeeping.
>
> Do not assume the Build Systems diagnosis applies unchanged.
>
> Prove it in this corpus.
>
> ---
>
> # 32. Keep Nift core untouched
>
> **Do not modify Nift core from this experiment workspace.**
>
> If a core issue is found:
>
> - create a minimal reproducer;
> - retain profile/syscall evidence;
> - write `docs/NIFT-CORE-HANDOVER.md`;
> - explain likely general benefit;
> - leave implementation to the separate core workspace.
>
> ---
>
> # 33. DX / practitioner notes
>
> Maintain:
>
> `docs/DX-NOTES.md`
>
> while implementing.
>
> Record:
>
> - traversal API ergonomics;
> - path handling;
> - error handling;
> - file reading/writing;
> - recursive operations;
> - copying;
> - deleting;
> - hashing;
> - glob/filter syntax;
> - manifest generation;
> - metadata access;
> - portability;
> - verbosity;
> - agent readability.
>
> Do not reconstruct these impressions at the end.
>
> ---
>
> # 34. Agent-maintainability assessment
>
> Explicitly evaluate:
>
> - Are paths represented clearly?
> - Are destructive operations obvious?
> - Is filesystem state easy for an agent to reason about?
> - Are errors explicit?
> - Is traversal order implicit or explicit?
> - Are relative/project-root semantics clear?
> - Can operations be composed without shell quoting?
> - Can tooling verify the intended input/output set?
>
> More structure is not automatically bad ceremony if it makes destructive automation safer.
>
> ---
>
> # 35. Practitioner review
>
> At the end create:
>
> `docs/NIFT-FILESYSTEM-DX-REVIEW.md`
>
> Answer:
>
> > Would I actually choose Nift for filesystem/project automation?
>
> Compare:
>
> - Nift vs Python;
> - Nift vs Node;
> - Nift vs Bun;
> - Nift vs Go.
>
> Address:
>
> - small scripts;
> - large project trees;
> - release/build automation;
> - file-generation pipelines;
> - agent-maintained automation;
> - cross-platform use;
> - large-volume path operations.
>
> If performance were equal, what would you choose by workload?
>
> Avoid vague “ecosystem” reasons.
>
> Name exact requirements:
>
> - Python libraries;
> - Node package integration;
> - Bun APIs;
> - Go deployment;
> - path semantics;
> - native hashing;
> - etc.
>
> ---
>
> # 36. Product conclusion
>
> Explicitly answer:
>
> > Is filesystem/project automation a genuine strength of Nift?
>
> Possible conclusion:
>
> - weak;
> - usable;
> - good with caveats;
> - compelling.
>
> Do not decide in advance.
>
> ---
>
> # 37. Local feasibility before cloud
>
> Before provisioning:
>
> - implement every participant;
> - certify outputs;
> - estimate campaign runtime/storage;
> - check destructive fixture reset;
> - ensure 100k cases are practical;
> - identify unsupported scenarios.
>
> Stop and report if:
>
> - fixture restoration dominates prohibitively;
> - semantics cannot be made equivalent;
> - filesystem state makes a scenario too unreliable.
>
> ---
>
> # 38. Freeze suite
>
> Freeze:
>
> - fixture generator;
> - canonical fixture manifest;
> - scenario matrix;
> - participant implementations;
> - runtime versions;
> - sample counts;
> - commands;
> - expected hashes;
> - cache-state methodology.
>
> Record exact:
>
> - Nift source SHA;
> - suite SHA;
> - Python version;
> - Node version;
> - Bun version;
> - Go version.
>
> ---
>
> # 39. Official machine
>
> Use one fresh inexpensive Linode after local certification.
>
> Prefer the established:
>
> - g6-standard-4;
> - us-east;
> - Ubuntu 24.04
>
> if still appropriate.
>
> Record:
>
> - CPU;
> - RAM;
> - kernel;
> - filesystem;
> - mount options if relevant;
> - available storage;
> - runtime versions.
>
> Same node for all participants.
>
> Rotate participant order within rounds.
>
> ---
>
> # 40. Evidence
>
> Canonical evidence belongs under:
>
> `nift-experiments/lab-evidence/benchmarks/filesystem-automation/<series>/`
>
> Preserve:
>
> - environment;
> - fixture manifest;
> - scenario matrix;
> - participant code;
> - commands;
> - raw samples;
> - warmups;
> - output hashes;
> - filesystem state receipts;
> - diagnostics;
> - strace/perf captures;
> - rejected attempts;
> - independent audit;
> - publication identities;
> - browser checks;
> - teardown.
>
> ---
>
> # 41. Labs page
>
> Work in:
>
> `/home/nick/Repositories/nift/lab`
>
> Add:
>
> `https://lab.nift.dev/benchmarks/filesystem-automation/`
>
> Add cards/links to:
>
> - homepage;
> - benchmark collection.
>
> Preserve all existing report content/assets except those intentional additions.
>
> ---
>
> # 42. IMPORTANT — give this report its own visual identity
>
> Recent Labs experiment pages have started looking **too suspiciously similar to one another**.
>
> Do **not** clone the layout/visual treatment of:
>
> - Concurrency;
> - Task Runners;
> - Template Engines;
> - Build Systems.
>
> The page should still clearly belong to **Nift Labs**, but it needs its **own dark-mode design** in the same spirit as how earlier Labs reports each had a distinct visual concept.
>
> Preserve:
>
> - dark-mode Labs identity;
> - charcoal base;
> - fluorescent-green shared Labs accents/favicons;
> - restrained sherbet/sorbet accent palette;
> - high information density;
> - responsive/mobile quality.
>
> But create a new composition, hierarchy and visual metaphor.
>
> Do not simply:
>
> - reuse the same hero structure;
> - reuse the same rounded stat cards;
> - reuse the same section framing;
> - reuse the same chart wrappers;
> - swap headings and colors.
>
> Treat this as a bespoke report design.
>
> ---
>
> # 43. Suggested unique visual direction
>
> Give Filesystem Automation a visual language around:
>
> **“project tree / file cabinet / path map / terminal filesystem inspector”**
>
> rather than execution lanes or dependency graphs.
>
> Possible motifs:
>
> - a large ASCII/tree-like directory map;
> - nested path columns;
> - file/directory rows flowing through filters;
> - path breadcrumbs;
> - filesystem metadata strips;
> - manifest/hash stamps;
> - diff/mirror before→after panels;
> - directory-tree heatmaps;
> - file-size/path-density visualizations;
> - terminal-style `ls`/tree-inspired structures;
> - file nodes rather than task nodes.
>
> Think:
>
> > walking and transforming a project tree
>
> rather than:
>
> > orchestrating jobs.
>
> A good hero might visually show:
>
> ```text
> project/
> ├── content/
> │   ├── ...
> ├── assets/
> ├── generated/
> └── manifest.json
> ```
>
> with selected paths being scanned/hashed/copied into an output tree.
>
> It should not look like the Concurrency control-room page.
>
> ---
>
> # 44. Suggested page structure
>
> Do not mechanically reuse the numbering/layout of other reports.
>
> A possible structure:
>
> **Hero / project tree**
> - what is being compared;
> - canonical fixture;
> - participants.
>
> **Walk the tree**
> - recursive traversal.
>
> **Ask every file**
> - stat/metadata.
>
> **Find what matters**
> - filtering/globbing.
>
> **Read everything**
> - many-small vs large reads.
>
> **Fingerprint it**
> - hashing.
>
> **Write the manifest**
> - aggregate real-world workload.
>
> **Make a copy**
> - copy/mirror.
>
> **Move the tree**
> - rename/delete operations.
>
> **What changed?**
> - mtime/hash incremental detection.
>
> **Generate the project**
> - generated-file pipeline.
>
> **Do the whole job**
> - mixed project automation.
>
> **Memory / syscall view**
> - resource/diagnostic findings.
>
> **Would I use Nift?**
> - practitioner judgement.
>
> **Method / evidence**
> - frozen identities and canonical evidence.
>
> Feel free to improve this structure if another bespoke design works better.
>
> ---
>
> # 45. Charts and visualizations
>
> Every chart needs an exact table.
>
> Useful charts:
>
> - traversal time vs file count;
> - stat time vs file count;
> - small-read throughput;
> - content-hash throughput;
> - manifest-generation time;
> - copy/mirror time;
> - changed-percent vs sync time;
> - mtime vs hash change-detection cost;
> - generated-pipeline scaling;
> - RSS vs file count.
>
> Consider visuals beyond conventional line charts:
>
> - before/after directory diagrams;
> - manifest excerpts;
> - syscall composition bars;
> - file-tree density illustrations.
>
> Keep graphics functional rather than decorative.
>
> ---
>
> # 46. Practitioner section
>
> End the live report with:
>
> **“Would I actually choose Nift for filesystem automation?”**
>
> Clearly mark:
>
> **qualitative practitioner assessment / not benchmark evidence**
>
> Include a decision matrix, perhaps:
>
> | Workflow | Preferred runtime | Why |
> |---|---|---|
> | Nift-owned project automation | ? | ? |
> | Agent-maintained release tooling | ? | ? |
> | Large tree scanning | ? | ? |
> | Existing Python tooling | ? | ? |
> | Existing JS tooling | ? | ? |
> | New standalone filesystem utility | ? | ? |
> | Cross-platform deployment | ? | ? |
>
> Fill after the campaign.
>
> Be candid.
>
> If Nift loses badly somewhere, say so.
>
> If Nift’s project-integrated model is better somewhere, say so.
>
> ---
>
> # 47. Nift-specific opinion questions
>
> Ask Codex:
>
> - Does Nift’s filesystem API feel coherent?
> - Is it easier to write safely than shell automation?
> - Does `.f` make project automation pleasant?
> - Are path semantics obvious?
> - Are recursive operations missing important primitives?
> - Is hashing/change detection natural?
> - Does Nift require too many stat/existence checks?
> - Are errors descriptive enough?
> - Would an agent safely maintain destructive file operations in Nift?
> - Would you choose Nift over Python for a new project-local automation script?
> - Would you choose Nift over Node/Bun?
> - What would make you prefer Go?
>
> ---
>
> # 48. Storage discipline
>
> The hardened Labs policy must remain intact.
>
> Before Labs commits:
>
> run:
>
> `python3 scripts/check_storage_policy.py`
>
> plus normal site validation.
>
> Labs may contain:
>
> - compact publication dataset;
> - report HTML/source;
> - charts;
> - necessary CSS/JS/assets.
>
> Labs must not contain:
>
> - raw timing arrays;
> - raw memory samples;
> - fixture corpora;
> - traces;
> - strace/perf captures;
> - canonical manifests beyond compact publication needs;
> - archives.
>
> Report:
>
> - net tracked bytes added;
> - largest new file;
> - confirmation no raw evidence entered Labs.
>
> ---
>
> # 49. Browser validation
>
> Validate:
>
> - 1440 px;
> - 390 px;
> - 320 px.
>
> Check:
>
> - report;
> - benchmark index;
> - homepage.
>
> Ensure:
>
> - no page-level overflow;
> - tree/path visualizations remain readable;
> - tables scroll independently;
> - long paths wrap/scroll safely;
> - hashes/SHAs do not destroy mobile layout;
> - charts and exact tables align;
> - favicon remains the shared green Labs test tube.
>
> ---
>
> # 50. Preservation
>
> Verify every prior report/public asset is unchanged except intentional:
>
> - homepage;
> - benchmark collection.
>
> Produce a preservation receipt.
>
> ---
>
> # 51. Publication lifecycle
>
> Follow established order:
>
> 1. local feasibility/correctness;
> 2. freeze suite;
> 3. official cloud measurement;
> 4. independent audit;
> 5. experiment result commit;
> 6. canonical evidence commit;
> 7. Labs source update;
> 8. source push;
> 9. public publication;
> 10. live byte/browser verification;
> 11. Linode teardown;
> 12. append lifecycle evidence.
>
> Keep all identities distinct.
>
> ---
>
> # 52. Teardown
>
> Only after verified publication:
>
> - delete Linode;
> - verify CLI absence;
> - authenticated API 404;
> - remove temporary SSH key;
> - remove known-host entry;
> - remove temporary CLI config/state;
> - run private-material scan.
>
> ---
>
> # 53. Checkpoints
>
> Commit/push around:
>
> 1. repo + campaign brief;
> 2. participant/fairness plan;
> 3. fixture generator + canonical manifest;
> 4. workload implementations;
> 5. local correctness;
> 6. feasibility/sample plan;
> 7. frozen suite;
> 8. cloud campaign;
> 9. audit/diagnostics;
> 10. practitioner review/core handover;
> 11. canonical evidence;
> 12. bespoke Labs design/report;
> 13. publication verification;
> 14. teardown/closeout.
>
> ---
>
> # 54. Final report back
>
> Return:
>
> - repo URL/local path;
> - participants and rationale;
> - exact versions/SHAs;
> - canonical tree sizes;
> - scenario matrix;
> - sample/observation counts;
> - correctness/audit result;
> - headline traversal results;
> - stat/metadata results;
> - read/write results;
> - hashing results;
> - copy/mirror results;
> - change-detection results;
> - generated/mixed-workflow results;
> - memory/syscall findings;
> - Nift bottlenecks;
> - core handover if needed;
> - Codex’s qualitative preferences;
> - whether filesystem/project automation is a genuine Nift strength;
> - experiment commit;
> - evidence commit;
> - Labs source commit;
> - publication commit;
> - live URL;
> - Labs byte growth;
> - teardown status.
>
> ## Hard boundary
>
> **Do not modify Nift core from the experiment workspace.**
>
> If core changes seem necessary, come back with:
>
> - minimal reproducer;
> - retained diagnostic evidence;
> - suspected general issue;
> - proposed investigation/fix direction.

The visual-design instruction is worth being unusually explicit about this time. I’d rather Codex spend a little more effort on a bespoke **filesystem/tree/manifest** visual language than have Labs gradually turn into “same report template, different heading.” The shared dark Nift Labs identity should make the pages feel related; their actual composition should still make each experiment immediately recognizable.