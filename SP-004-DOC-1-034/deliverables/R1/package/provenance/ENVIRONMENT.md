# Environment notes - DOC-1-034 R1 package

## Original R1 execution environment (partially recoverable)

Recoverable from the frozen artifacts:
- Search engine: phmmer via EBI HMMER API v1 (live service).
- Database: MGnify30-C2 - Non-singletons; db key `mgnify30_c2`; database
  version `2026_07` recorded at run time; Z = 128,674,267 sequences
  (results/run_manifest_ref.json, per-job stats).
- Stage-2 catalog: MGnify30-C5-ppfam (results/run_manifest_validation.json).
- Alignment for F4/F6: Biopython PairwiseAligner, global, BLOSUM62,
  open -11, extend -1 (locked protocol filter text).
- Run dates: 2026-09-21 (primary funnel, grounding, literature) and
  2026-09-21/22 (stage-2 validation; EBI HMMER API incident window).
- Retrieval and validation job UUIDs: results/run_manifest_*.json.

NOT recoverable (registered in MISSING_ARTIFACTS.md):
- Python version, OS image, installed package versions, requirements file or
  container image used for the R1 run.
- The R1 analysis code itself (code/ directory).

Consequence: the original environment cannot be restored byte-exactly, which
is one of the three recorded reasons the packaged CLI is determination (a),
a read-only query/audit tool, not a rerunnable pipeline wrapper.

## Packaging environment (this package)

- Date: 2026-09-23 (UTC+05:30).
- OS: Linux x86_64 (kernel 6.1.158), sandbox container.
- Python 3.10.12 (CLI and tests: standard library only).
- pdfTeX 3.141592653-2.6-1.40.22 (TeX Live 2022/dev/Debian); packages used:
  geometry, mathptmx, color, colortbl, array, longtable, graphicx, fancyhdr,
  url. (hyperref unavailable in this TeX installation - pdftexcmds.sty
  missing - so the PDF has no hyperlink layer; all references are numeric.)
- Paper rebuild: `pdflatex DOC-1-034-R1-paper.tex` run twice from the
  package `paper/` directory (figure paths are relative: ../figures/).
