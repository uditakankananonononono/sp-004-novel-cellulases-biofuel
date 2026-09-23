# DOC-1-034 R1 (SP-004 cellulase discovery) - publication package

Packaging-only backfill of the frozen R1 result: 1,433 novel, catalytically
intact cellulase candidates from MGnify30-C2, locked-gate PASS 6/6. Scientific
bytes and claims are frozen; this package adds presentation, audit tooling,
and provenance only.

## Contents
- `paper/DOC-1-034-R1-paper.pdf` - submission-length paper (22 pages)
- `paper/DOC-1-034-R1-paper.tex` - paper source (pdflatex; rebuild twice)
- `paper/SOURCE_paper.md` - original short paper (frozen)
- `figures/` - the two frozen figures
- `protocol/` - locked protocol + feasibility log (frozen)
- `report/` - report, literature ledger, project summary, source README (frozen)
- `results/` - all 13 frozen result artifacts (gate record, funnels, candidate
  tables, structure check, cross-catalog set, scrambles, UniProt screen, run manifests)
- `cli/sp004_audit.py` - read-only query/audit CLI (determination (a));
  see `cli/CLI_README.md`
- `tests/` - golden-output test suite (byte-for-byte) + corruption test
- `provenance/` - environment notes, provenance chain + raw-archive registry,
  missing-artifacts registry
- `MANIFEST.sha256` - SHA-256 of every packaged file
- `PACKAGE_MANIFEST.json` - machine-readable package summary

## Restore and audit (no network, Python 3.8+ stdlib only)
```
tar xzf DOC-1-034-R1-package.tar.gz
cd DOC-1-034-R1-package
sha256sum -c MANIFEST.sha256
python3 cli/sp004_audit.py verify     # 12-check audit; exit 0 = PASS
python3 tests/run_tests.py            # golden outputs + corruption test
```

Clean-restore evidence for this exact archive ships alongside it as
CLEAN_RESTORE_EVIDENCE.txt (kept outside the archive so its own hash never
becomes self-referential).

## Boundary
Computational nomination only. No enzymatic activity is claimed for any
candidate; no wet-lab validation was performed. The "1,433 final candidates"
retains its original locked definition (F1 length, F2 cellulase-GH Pfam,
F3 E<=1e-10, F4 <40% identity to all 15 references, F6 catalytic Asp/Glu
conservation) and its caveats (paper Section 6, Appendix F).
