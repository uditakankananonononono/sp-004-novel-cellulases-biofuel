# sp004_audit - CLI for the frozen SP-004 (DOC-1-034 R1) outputs

## Determination: (a) read-only query/audit tool over frozen outputs

`sp004_audit.py` is determination **(a)**: a read-only query/audit interface
over the frozen funnel/novelty logic outputs and result tables of R1. It is
**not** a rerunnable pipeline wrapper, and it never creates a new scientific
result for R1.

### Why (a) and not (b)

1. **The analysis code is unrecoverable.** The project README references
   `code/run_analysis.py`, `code/stage2_validation.py`, `code/evaluate_gates.py`,
   `code/pubmed_grounding.py` and `code/pubmed_broaden.py`. That directory was
   never committed to the program repository (the project's only commit,
   `6cfa8a7`, contains exactly the 22 files packaged here) and is absent from
   the Drive raw archives recovered during packaging. Recreating it would mean
   rewriting the science from memory, which is prohibited.
2. **The execution environment cannot be restored byte-exactly.** R1 ran live
   against the EBI HMMER API v1 on MGnify30-C2 (database version `2026_07`,
   Z = 128,674,267 sequences, recorded in `results/run_manifest_ref.json`),
   UniProtKB, RCSB and NCBI eutils on 2026-09-21/22. Those services serve
   current, mutable state; even a perfect code restoration would query
   different bytes today. The documented EBI API incident of 2026-09-21/22
   (`results/uniprot_screen_summary.json`) shows the live dependency is not
   stable even across two days.
3. **The frozen outputs are complete for audit.** Every reported number
   rederives from the packaged frozen tables by direct tabulation, so an
   auditor needs no rerun.

### What the CLI can and cannot do

- It **can** print frozen artifacts (`funnel`, `gates`, `structure`,
  `scrambles`, `uniprot`, `xcat`, `decoys`, `candidate`, `candidates`),
  tabulate frozen per-candidate fields (`composition`, `novelty`), and
  re-derive every gate metric from the frozen tables and compare it against
  the frozen audit record (`verify`).
- It **cannot** run phmmer, re-score candidates, re-align sequences, change a
  threshold, re-filter a pool, or emit a candidate set that differs from the
  frozen one. It contains no search, alignment, or scoring logic.

## Usage

```
python3 cli/sp004_audit.py [--root PACKAGE_ROOT] <command> [--json]

verify                          full audit; exit 0 = PASS, 1 = FAIL
funnel                          reference + decoy funnel (frozen JSON)
gates                           locked-gate evaluation (frozen JSON)
composition                     GH-family tabulation of the frozen candidate table
novelty                         predeclared sensitivity tabulation of frozen novel_at_* flags
structure                       top-50 structure-template table (frozen JSON)
decoys                          decoy-pool tabulation (frozen CSV)
scrambles                       scrambled-control outcomes (frozen JSON)
uniprot                         UniProtKB novelty screen (frozen JSON)
xcat                            30 cross-catalog replication candidates (frozen JSON)
candidate ACCESSION             one verbatim frozen candidate row
candidates [--family GH7] [--closest Tre_CBH1_GH7] [--limit N] [--csv]
                                frozen candidate rows, sorted by min E-value
```

Requires Python 3.8+ standard library only. No network access. The tool opens
files only under `--root` and never writes anywhere.

## Canonicalization (golden-output contract)

Golden outputs in `tests/golden/` are compared **byte-for-byte** under this
documented canonicalization:

- Output is UTF-8, LF line endings, no trailing whitespace, exactly one
  trailing newline per invocation.
- Numbers taken from frozen artifacts are emitted exactly as stored in those
  artifacts (CSV fields pass through as strings; JSON numbers pass through
  Python's `json` parser and `repr`, which is deterministic for the stored
  values).
- The only computed quantities are direct tabulations of frozen tables
  (counts, and the percentage shares in `composition`/`novelty`, formatted
  `%.1f%%`) and the gate arithmetic that `verify` compares against the frozen
  `results/gate_evaluation.json`.
- Table columns are space-padded to the fixed widths visible in the golden
  files; row order is the frozen file order except in `candidates`, which
  sorts by the frozen `min_evalue` field ascending.
- `verify` exit code: 0 when all 12 checks pass, 1 otherwise, 2 when invoked
  outside a package root.
- Manifest custody model: MANIFEST.sha256 lists every regular file in the
  package except itself (self-manifest exception - a file cannot hash its own
  final bytes). Coverage is enforced in both directions: the `manifest` check
  verifies every listed file's hash and presence, and the
  `inventory-exhaustive` check walks the package tree and FAILS if any
  regular file other than MANIFEST.sha256 itself is unlisted. Adding bytes to
  the package therefore fails `verify`. Custody for MANIFEST.sha256 itself
  is the outer archive SHA-256, recorded outside the archive in
  CLEAN_RESTORE_EVIDENCE.txt and the release report (a manifest cannot
  carry the hash of an archive that contains it).
